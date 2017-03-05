from app import app
from flask import render_template, request, redirect, url_for
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
        print 2
    except:
        app.config['obj'] = WordCount()
        print 1
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if request.form['upload'] == "corpus":
                print "corpus"
                file.save(os.path.join(app.config['CORPORA_UPLOAD_FOLDER'], filename))
            elif request.form['upload'] == "dictionary":
                print "dic"
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


@app.route('/FileManager')
def FileManager():
    content = "<table>"
    count = 0
    for corpus in os.listdir(app.config['CORPORA_UPLOAD_FOLDER']):
        content += "<tr>" \
                        "<td><input type='checkbox' name='corpus" + str(count) +"' value='val' checked></td>" \
                        "<td>" + corpus + "</td>" \
                        "<td><input type=submit value='Download'></td>" \
                        "<td><input type=submit value='Delete'></td>" \
                   "</tr>"
        count += 1
    content += "</table>"
    return render_template("index.html",
                           title='File Manager',
                           content=content
                           )


@app.route('/DictionaryManager')
def DictionaryManager():
    content = "<table>"
    count = 0
    for corpus in os.listdir(app.config['CORPORA_UPLOAD_FOLDER']):
        content += "<tr>" \
                        "<td><input type='checkbox' name='corpus" + str(count) +"' value='val' checked></td>" \
                        "<td>" + corpus + "</td>" \
                        "<td><input type=submit value='Edit'></td>" \
                        "<td><input type=submit value='Download'></td>" \
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
    obj.add_list(obj.threat, "thread")
    obj.add_list(obj.enactment, "enactment")
    obj.add_list(obj.opportunity, "opportunity")
    obj.add_list(obj.org_iden, "org_iden")
    obj.upload_list("/home/alvaro/Desktop/COMP-401/Dictionaries/my_dict.csv", "my_dict")
    obj.count_words()
    obj.display()
    content = obj.to_html() + "<p><input type=submit value='Download Results'></p>"
    return render_template("index.html",
                           content=content)

@app.route('/Reset')
def Reset():
    delete_tmp_folder()
    create_tmp_folder()
    return redirect(url_for('index'))
