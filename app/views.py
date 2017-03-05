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
    obj = app.config['obj']
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
                obj.add_corpus(os.path.join(app.config['CORPORA_UPLOAD_FOLDER'], filename),filename)
            elif request.form['upload'] == "dictionary":
                file.save(os.path.join(app.config['DICTIONARIES_UPLOAD_FOLDER'], filename))
                obj.add_list(os.path.join(app.config['DICTIONARIES_UPLOAD_FOLDER'], filename),filename)
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
        file_name = request.form['corpus']
        obj = app.config['obj']
        i = 0
        file_content = ""
        print obj.corpora_names
        print obj.corpora
        for name in obj.corpora_names:
            if name == file_name:
                file_content = obj.corpora[i]
            i += 1
        return Response(
            file_content,
            mimetype="text/plain",
            headers={"Content-disposition":
                         "attachment; filename=" + file_name})
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
        file_name = request.form['dictionary']
        obj = app.config['obj']
        i = 0
        file_content = ""
        print obj.list_names
        print obj.lists_to_use
        for name in obj.list_names:
            if name == file_name:
                file_content = obj.lists_to_use[i]
            i += 1
        return Response(
            file_content,
            mimetype="text/plain",
            headers={"Content-disposition":
                         "attachment; filename=" + file_name})
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
    obj = app.config['obj']
    os.chdir(CORPORA_UPLOAD_FOLDER)
    obj.count_words()
    # obj.display()
    print len(str(obj.corpora[0]).split(" "))
    content = obj.to_html() + "<p><input type=submit value='Download Results'></p>"
    return render_template("index.html",
                           title='Analyze',
                           content=content)


@app.route('/Reset')
def Reset():
    delete_tmp_folder()
    create_tmp_folder()
    obj = app.config['obj']
    del obj
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
