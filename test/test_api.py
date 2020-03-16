"""Tests for the API."""

import os
import tempfile
import pytest
import app
from werkzeug.datastructures import FileStorage
import db


@pytest.fixture
def client():
    """Create a new Flask test client."""
    with app.app.test_client() as client:
        yield client


@pytest.mark.dependency()
def test_shorten__2xx(client, request):
    """Test the shorten endpoint with a valid URL."""
    response = client.post("/api/shorten", json={
        "url": "https://vh7.uk/"
    })
    json_data = response.get_json()
    request.config.cache.set("short_link", json_data["link"])
    assert response.status_code in range(200, 300)


@pytest.mark.dependency()
def test_shorten__invalid_url__non_2xx(client, request):
    """Test the shorten endpoint with an invalid URL."""
    response = client.post("/api/shorten", json={
        "url": "ahh"
    })
    assert response.status_code not in range(200, 300)


def test_paste__no_language__non_2xx(client):
    """Test the paste endpoint with no language set."""
    response = client.post("/api/paste", json={
        "code": "Hello World!"
    })
    assert response.status_code not in range(200, 300)


def test_paste__2xx(client):
    """Test the paste endpoint with a valid paste."""
    response = client.post("/api/paste", json={
        "code": "Hello World!",
        "language": "plaintext"
    })
    assert response.status_code in range(200, 300)


def test_upload__1mb__2xx(client):
    """Test the upload endpoint with a valid 1mb file."""
    # Create a new 1mb temporary file
    new_file, filename = tempfile.mkstemp()
    with open(filename, "w") as f:
        f.seek((1024 * 1024) - 1)
        f.write("\0")

    # Load the temporary file into a FileStorage object
    req_file = FileStorage(stream=open(filename, "rb"), filename="test.txt",
                           content_type="text/plain")
    # Create a new POST request
    response = client.post("/api/upload", data={
        "file": req_file
    }, content_type="multipart/form-data")

    # Close and delete the file
    os.close(new_file)
    os.unlink(filename)

    # Make assertion
    assert response.status_code in range(200, 300)


def test_upload__512mb__too_big__413(client):
    """Test the upload endpoint with a 512mb file that is too large."""
    # Create a new 512mb temporary file
    new_file, filename = tempfile.mkstemp()
    with open(filename, "w") as f:
        f.seek((1024 * 1024 * 512) - 1)
        f.write("\0")

    # Load the temporary file into a FileStorage object
    req_file = FileStorage(stream=open(filename, "rb"), filename="test.txt",
                           content_type="text/plain")
    # Create a new POST request
    response = client.post("/api/upload", data={
        "file": req_file
    }, content_type="multipart/form-data")

    # Close and delete the file
    os.close(new_file)
    os.unlink(filename)

    # Make assertion
    assert response.status_code == 413


def test_upload__file_saves(client):
    """Test the upload endpoint with a valid file to check that it is saved."""
    # Create a new temporary file
    new_file, filename = tempfile.mkstemp()
    with open(filename, "w") as f:
        f.write("VH7 TEST FILE")

    # Load the temporary file into a FileStorage object
    req_file = FileStorage(stream=open(filename, "rb"),
                           filename="test_file.txt",
                           content_type="text/plain")
    # Create a new POST request
    client.post("/api/upload", data={
        "file": req_file
    }, content_type="multipart/form-data")

    # Close and delete the file
    os.close(new_file)
    os.unlink(filename)

    # Find the upload object and get the stored filename
    upload = db.Upload.query.filter_by(original_filename="test_file.txt"
                                       ).first()
    pytest.assume(upload is not None)
    store_path = upload.filename
    pytest.assume(store_path is not None)

    # Get the full path of the file
    full_store_path = os.path.join(app.app.config["UPLOAD_FOLDER"], store_path)

    # Make assertion
    assert os.path.exists(full_store_path)


def test_info__invalid_link__404(client):
    """Test the info endpoint with an invalid link."""
    response = client.get("/api/info/AA")
    assert response.status_code == 404


@pytest.mark.dependency(depends=["test_shorten__2xx"])
def test_info__valid_link__2xx(client, request):
    """Test the info endpoint with a valid link."""
    short_link = request.config.cache.get("short_link", None)
    response = client.get("/api/info{}".format(short_link))
    assert response.status_code in range(200, 300)
