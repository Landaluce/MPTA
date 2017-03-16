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


def get_file_size(filepath):
    size = os.stat(filepath).st_size  # in bytes
    return size


def get_file_type(filepath):
    type = os.path.splitext(filepath)[1]
    return type


def file_to_html(filename, size):
    result = """<table id="file_to_html">
    <tr><td align="center"> """ + filename + """</td></tr>
    <tr><td align="center"> Size: """ + str(size) + """ bytes </td></tr>
    </table>"""
    return result


def files_to_html_table(filenames, sizes):
    result = "<table id='files_to_html_table'>\n"
    for i in range(len(filenames)):
        if i % 2 == 1:
            result += "<td>" + file_to_html(filenames[i], sizes[i]) + "</td>"
        else:
            if i != 0:
                result += "</tr>"
            result += "\n<tr>\n<td>" + file_to_html(filenames[i], sizes[i]) + "</td>\n"
    result += "\n</tr>\n</table>"
    return result
