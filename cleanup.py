"""The functions for cleaning up VH7 on a regular basis."""

import db
import datetime
import os
import config
from timeloop import Timeloop
from datetime import timedelta

tl = Timeloop()


@tl.job(interval=timedelta(hours=2))
def cleanup_uploads():
    """A function for cleaning up expired uploads."""
    print("Performing cleanup...")

    results = list(db.Upload.query.filter(
        db.Upload.expires <= datetime.datetime.now(),
        db.Upload.filename.isnot(None)))
    print("Found {} expired uploads!".format(len(results)))

    for result in results:
        path = os.path.join(config.UPLOAD_FOLDER, result.filename)
        # Delete the file
        try:
            os.remove(path)
        except FileNotFoundError:
            print("File doesn't exist!")
        # Update path in the database
        result.filename = None
        # Save changes to the database
        db.db.session.commit()


def start():
    """Start the cleanup function timers."""
    tl.start()


def stop():
    """Stop the cleanup function timers."""
    tl.stop()
