from utils.uploads import get_path
from fastapi import FastAPI, Depends, File, UploadFile
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from starlette.responses import FileResponse, RedirectResponse
import uvicorn

import crud
from crud import get_user_by_email
import schemas
from database import SessionLocal
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import pbkdf2_sha256
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware
from database import hashids
from os import getenv
from urllib.parse import urljoin


SECRET_KEY = getenv("JWT_KEY", "keyboardcat")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 43200


app = FastAPI(title="VH7",
              description=("A free and open source URL shortening, file "
                           "sharing and pastebin service."),
              version="1.0.0", openapi_tags=[
                  {
                      "name": "users",
                      "description": ("Operations with users. The **login** "
                                      "logic is also here.")
                  }
              ])
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def authenticate_user(db: Session, username: str, password: str):
    db_user = crud.get_user_by_email(db=db, email=username)
    if not db_user:
        return False
    if not pbkdf2_sha256.verify(password, db_user.password):
        return False
    return db_user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(db: Session = Depends(get_db),
                     token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=401,
                                          detail=("Could not validate "
                                                  "credentials"),
                                          headers={"WWW-Authenticate":
                                                   "Bearer"})

    if token is None:
        return None

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db=db, email=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def get_required_user(current_user: schemas.User = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=401,
                            detail="Authentication is required")
    return current_user


def get_required_active_user(current_user: schemas.User =
                             Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=401,
                            detail="Authentication is required")
    if not current_user.active:  # or not current_user.confirmed:
        raise HTTPException(status_code=401,
                            detail="Disabled or unconfimed user")
    return current_user


def get_optional_active_user(current_user: schemas.User =
                             Depends(get_current_user)):
    if current_user is None:
        return None
    if not current_user.active:  # or not current_user.confirmed:
        raise HTTPException(status_code=401,
                            detail="Disabled or unconfimed user")
    return current_user


@app.get("/")
def web_app():
    """Redirect to the web app."""
    return RedirectResponse(getenv("INSTANCE_APP_URL", "https://app.vh7.uk"),
                            status_code=308)


@app.post("/shorten", response_model=schemas.ShortLink,
          response_model_exclude={"id"})
def create_shorten(url: schemas.Url, db: Session = Depends(get_db),
                   user: Optional[schemas.User] =
                   Depends(get_optional_active_user)):
    """Shorten a URL into a short link."""
    return crud.create_shorten(db=db, url=url, user=user)


@app.post("/paste", response_model=schemas.ShortLink,
          response_model_exclude={"id"})
def create_paste(paste: schemas.PasteCreate, db: Session = Depends(get_db),
                 user: Optional[schemas.User] =
                 Depends(get_optional_active_user)):
    """Save code to a short link."""
    return crud.create_paste(db=db, paste=paste, user=user)


@app.post("/upload", response_model=schemas.ShortLink,
          response_model_exclude={"id"})
def create_upload(file: UploadFile = File(...), db: Session = Depends(get_db),
                  user: Optional[schemas.User] =
                  Depends(get_optional_active_user)):
    """Upload a file to a short link."""
    return crud.create_upload(db=db, filename=file.filename, file=file.file,
                              mimetype=file.content_type, user=user)


@app.get("/info/{short_link_id}", response_model=schemas.ShortLink,
         response_model_exclude={"id"})
def short_link_info(short_link_id: str, db: Session = Depends(get_db)):
    """Get information on a given short link."""
    try:
        decoded_id = hashids.decode(short_link_id)[0]
    except IndexError:
        raise HTTPException(status_code=404,
                            detail="Short link not found")

    short_link = crud.get_short_link(db=db, short_link_id=decoded_id)

    if short_link is not None:
        return short_link
    else:
        raise HTTPException(status_code=404,
                            detail="Short link not found")


@app.get("/download/{short_link_id}")
def short_link_download(short_link_id: str, db: Session = Depends(get_db)):
    """Download the file from a given short link (only for uploads)."""
    try:
        decoded_id = hashids.decode(short_link_id)[0]
    except IndexError:
        raise HTTPException(status_code=404,
                            detail="Short link not found")

    short_link = crud.get_short_link(db=db, short_link_id=decoded_id)

    if short_link is None:
        raise HTTPException(status_code=404,
                            detail="Short link not found")

    if short_link.upload is None:
        raise HTTPException(status_code=404,
                            detail="The given short link is not a file")

    if short_link.upload.filename is None:
        raise HTTPException(status_code=404,
                            detail="The given short link has expired")

    return FileResponse(get_path(short_link.upload.filename),
                        filename=short_link.upload.original_filename,
                        media_type=short_link.upload.mimetype)


@app.post("/user", response_model=schemas.User, tags=["users"],
          response_model_exclude={"id"})
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create a new user account."""
    return crud.create_user(db=db, user=user)


@app.get("/users/me", response_model=schemas.User, tags=["users"],
         response_model_exclude={"id"})
def get_user(current_user: schemas.User = Depends(get_required_user)):
    """Get the logged in user details."""
    return current_user


@app.patch("/users/me", tags=["users"], response_model=schemas.User,
           response_model_exclude={"id"})
def update_user(new_data: schemas.UserUpdate, db: Session = Depends(get_db),
                current_user: schemas.User = Depends(get_required_user)):
    """Update a user's details."""
    return crud.update_user(db=db, user=current_user, new_user=new_data)


@app.get("/users/me/links", response_model=List[schemas.ShortLink],
         tags=["users"], response_model_exclude={"id"})
def get_user_links(db: Session = Depends(get_db), current_user: schemas.User =
                   Depends(get_required_active_user)):
    """Get a user's saved short links."""
    return crud.get_user_links(db=db, user_id=current_user.id)


@app.post("/token", response_model=schemas.Token, tags=["users"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):
    """Authenticate with a user's username and password to receive a token for
    use with the API.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    if not user.active:  # or not user.confirmed:
        raise HTTPException(status_code=401,
                            detail=("You must have an active account before "
                                    "logging in"),
                            headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email},
                                       expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/info", response_model=schemas.InstanceInformation)
def get_instance_information(db: Session = Depends(get_db)):
    """Get the instance's information and statistics."""
    stats = crud.get_stats(db)

    return {
        "url": getenv("INSTANCE_URL", "https://unknown.vh7.uk"),
        "admin": getenv("INSTANCE_ADMIN", "admin@unknown.vh7.uk"),
        "version": "1.0.0",
        "stats": stats
    }


@app.get("/{short_link_id}")
def short_link_redirect(short_link_id: str, db: Session = Depends(get_db)):
    """Route short links. URL type short links are redirected straight to the
    URL that was shortened. All other types are redirected to the web app for
    viewing.
    """
    try:
        decoded_id = hashids.decode(short_link_id)[0]
    except IndexError:
        raise HTTPException(status_code=404,
                            detail="Short link not found")

    short_link = crud.get_short_link(db=db, short_link_id=decoded_id)

    if short_link is None:
        raise HTTPException(status_code=404,
                            detail="Short link not found")

    # Default to redirecting the request to the web app
    url = urljoin(getenv("INSTANCE_APP_URL", "https://app.vh7.uk"), "/link/")
    url = urljoin(url, short_link_id)

    # If the short link is a URL, redirect straight to that instead of the
    # web app
    if short_link.url is not None:
        url = short_link.url.url

    return RedirectResponse(url, status_code=308)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
