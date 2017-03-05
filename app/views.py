from app import app
from flask import render_template, request, redirect, url_for, Response
from werkzeug import secure_filename
from fileManager import *
import glob
import os
from WordCount import WordCount


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    try:
        app.config['obj']
    except:
        app.config['obj'] = WordCount()
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if request.form['upload'] == "corpus":
                file.save(os.path.join(app.config['CORPORA_UPLOAD_FOLDER'], filename))
            elif request.form['upload'] == "dictionary":
                file.save(os.path.join(app.config['DICTIONARIES_UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
    content = """
        <!doctype html>
        <h1>Upload new File</h1>
        <form action="" method=post enctype=multipart/form-data>
          <input type="hidden" name="upload" value="corpus">
          <p><input type=file name=file>
             <input type=submit value=Upload>
        </form>
        <p>%s</p>
        """ % "<br>".join(os.listdir(app.config['CORPORA_UPLOAD_FOLDER'], ))
    content += """
        <h1>Upload new Dictionary</h1>
        <form action="" method=post enctype=multipart/form-data>
          <input type="hidden" name="upload" value="dictionary">
          <p><input type=file name=file>
             <input type=submit value=Upload>
        </form>
        <p>%s</p>
        """ % "<br>".join(os.listdir(app.config['DICTIONARIES_UPLOAD_FOLDER'], ))
    return render_template("index.html",
                           title='Home',
                           content=content)


@app.route('/FileManager', methods=['GET', 'POST'])
def FileManager():
    if request.method == 'POST':
        return Response(
            mimetype="text/csv",
            headers={"Content-disposition":
                         "attachment; filename=" + request.form['corpus']})
    content = "<table>"
    count = 0
    for corpus in os.listdir(app.config['CORPORA_UPLOAD_FOLDER']):
        content += "<tr>" \
                   "<td><input type='checkbox' name='corpus" + str(count) + "' value='val' checked></td>" \
                   "<td>" + corpus + "</td>" \
                   "<td>" \
                   "<form method='POST'><input type='hidden' name='corpus' type='text' value='" + corpus + "'>" \
                   "<input id='my_submit' type='submit' value='Download'>" \
                   "</form>" \
                   "</td>" \
                   "<td><input type=submit value='Delete'></td>" \
                   "</tr>"
        count += 1
    content += "</table>"
    return render_template("index.html",
                           title='File Manager',
                           content=content
                           )


@app.route('/DictionaryManager', methods=['GET', 'POST'])
def DictionaryManager():
    if request.method == 'POST':
        return Response(
            mimetype="text/csv",
            headers={"Content-disposition":
                         "attachment; filename=" + request.form['dictionary']})
    content = "<table>"
    count = 0
    for dictionary in os.listdir(app.config['DICTIONARIES_UPLOAD_FOLDER']):
        content += "<tr>" \
                   "<td><input type='checkbox' name='corpus" + str(dictionary) + "' value='val' checked></td>" \
                   "<td>" + dictionary + "</td>" \
                   "<td><input type=submit value='Edit'></td>" \
                   "<td>" \
                   "<form method='POST'><input type='hidden' name='dictionary' type='text' value='" + dictionary + "'>" \
                   "<input id='my_submit' type='submit' value='Download'>" \
                   "</form>" \
                   "</td>" \
                   "<td><input type=submit value='Delete'></td>" \
                   "</tr>"
        count += 1
    content += "</table>"
    return render_template("index.html",
                           title='Dictionary Manager',
                           content=content
                           )


@app.route('/Analyze')
def Analyze():
    obj = WordCount()
    os.chdir(CORPORA_UPLOAD_FOLDER)
    for file in glob.glob("*"):
        obj.add_corpus(CORPORA_UPLOAD_FOLDER + "/" + file)
    os.chdir(DICTIONARIES_UPLOAD_FOLDER)
    for file in glob.glob("*"):
        with open(file, 'r') as myfile:
            dictionary = myfile.read().replace('\n', '').split(", ")
            obj.add_list(dictionary, file)
    obj.count_words()
    # obj.display()
    content = obj.to_html() + "<p><input type=submit value='Download Results'></p>"
    return render_template("index.html",
                           title='Analyze',
                           content=content)


@app.route('/Reset')
def Reset():
    delete_tmp_folder()
    create_tmp_folder()
    return redirect(url_for('index'))


@app.route("/getPlotCSV/<id>")
def getPlotCSV(id):
    # with open("outputs/Adjacency.csv") as fp:
    #     csv = fp.read()
    print id
    csv = '1,2,3\n4,5,6\n'
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                     "attachment; filename=myplot.csv"})
