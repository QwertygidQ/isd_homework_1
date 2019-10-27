import os


host = "0.0.0.0"
port = 8080
debug = False

base_folder = os.path.abspath(os.path.dirname(__file__))


class Config:
    UPLOAD_FOLDER = os.path.join(base_folder, "uploads/")
    ALLOWED_ARCHIVES = set(["zip", "tar", "tar.gz", "tar.bz2", "tar.xz"])
