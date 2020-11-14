from tempfile import SpooledTemporaryFile
import os


def get_uploads_folder():
    default_upload_path = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), "uploads")
    return os.getenv("UPLOAD_FOLDER", default_upload_path)


def save_upload(file: SpooledTemporaryFile, filename: str):
    uploads_folder = get_uploads_folder()
    if not os.path.exists(uploads_folder):
        os.makedirs(uploads_folder)

    with open(os.path.join(uploads_folder, filename), "wb") as f:
        f.writelines(file.readlines())
