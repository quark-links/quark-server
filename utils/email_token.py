from itsdangerous import URLSafeTimedSerializer
from db import User
from config import SECRET_KEY, TOKEN_SALT, TOKEN_MAX_AGE


def _get_serializer():
    return URLSafeTimedSerializer(SECRET_KEY)


def generate_confirmation_token(user: User):
    """Generate a new email confirmation token.

    Args:
        user (User): The user to create a confirmation token for.

    Returns:
        str: The confirmation token to be sent in an email.
    """
    return _get_serializer().dumps((user.id, user.email), salt=TOKEN_SALT)


def verify_confirmation_token(token):
    """Verify an email confirmation token.

    Args:
        token (str): The confirmation token from the user.

    Returns:
        User: The user that the token belongs to.
    """
    serializer = _get_serializer()

    # Get the user ID and email from the token
    try:
        user_id, user_email = serializer.loads(
            token,
            salt=TOKEN_SALT,
            max_age=TOKEN_MAX_AGE
        )
    except Exception:
        print("Invalid token")
        return None

    # Check that the token is valid for the user's email.
    user = User.query.filter_by(id=user_id).first()

    if user is None or user.email != user_email:
        print("Invalid user or email")
        return None

    return user