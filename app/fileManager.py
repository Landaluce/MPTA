from app import app
import math
import shutil
import os


def allowed_file(file_name):
    """
    Checks if the given file name extension is allowed
    :param file_name: String.
    :return: Boolean.
    """
    file_extension = file_name.rsplit('.', 1)[1]
    if file_extension in app.config['ALLOWED_EXTENSIONS']:
        return True
    else:
        return False


def create_tmp_folder():
    """
    Creates tmp and its subdirectories dictionaries and corpora.
    :return: Nothing.
    """
    if not os.path.exists(app.config['CORPORA_UPLOAD_FOLDER']):
        os.makedirs(app.config['CORPORA_UPLOAD_FOLDER'])
    if not os.path.exists(app.config['DICTIONARIES_UPLOAD_FOLDER']):
        os.makedirs(app.config['DICTIONARIES_UPLOAD_FOLDER'])


def delete_tmp_folder():
    """
        Deletes tmp and its subdirectories dictionaries and corpora.
        :return: Nothing.
        """
    if os.path.exists(app.config['TMP_DIRECTORY']):
        shutil.rmtree(app.config['TMP_DIRECTORY'])


def humanize_file_size(size):
    """
    Converts size from bytes to a human readable unit.
    :param size: size in bytes (Integer)
    :return: Size in human readable unit.
    """
    size = abs(size)
    if size == 0:
        return "0 bytes"
    units = ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    p = math.floor(math.log(size, 2)/10)
    return "%.1f %s" % (size / math.pow(1000, p), units[int(p)])


def get_file_size(file_path):
    """
    Gets the size of the given file
    :param file_path: path of a file (String)
    :return: size of file (Float)
    """
    size = os.stat(file_path).st_size
    return humanize_file_size(size)


def get_file_extension(file_path):
    """
    Gets the extension of the given file
    :param file_path: path of a file (String)
    :return: extension of file (Float)
    """
    extension = os.path.splitext(file_path)[1]
    return extension


def strip_file_extension(file_name):
    """
    Strinps the extension of the given file_name
    :param file_name: name of a file (String)
    :return: name (String)
    """
    name = os.path.splitext(file_name)[0]
    return name


def file_to_html(file_name, size):
    """
    Generates a HTML table of for a given file_name an size
    :param file_name: name of a file (String)
    :param size: size of the file (Float)
    :return: a HTML table
    """
    result = """<table id="file_to_html">
    <tr><td align="center"> """ + file_name + """</td></tr>
    <tr><td align="center"> Size: """ + str(size) + """</td></tr>
    </table>"""
    return result


def files_to_html_table(file_names, sizes):
    """
    Generates an HTML table containing all the given files and their sizes
    :param file_names: List of files (List of Strings)
    :param sizes: List of sizes (List of Floats)
    :return: a HTML table
    """
    result = "<table id='files_to_html_table'>\n"
    for i in range(len(file_names)):
        if i % 2 == 1:
            result += "<td>" + file_to_html(file_names[i], sizes[i]) + "</td>"
        else:
            if i != 0:
                result += "</tr>"
            result += "\n<tr>\n<td>" + file_to_html(file_names[i], sizes[i]) + "</td>\n"
    result += "\n</tr>\n</table>"
    return result
