#!flask/bin/python
from app import app
from WordCount import WordCount
from app.fileManager import create_tmp_folder
import os

cwd = os.getcwd()
app.config['TMP_DIRECTORY'] = cwd + "/tmp"
app.config['CORPORA_UPLOAD_FOLDER'] = cwd + "/tmp/corpora"
app.config['DICTIONARIES_UPLOAD_FOLDER'] = cwd + "/tmp/dictionaries"
create_tmp_folder()

app.config['check_all_corpora'] = 1
app.config['check_all_dictionaries'] = 1
app.config['active_corpora'] = []
app.config['active_dictionaries'] = []
app.config['obj'] = WordCount()

app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'
app.run(debug=True)
