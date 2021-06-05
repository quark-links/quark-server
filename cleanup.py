"""Methods for cleaning up expired uploads.

These should be run as a cronjob. For example, to run every 6 hours:

    0 */6 * * * /path/to/venv/python /path/to/quark-server/cleanup.py >/dev/null 2>&1
"""

from logzero import logger
import models
from database import SessionLocal
import datetime
from utils.uploads import get_path
import os


def run_cleanup() -> None:
    """Perform a full cleanup."""
    logger.info("Performing cleanup...")

    db = SessionLocal()
    results = db.query(models.Upload).filter(
        models.Upload.filename.isnot(None)).join(models.ShortLink).filter(
        models.ShortLink.expiry <= datetime.datetime.utcnow())

    logger.info("Found {} expired uploads!".format(results.count()))

    for result in results:
        path = get_path(result.filename)

        try:
            os.remove(path)
        except FileNotFoundError:
            logger.warning("The file '{}' doesn't exist for upload {}".format(
                result.filename, result.id))

        logger.debug("Removed upload {}!".format(result.id))

        result.filename = None
        db.add(result)

    logger.debug("Saving database changes...")
    db.commit()
    db.close()


if __name__ == "__main__":
    run_cleanup()
