from app import app
import math
import shutil
import os


def allowed_file(filename):
    file_extension = filename.rsplit('.', 1)[1]
    if file_extension in app.config['ALLOWED_EXTENSIONS']:
        return True
    else:
        return False


def create_tmp_folder():
    if not os.path.exists(app.config['CORPORA_UPLOAD_FOLDER']):
        os.makedirs(app.config['CORPORA_UPLOAD_FOLDER'])
    if not os.path.exists(app.config['DICTIONARIES_UPLOAD_FOLDER']):
        os.makedirs(app.config['DICTIONARIES_UPLOAD_FOLDER'])


def delete_tmp_folder():
    if os.path.exists(app.config['TMP_DIRECTORY']):
        shutil.rmtree(app.config['TMP_DIRECTORY'])


def humanize_file_size(size):
    size = abs(size)
    if size == 0:
        return "0 bytes"
    units = ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    p = math.floor(math.log(size, 2)/10)
    return "%.1f %s" % (size / math.pow(1000, p), units[int(p)])


def get_file_size(filepath):
    size = os.stat(filepath).st_size
    return humanize_file_size(size)


def get_file_type(filepath):
    type = os.path.splitext(filepath)[1]
    return type


def strip_file_extension(filepath):
    name = os.path.splitext(filepath)[0]
    return name


def file_to_html(filename, size):
    result = """<table id="file_to_html">
    <tr><td align="center"> """ + filename + """</td></tr>
    <tr><td align="center"> Size: """ + str(size) + """</td></tr>
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
