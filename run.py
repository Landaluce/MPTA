#!flask/bin/python
from app.fileManager import create_tmp_folder
from WordCount import WordCount
from app import app
import os

cwd = os.getcwd()
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'csv', 'docx'}
app.config['TMP_DIRECTORY'] = cwd + "/tmp"
app.config['CORPORA_UPLOAD_FOLDER'] = cwd + "/tmp/corpora"
app.config['DICTIONARIES_UPLOAD_FOLDER'] = cwd + "/tmp/dictionaries"
create_tmp_folder()
app.config['OH_UPLOAD_FOLDER'] = cwd + "/OrganizationalHardiness"
app.config['check_all_corpora'] = True
app.config['check_all_dictionaries'] = True
app.config['check_all_oh'] = False
app.config['active_corpora'] = []
app.config['active_dictionaries'] = []
app.config['active_oh'] = [False, False, False, False]
app.config['obj'] = WordCount()
app.config['oh_uploaded'] = False
app.config['tem_labels'] = []
app.config['op1'] = []
app.config['quantity'] = []
app.config['op2'] = []
app.config['formula'] = []
app.config['content'] = ''
app.config['first_oh_index'] = -1
app.run(debug=False)
