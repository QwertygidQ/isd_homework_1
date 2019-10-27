import tarfile
import zipfile
import os
from pathlib import Path
from . import app


def create_archive(filename: str, archive_type: str) -> str:
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    if not os.path.isfile(filepath):
        raise RuntimeError("File is missing")

    archive_type = archive_type.lower()
    filename_stem = Path(filename).resolve().stem
    archive_name = filename_stem + "." + archive_type
    archive_path = os.path.join(app.config["UPLOAD_FOLDER"], archive_name)

    if "tar" in archive_type:
        tarfile_options = {
            "tar": "w",
            "tar.gz": "w:gz",
            "tar.bz2": "w:bz2",
            "tar.xz": "w:xz",
        }

        if archive_type not in tarfile_options:
            raise RuntimeError("Unsupported tar archive type")

        try:
            with tarfile.open(archive_path, tarfile_options[archive_type]) as archive:
                archive.add(filepath, arcname=filename)
        except Exception:
            raise RuntimeError("Failed to create an archive")

        return archive_name
    elif archive_type == "zip":
        try:
            with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as archive:
                archive.write(filepath, arcname=filename)
        except Exception:
            raise RuntimeError("Failed to create an archive")

        return archive_name
    else:
        raise RuntimeError("Unsupported archive type")
