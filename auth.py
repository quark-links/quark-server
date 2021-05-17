"""Methods for helping with authentication."""
from fastapi.security.oauth2 import OAuth2
from fastapi.openapi.models import OAuthFlows
from jose import jwt
from fastapi import HTTPException
from typing import Dict, Optional
import requests
from logzero import logger
import json
from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import Request
from config import settings


class CustomOAuth2(OAuth2):
    def __init__(self, scheme_name: Optional[str] = None,
                 scopes: Optional[Dict[str, str]] = None,
                 auto_error: bool = False):
        if not scopes:
            scopes = {}
        flows = OAuthFlows(implicit={
                "authorizationUrl": settings.auth.authorization_endpoint
            })
        super().__init__(flows=flows, scheme_name=scheme_name,
                         auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            return None
        return param


class AuthError(HTTPException):
    """General FastAPI authentication error."""
    def __init__(self, detail: str = "Could not validate credentials"):
        """Create a new authentication error.

        Args:
            detail (str, optional): The error detail. Defaults to "Could not
                validate credentials".
        """
        super().__init__(status_code=401, detail=detail,
                         headers={"WWW-Authenticate": "Bearer"})


def parse_header(header: Optional[str]) -> Optional[str]:
    """Parse the contents of the authorization header.

    Args:
        header (Optional[str]): The authorization header contents.

    Returns:
        Optional[str]: The bearer token container in the header.
    """
    if header is None:
        return None

    return header.replace("Bearer ", "")


def parse_token(token: str) -> Dict:
    """Parse and validate a JWT bearer token.

    Args:
        token (str): The token the parse and validate.

    Returns:
        Dict: The contents of the JWT token.
    """
    try:
        with open("jwks.json", "r") as f:
            jwks = json.load(f)
    except Exception as err:
        logger.error("Error loading JWKS: %s", err)
        raise HTTPException(status_code=500)

    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.JWTError:
        raise AuthError()

    rsa_key = None
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = key
            break

    if rsa_key is None:
        logger.warning("Auth Error: The token's RSA key was not found")
        raise AuthError

    try:
        return jwt.decode(token, rsa_key, algorithms=settings.auth.algorithms,
                          audience=settings.auth.audience,
                          issuer=settings.auth.issuer)
    except Exception as ex:
        logger.warning("Auth Error: %s", ex)
        raise AuthError


def get_profile(token: str) -> Optional[Dict]:
    """Get a user's profile from the external OAuth server.

    Args:
        token (str): The user's token to get the profile of.

    Returns:
        Optional[Dict]: The user's profile.
    """
    try:
        r = requests.get(settings.auth.user_info_endpoint, headers={
            "Authorization": f"Bearer {token}"
        })
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logger.error("Error getting auth keys: %s", err)
        raise HTTPException(status_code=500)

    profile = r.json()

    return profile
