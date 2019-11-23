import os
from flask import request, send_from_directory, send_file
from werkzeug.utils import secure_filename
from . import app
from .archive import create_archive


@app.route('/')
def root():
    return send_file('../html/index.html'), 200


@app.route("/convert/<filetype>", methods=["POST"])
def convert(filetype):
    if "file" not in request.files:
        return "No file in POST", 400

    file = request.files["file"]
    if file is None or file.filename == "":
        return "Filename is empty", 400

    filetype = filetype.lower()
    if filetype not in app.config["ALLOWED_ARCHIVES"]:
        return "Unsupported archive type", 400

    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])

    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    try:
        archive_name = create_archive(filename, filetype.lower())
    except NotImplementedError as err:
        return err.args[0], 501
    except RuntimeError as err:
        return err.args[0], 500

    archive_path = os.path.join(app.config["UPLOAD_FOLDER"], archive_name)
    if not os.path.isfile(archive_path):
        return "Archive file is missing", 404

    return send_from_directory(app.config["UPLOAD_FOLDER"], archive_name), 200
