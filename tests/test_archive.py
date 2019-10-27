import os
import pytest
import shutil
import tarfile
import zipfile

from ..config import Config
from ..app.archive import create_archive


UPLOAD_FOLDER = Config.UPLOAD_FOLDER


@pytest.fixture
def temp_file():
    TEMP_FILENAME = "temp.txt"
    TEMP_FILEPATH = os.path.join(UPLOAD_FOLDER, TEMP_FILENAME)
    TEMP_CONTENT = "Hello world!"

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    with open(TEMP_FILEPATH, "w") as file:
        file.write(TEMP_CONTENT)

    return TEMP_FILENAME


@pytest.fixture(autouse=True)
def teardown():
    yield  # Don't do anything before the tests

    if os.path.exists(UPLOAD_FOLDER):
        shutil.rmtree(UPLOAD_FOLDER)


class TestSuccess:
    def __assert_success_tar(self, temp_file, archive_type):
        tarfile_options = {
            "tar": "r",
            "tar.gz": "r:gz",
            "tar.bz2": "r:bz2",
            "tar.xz": "r:xz",
        }

        archive_name = create_archive(temp_file, archive_type)
        with tarfile.open(
            os.path.join(UPLOAD_FOLDER, archive_name), tarfile_options[archive_type]
        ) as archive:
            assert temp_file in archive.getnames()

    def test_tar(self, temp_file):
        self.__assert_success_tar(temp_file, "tar")

    def test_tar_gz(self, temp_file):
        self.__assert_success_tar(temp_file, "tar.gz")

    def test_tar_bz2(self, temp_file):
        self.__assert_success_tar(temp_file, "tar.bz2")

    def test_tar_xz(self, temp_file):
        self.__assert_success_tar(temp_file, "tar.xz")

    def test_zip(self, temp_file):
        archive_name = create_archive(temp_file, "zip")

        with zipfile.ZipFile(
            os.path.join(UPLOAD_FOLDER, archive_name), "r", zipfile.ZIP_DEFLATED
        ) as archive:
            assert temp_file in archive.namelist()


def test_missing_path():
    with pytest.raises(RuntimeError):
        create_archive("dasdasdiaj", "zip")


def test_unsupported_tar(temp_file):
    with pytest.raises(RuntimeError):
        create_archive(temp_file, "tar.ab")


def test_unsupported_archive_type(temp_file):
    with pytest.raises(RuntimeError):
        create_archive(temp_file, "abcd")
