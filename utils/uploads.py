"""Upload handling functions."""
from tempfile import SpooledTemporaryFile
import os


def get_uploads_folder():
    """Get the path to the folder for upload storage.

    Returns:
        str: The path to the upload folder.
    """
    default_upload_path = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), "../uploads")
    return os.getenv("UPLOAD_FOLDER", default_upload_path)


def save_upload(file: SpooledTemporaryFile, filename: str):
    """Save a given uploaded file into the upload folder.

    Args:
        file (SpooledTemporaryFile): The uploaded file.
        filename (str): The name to store the file as.
    """
    uploads_folder = get_uploads_folder()
    if not os.path.exists(uploads_folder):
        os.makedirs(uploads_folder)

    with open(os.path.join(uploads_folder, filename), "wb") as f:
        f.writelines(file.readlines())


def get_path(filename: str):
    """Get the path to a file.

    Args:
        filename (str): The name of the file to get the path of.

    Returns:
        str: The path of the file.
    """
    uploads_folder = get_uploads_folder()
    path = os.path.join(uploads_folder, filename)
    return path
