from fastapi import FastAPI, Depends, File, UploadFile
from fastapi.exceptions import HTTPException
from sqlalchemy import schema
from sqlalchemy.orm import Session
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


SECRET_KEY = "f8afd7fcece3aa4d3ae21216c9a3b76be631fd2febc0dabd1dbb2402a77dbd7f"
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
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
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
    if not current_user.active or not current_user.confirmed:
        raise HTTPException(status_code=401,
                            detail="Disabled or unconfimed user")
    return current_user


def get_optional_active_user(current_user: schemas.User =
                             Depends(get_current_user)):
    if current_user is None:
        return None
    if not current_user.active or not current_user.confirmed:
        raise HTTPException(status_code=401,
                            detail="Disabled or unconfimed user")
    return current_user


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/shorten", response_model=schemas.ShortLink)
def create_shorten(url: schemas.Url, db: Session = Depends(get_db),
                   user: Optional[schemas.User] =
                   Depends(get_optional_active_user)):
    return crud.create_shorten(db=db, url=url, user=user)


@app.post("/paste", response_model=schemas.ShortLink)
def create_paste(paste: schemas.PasteCreate, db: Session = Depends(get_db),
                 user: Optional[schemas.User] =
                 Depends(get_optional_active_user)):
    return crud.create_paste(db=db, paste=paste, user=user)


@app.post("/upload", response_model=schemas.ShortLink)
def create_upload(file: UploadFile = File(...), db: Session = Depends(get_db),
                  user: Optional[schemas.User] =
                  Depends(get_optional_active_user)):
    return crud.create_upload(db=db, filename=file.filename, file=file.file,
                              mimetype=file.content_type, user=user)


@app.get("/info/{short_link_id}", response_model=schemas.ShortLink)
def get_short_link(short_link_id: str, db: Session = Depends(get_db)):
    return crud.get_short_link(db=db, short_link_id=short_link_id)


@app.post("/user", response_model=schemas.User, tags=["users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@app.get("/users/me", response_model=schemas.User, tags=["users"])
def get_user(current_user: schemas.User = Depends(get_required_user)):
    return current_user


@app.get("/users/me/links", response_model=List[schemas.ShortLink],
         tags=["users"])
def get_user_links(db: Session = Depends(get_db), current_user: schemas.User =
                   Depends(get_required_active_user)):
    return crud.get_user_links(db=db, user_id=current_user.id)


@app.post("/token", response_model=schemas.Token, tags=["users"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email},
                                       expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/info", response_model=schemas.InstanceInformation)
def get_instance_information():
    return {
        "url": "https://example.com",
        "admin": "admin@example.com",
        "version": "1.0.0",
        "stats": {
            "shortened_links": 1,
            "uploaded_files": 3,
            "pasted_code": 2,
            "total": 6
        }
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
