from app.constants import *
import shutil
import os


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def create_tmp_folder():
    if not os.path.exists(CORPORA_UPLOAD_FOLDER):
        os.makedirs(CORPORA_UPLOAD_FOLDER)
    if not os.path.exists(DICTIONARIES_UPLOAD_FOLDER):
        os.makedirs(DICTIONARIES_UPLOAD_FOLDER)


def delete_tmp_folder():
    if os.path.exists(TMP_DIRECTORY):
        shutil.rmtree(TMP_DIRECTORY)