#!flask/bin/python
from app import app
from WordCount import WordCount
from app.constants import CORPORA_UPLOAD_FOLDER, DICTIONARIES_UPLOAD_FOLDER
from app.fileManager import create_tmp_folder

create_tmp_folder()
app.config['active_corpora'] = []
app.config['obj'] = WordCount()
app.config['CORPORA_UPLOAD_FOLDER'] = CORPORA_UPLOAD_FOLDER
app.config['DICTIONARIES_UPLOAD_FOLDER'] = DICTIONARIES_UPLOAD_FOLDER
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'
app.run(debug=True)
