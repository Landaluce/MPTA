#!flask/bin/python
from app import app
from app.constants import CORPORA_UPLOAD_FOLDER, DICTIONARIES_UPLOAD_FOLDER
app.config['CORPORA_UPLOAD_FOLDER'] = CORPORA_UPLOAD_FOLDER
app.config['DICTIONARIES_UPLOAD_FOLDER'] = DICTIONARIES_UPLOAD_FOLDER
app.run(debug=True)

