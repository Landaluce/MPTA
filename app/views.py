from app import app
from flask import render_template, request, redirect, url_for, Response
from werkzeug import secure_filename
from fileManager import *
import glob
import os
from WordCount import WordCount, read_txt
import csv


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    obj = app.config['obj']
    try:
        app.config['obj']
    except:
        app.config['obj'] = WordCount()
    if request.method == 'POST':
        files = request.files.getlist("file[]")
        for file in files:
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
        <form action="index" method="post" enctype="multipart/form-data">
          <input type="hidden" name="upload" value="corpus">
          <input type="file" multiple="multiple" name="file[]">
          <input type="submit" value="Upload">
        </form>
        <p>%s</p>
        """ % "<br>".join(os.listdir(app.config['CORPORA_UPLOAD_FOLDER'], ))
    content += """
        <h1>Upload new Dictionary</h1>
        <form action="index" method="post" enctype="multipart/form-data">
                <input type="hidden" name="upload" value="dictionary">
                <input type="file" multiple="multiple" name="file[]">
                <input type="submit" value="Upload">
        </form>
        <p>%s</p>
        """ % "<br>".join(os.listdir(app.config['DICTIONARIES_UPLOAD_FOLDER'], ))
    return render_template("index.html",
                           title='Home',
                           content=content)


@app.route('/FileManager', methods=['GET', 'POST'])
def FileManager():
    if request.method == 'POST':
        obj = app.config['obj']
        try:
            file_name = request.form['download']
            i = 0
            file_content = ""
            for name in obj.corpora_names:
                if name == file_name:
                    file_content = obj.corpora[i]
                i += 1
            return Response(
                file_content,
                mimetype="text/plain",
                headers={"Content-disposition":
                             "attachment; filename=" + file_name})
        except:
            try:
                file_name = request.form['delete']
                i = 0
                corpus_index = 0
                for name in obj.corpora_names:
                    if name == file_name:
                        corpus_index = i
                    i += 1
                obj.delete_corpus(corpus_index)
                os.remove(CORPORA_UPLOAD_FOLDER + "/" + file_name)
            except:
                # bad Post request
                pass

    content = "<table>"
    count = 0
    for corpus in os.listdir(app.config['CORPORA_UPLOAD_FOLDER']):
        content += "<tr>" \
                   "<td><input type='checkbox' name='corpus" + str(count) + "' value='val' checked></td>" \
                   "<td>" + corpus + "</td>" \
                   "<td>" \
                   "<form method='POST'><input type='hidden' name='download' type='text' value='" + corpus + "'>" \
                   "<input id='my_submit' type='submit' value='Download'>" \
                   "</form>" \
                   "</td>" \
                   "<td>" \
                   "<form method='POST'><input type='hidden' name='delete' type='text' value='" + corpus + "'>" \
                   "<input id='my_submit' type='submit' value='Delete'>" \
                   "</form>" \
                   "</td>" \
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
        obj = app.config['obj']
        try:
            file_name = request.form['download']
            i = 0
            file_content = ""
            for name in obj.list_names:
                if name == file_name:
                    file_content = read_txt(obj.lists_to_use[i])
                i += 1
            return Response(
                file_content,
                mimetype="text/plain",
                headers={"Content-disposition":
                             "attachment; filename=" + file_name})
        except:
            try:
                file_name = request.form['delete']
                i = 0
                dictionary_index = 0
                for name in obj.corpora_names:
                    if name == file_name:
                        dictionary_index = i
                    i += 1
                obj.delete_corpus(dictionary_index)
                os.remove(DICTIONARIES_UPLOAD_FOLDER + "/" + file_name)
            except:
                try:
                    file_name = request.form['edit']
                    print "edit"
                except:
                    # bad Post request
                    pass
            print(request.form)
            for dictionary in os.listdir(app.config['DICTIONARIES_UPLOAD_FOLDER']):

                if not request.form.get("use_dictionary" + str(dictionary)):
                    print "not use", dictionary
    content = "<table>"
    count = 0
    for dictionary in os.listdir(app.config['DICTIONARIES_UPLOAD_FOLDER']):
        content += "<tr>" \
                   "<td><form method='POST'><input type='checkbox' name='use_dictionary' value='" + str(dictionary) + "' checked><form></td>" \
                   "<td>" + dictionary + "</td>" \
                   "<td>" \
                   "<form method='POST'><input type='hidden' name='edit' type='text' value='" + dictionary + "'>" \
                   "<input id='my_submit' type='submit' value='Edit'>" \
                   "</form>" \
                   "</td>" \
                   "<td>" \
                   "<form method='POST'><input type='hidden' name='download' type='text' value='" + dictionary + "'>" \
                   "<input id='my_submit' type='submit' value='Download'>" \
                   "</form>" \
                   "</td>" \
                   "<td>" \
                   "<form method='POST'><input type='hidden' name='delete' type='text' value='" + dictionary + "'>" \
                   "<input id='my_submit' type='submit' value='Delete'>" \
                   "</form>" \
                   "</td>" \
                   "</tr>"
        count += 1
    content += "</table>"
    return render_template("index.html",
                           title='Dictionary Manager',
                           content=content
                           )


@app.route('/Analyze', methods=['GET', 'POST'])
def Analyze():
    if request.method == 'POST':
        print "post"
        file_name = request.form['results']
        file_content = ""
        with open(TMP_DIRECTORY + '/results.csv', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in spamreader:
                file_content += ', '.join(row) + '\n'
        return Response(
            file_content,
            mimetype="text/csv",
            headers={"Content-disposition":
                         "attachment; filename=" + file_name})
    obj = app.config['obj']
    os.chdir(CORPORA_UPLOAD_FOLDER)
    obj.count_words()
    obj.display()

    obj.generate_scores()
    os.chdir(TMP_DIRECTORY)
    obj.save_to_csv()
    content = obj.to_html() + "<p><form method='POST'><input type='hidden' name='results' type='text' value='results'>" \
                   "<input id='my_submit' type='submit' value='Download'>" \
                   "</form></p>"
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

