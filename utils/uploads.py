"""Upload handling functions."""
from tempfile import SpooledTemporaryFile
import os
from config import settings


def save_upload(file: SpooledTemporaryFile, filename: str) -> None:
    """Save a given uploaded file into the upload folder.

    Args:
        file (SpooledTemporaryFile): The uploaded file.
        filename (str): The name to store the file as.
    """
    uploads_folder = settings.uploads.folder
    if not os.path.exists(uploads_folder):
        os.makedirs(uploads_folder)

    with open(os.path.join(uploads_folder, filename), "wb") as f:
        f.writelines(file.readlines())


def get_path(filename: str) -> str:
    """Get the path to a file.

    Args:
        filename (str): The name of the file to get the path of.

    Returns:
        str: The path of the file.
    """
    uploads_folder = settings.uploads.folder
    path = os.path.join(uploads_folder, filename)
    return path
