import pytest
import requests
import tarfile

from ..config import host, port


BASE_URI = f"http://{host}:{str(port)}/"
URI = BASE_URI + "convert/"


@pytest.fixture
def temp_file(tmpdir):
    TEMP_FILENAME = "temp.txt"
    TEMP_CONTENT = "Hello world!"

    path = tmpdir.join(TEMP_FILENAME)
    path.write(TEMP_CONTENT)

    return TEMP_FILENAME, str(path)


def test_success(tmpdir, temp_file):
    TEMP_ARCHIVENAME = "archive.tar.gz"
    TEMP_ARCHIVEPATH = str(tmpdir.join(TEMP_ARCHIVENAME))

    TEMP_FILENAME, TEMP_FILEPATH = temp_file

    with open(TEMP_FILEPATH, "rb") as file:
        request = requests.post(URI + "TaR.gZ", files={"file": file}, timeout=10)
        assert request.status_code == 200

        with open(TEMP_ARCHIVEPATH, "wb") as archive:
            archive.write(request.content)

        with tarfile.open(TEMP_ARCHIVEPATH, "r:gz") as archive:
            assert TEMP_FILENAME in archive.getnames()


def test_archive_types(temp_file):
    archives = ["zip", "tar", "tar.gz", "tar.bz2", "tar.xz"]

    _, TEMP_FILEPATH = temp_file
    with open(TEMP_FILEPATH, "rb") as file:
        for archive in archives:
            request = requests.post(URI + archive, files={"file": file}, timeout=10)
            assert request.status_code == 200


def test_wrong_uri():
    request = requests.post(BASE_URI, timeout=10)
    assert request.status_code == 404

    request = requests.post(BASE_URI + "abcd", timeout=10)
    assert request.status_code == 404

    request = requests.post(URI, timeout=10)
    assert request.status_code == 404


def test_not_post():
    request = requests.get(URI + "tar.gz", timeout=10)
    assert request.status_code == 405


def test_no_file():
    request = requests.post(URI + "tar.gz", timeout=10)
    assert request.status_code == 400


def test_unsupported_filetype(temp_file):
    _, TEMP_FILEPATH = temp_file
    with open(TEMP_FILEPATH, "rb") as file:
        request = requests.post(URI + "abcd", files={"file": file}, timeout=10)
        assert request.status_code == 400
