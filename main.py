"""Main VH7 API server."""
from fastapi import Header
from cleanup import run_cleanup
from utils.uploads import get_path
from fastapi import FastAPI, Depends, File, UploadFile
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from starlette.responses import FileResponse, JSONResponse, RedirectResponse, Response
import uvicorn
from fastapi_utils.tasks import repeat_every
import crud
from crud import get_or_create_user
import schemas
from database import SessionLocal
from datetime import datetime
from typing import Any, Dict, Optional, List
from fastapi.middleware.cors import CORSMiddleware
from os import getenv
from urllib.parse import urljoin
from logzero import logger
import utils.languages
import models
import auth

VERSION = "1.2.0"

app = FastAPI(title="VH7",
              description=("A free and open source URL shortening, file "
                           "sharing and pastebin service."),
              version=VERSION, openapi_tags=[
                  {
                      "name": "users",
                      "description": ("Operations with users. The **login** "
                                      "logic is also here.")
                  },
                  {
                      "name": "routing",
                      "description": ("Routing endpoints for seamless "
                                      "integration with the web app.")
                  }
              ])
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])

oauth_scheme = auth.CustomOAuth2()


def get_db() -> Session:
    """Fetch a database instance.

    Yields:
        Session: A database instance
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth_scheme),
                     db: Session = Depends(get_db)) -> Optional[models.User]:
    """Get the current user.

    Args:
        authorization (Optional[str], optional): The user's authorization
            header. Defaults to Header(None).
        db (Session, optional): A database instance. Defaults to
            Depends(get_db).

    Returns:
        Optional[models.User]: The current user.
    """
    if token is None:
        return None

    token_data = auth.parse_token(token)

    user = get_or_create_user(db=db, sub=token_data["sub"])
    return user


def get_required_user(user: schemas.User = Depends(get_current_user)
                      ) -> schemas.User:
    """Get the current user and fail if they are not logged in.

    Args:
        user (schemas.User, optional): The current user. Defaults to
            Depends(get_current_user).

    Returns:
        schemas.User: The current user.
    """
    if user is None:
        raise HTTPException(status_code=401,
                            detail="Authentication is required",
                            headers={"WWW-Authenticate": "Bearer"})
    return user


@app.get("/", tags=["routing"])
def web_app() -> Response:
    """Redirect to the web app."""
    return RedirectResponse(getenv("INSTANCE_APP_URL", "https://app.vh7.uk"),
                            status_code=308)


@app.post("/shorten", response_model=schemas.ShortLink)
def create_shorten(url: schemas.Url, db: Session = Depends(get_db),
                   user: Optional[schemas.User] =
                   Depends(get_current_user)) -> Response:
    """Shorten a URL into a short link."""
    return crud.create_shorten(db=db, url=url, user=user)


@app.post("/paste", response_model=schemas.ShortLink)
def create_paste(paste: schemas.PasteCreate, db: Session = Depends(get_db),
                 user: Optional[schemas.User] =
                 Depends(get_current_user)) -> Response:
    """Save code to a short link."""
    return crud.create_paste(db=db, paste=paste, user=user)


@app.post("/upload", response_model=schemas.ShortLink)
def create_upload(file: UploadFile = File(...), db: Session = Depends(get_db),
                  user: Optional[schemas.User] =
                  Depends(get_current_user)) -> Response:
    """Upload a file to a short link."""
    return crud.create_upload(db=db, filename=file.filename, file=file.file,
                              mimetype=file.content_type, user=user)


@app.get("/info/{link}", response_model=schemas.ShortLink)
def short_link_info(link: str, db: Session = Depends(get_db)) -> Response:
    """Get information on a given short link."""
    short_link = crud.get_short_link(db=db, link=link)

    if short_link is None:
        raise HTTPException(status_code=404,
                            detail="Short link not found")

    if (short_link.expiry is not None and
            short_link.expiry <= datetime.utcnow()):
        raise HTTPException(status_code=404,
                            detail="The given short link has expired")

    return short_link


@app.get("/dl/{link}")
def short_link_download(link: str, db: Session = Depends(get_db)) -> Response:
    """Download the file from a given short link (only for uploads)."""
    short_link = crud.get_short_link(db=db, link=link)

    if short_link is None:
        raise HTTPException(status_code=404,
                            detail="Short link not found")

    if short_link.upload is None:
        raise HTTPException(status_code=404,
                            detail="The given short link is not a file")

    if (short_link.expiry is not None and
        short_link.expiry <= datetime.utcnow() or
            short_link.upload.filename is None):
        raise HTTPException(status_code=404,
                            detail="The given short link has expired")

    return FileResponse(get_path(short_link.upload.filename),
                        filename=short_link.upload.original_filename,
                        media_type=short_link.upload.mimetype)


@app.get("/users/me", response_model=schemas.User, tags=["users"])
def get_user(current_user: schemas.User = Depends(get_required_user),
             token: str = Depends(oauth_scheme)) -> JSONResponse:
    """Get the logged in user details."""
    if token is None:
        raise auth.AuthError

    profile = auth.get_profile(token)
    return JSONResponse(profile)


@app.get("/users/me/links", response_model=List[schemas.ShortLink],
         tags=["users"])
def get_user_links(db: Session = Depends(get_db), current_user: models.User =
                   Depends(get_required_user)) -> Response:
    """Get a user's saved short links."""
    return crud.get_user_links(db=db, user_id=current_user.id)


@app.get("/info", response_model=schemas.InstanceInformation)
def get_instance_information(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Get the instance's information and statistics."""
    stats = crud.get_stats(db)

    return {
        "url": getenv("INSTANCE_URL", "https://unknown.vh7.uk"),
        "admin": getenv("INSTANCE_ADMIN", "admin@unknown.vh7.uk"),
        "version": VERSION,
        "stats": stats
    }


@app.get("/languages", tags=["misc"])
def get_languages() -> Response:
    """Get a list of the supported paste languages."""
    return utils.languages.languages


@app.get("/{link}", tags=["routing"])
def short_link_redirect(link: str, db: Session = Depends(get_db)) -> Response:
    """Route short links.

    URL type short links are redirected straight to the URL that was shortened.
    All other types are redirected to the web app for viewing.
    """
    short_link = crud.get_short_link(db=db, link=link)

    if short_link is None:
        raise HTTPException(status_code=404,
                            detail="Short link not found")

    if (short_link.expiry is not None and
            short_link.expiry <= datetime.utcnow()):
        raise HTTPException(status_code=404,
                            detail="The given short link has expired")

    # Default to redirecting the request to the web app
    url = urljoin(getenv("INSTANCE_APP_URL", "https://app.vh7.uk"), "/link/")
    url = urljoin(url, link)

    # If the short link is a URL, redirect straight to that instead of the
    # web app
    if short_link.url is not None:
        url = short_link.url.url

    return RedirectResponse(url, status_code=308)


@app.on_event("startup")
def task_startup_message() -> None:
    """Show version information on startup."""
    logger.info("Welcome to VH7 API Server (v{})".format(VERSION))


@app.on_event("startup")
@repeat_every(seconds=14400)
def task_cleanup() -> None:
    """Perform a cleanup periodically."""
    run_cleanup()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
