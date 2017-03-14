from app import app
from flask import render_template, request, redirect, url_for, Response, session
from werkzeug import secure_filename
from fileManager import *
import os
from WordCount import WordCount, read_txt
import csv


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    active_corpora = app.config['active_corpora']
    active_dictionaries = app.config['active_dictionaries']
    try:
        obj = app.config['obj']
    except:
        app.config['obj'] = WordCount()
        obj = app.config['obj']
    if request.method == 'POST':
        files = request.files.getlist("file[]")
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                if request.form['upload'] == "corpus":
                    file.save(os.path.join(app.config['CORPORA_UPLOAD_FOLDER'], filename))
                    obj.add_corpus(os.path.join(app.config['CORPORA_UPLOAD_FOLDER'], filename), filename)
                    active_corpora.append("checked")
                elif request.form['upload'] == "dictionary":
                    file.save(os.path.join(app.config['DICTIONARIES_UPLOAD_FOLDER'], filename))
                    obj.add_dictionary(os.path.join(app.config['DICTIONARIES_UPLOAD_FOLDER'], filename), filename)
                    active_dictionaries.append("checked")
        app.config['active_corpora'] = active_corpora
        app.config['active_dictionaries'] = active_dictionaries
        return redirect(url_for('index'))

    corpora_sizes = []
    for filename in os.listdir(app.config['CORPORA_UPLOAD_FOLDER']):
        corpora_sizes.append(get_file_size(app.config['CORPORA_UPLOAD_FOLDER'] + "/" + filename))
    dictionaries_sizes = []
    for filename in os.listdir(app.config['DICTIONARIES_UPLOAD_FOLDER']):
        dictionaries_sizes.append(get_file_size(app.config['DICTIONARIES_UPLOAD_FOLDER'] + "/" + filename))


    content = """
        <table id="index_table" >
            <tr>
                <td align="center">
                    <h1>Upload new File</h1>
                </td>
                <td align="center">
                    <h1>Upload new Dictionary</h1>
                </td>
            <tr>
                <td align="center">
                    <form action="index" method="post" enctype="multipart/form-data">
                        <input type="hidden" name="upload" value="corpus">
                        <input id="uploadbutton" type="file" multiple="multiple" name="file[]" onchange="this.form.submit();">
                        <div id="dragndrop"><p>or drop files here</p></div>
                    </form>
                </td>
                <td align="center">
                    <form action="index" method="post" enctype="multipart/form-data">
                        <input type="hidden" name="upload" value="dictionary">
                        <input id="uploadbutton" type="file" multiple="multiple" name="file[]" onchange="this.form.submit();">
                        <div id="dragndrop"><p>or drop files here</p></div>
                    </form>
                </td>
            </tr>
            <tr>
                <td align="center" valign="top">"""
    content += files_to_html_table(os.listdir(app.config['CORPORA_UPLOAD_FOLDER']),corpora_sizes)
    content += """
                </td>
                <td align="center" valign="top">"""
    content += files_to_html_table(os.listdir(app.config['DICTIONARIES_UPLOAD_FOLDER']),dictionaries_sizes)
    content += """
                </td>
            </tr>
        </table>
    """

    return render_template("index.html",
                           title='Home',
                           content=content)

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

@app.route('/FileManager', methods=['GET', 'POST'])
def FileManager():
    if request.method == 'POST':
        obj = app.config['obj']
        active_corpora = app.config['active_corpora']
        try:
            index = int(request.form['index'].encode("utf-8"))
            corpus = request.form['corpus'].encode("utf-8")
            obj_index = 0
            count = 0
            for name in obj.corpora_names:
                if name == corpus:
                    obj_index = count
                count += 1
            if active_corpora[index] == "checked":
                active_corpora[index] = ""
                app.config['obj'].deactivate_corpus(obj_index)
            else:
                active_corpora[index] = "checked"
                app.config['obj'].activate_corpus(obj_index)
            return render_template("fileManager.html",
                                   title='File Manager',
                                   active_corpora=active_corpora,
                                   corpora=os.listdir(app.config['CORPORA_UPLOAD_FOLDER']))
        except:
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
    return render_template("fileManager.html",
                           title='File Manager',
                           active_corpora=app.config['active_corpora'],
                           corpora=os.listdir(app.config['CORPORA_UPLOAD_FOLDER']))


@app.route('/DictionaryManager', methods=['GET', 'POST'])
def DictionaryManager():
    if request.method == 'POST':
        obj = app.config['obj']
        active_dictionaries = app.config['active_dictionaries']
        try:
            index = int(request.form['index'].encode("utf-8"))
            dictionary = request.form['dictionary'].encode("utf-8")
            obj_index = 0
            count = 0
            for name in obj.dictionaries_names:
                if name == dictionary:
                    obj_index = count
                count += 1
            if active_dictionaries[index] == "checked":
                active_dictionaries[index] = ""
                app.config['obj'].deactivate_dictionary(obj_index)
            else:
                active_dictionaries[index] = "checked"
                app.config['obj'].activate_dictionary(obj_index)
            app.config['active_dictionaries'] = active_dictionaries
            print app.config['active_dictionaries']
            return render_template("dictionaryManager.html",
                                   title='File Manager',
                                   actiactive_dictionaries=active_dictionaries,
                                   dictionaries=os.listdir(app.config['DICTIONARIES_UPLOAD_FOLDER']))
        except:
            try:
                file_name = request.form['download']
                i = 0
                file_content = ""
                for name in obj.dictionaries_names:
                    if name == file_name:
                        file_content = read_txt(obj.dictionaries[i])
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
                    obj.delete_dictionary(dictionary_index)
                    os.remove(DICTIONARIES_UPLOAD_FOLDER + "/" + file_name)
                    return render_template("dictionaryManager.html",
                                           title='File Manager',
                                           active_dictionaries=app.config['active_dictionaries'],
                                           dictionaries=os.listdir(app.config['DICTIONARIES_UPLOAD_FOLDER']))
                except:
                    try:
                        file_name = request.form['edit']
                        file_content = ""
                        for i in range(len(obj.dictionaries_names)):
                            if obj.dictionaries_names[i] == file_name:
                                file_content = read_txt(obj.dictionaries[i])
                        return render_template("edit.html",
                                               title='Edit',
                                               file_name=file_name,
                                               file_content=file_content)
                    except:
                        # bad Post request
                        pass
    return render_template("dictionaryManager.html",
                           title='File Manager',
                           active_dictionaries=app.config['active_dictionaries'],
                           dictionaries=os.listdir(app.config['DICTIONARIES_UPLOAD_FOLDER']))


@app.route('/Analyze', methods=['GET', 'POST'])
def Analyze():
    if request.method == 'POST':
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

    obj.generate_scores()
    os.chdir(TMP_DIRECTORY)
    content = obj.to_html() + "<p><form method='POST'><input type='hidden' name='results' type='text' value='results'>" \
                   "<input class='button' id='download_button' type='submit' value='Download'>" \
                   "</form></p>"
    #obj.display()
    obj.save_to_csv()
    return render_template("index.html",
                           title='Analyze',
                           content=content)


@app.route('/Reset')
def Reset():
    session.clear()
    delete_tmp_folder()
    create_tmp_folder()
    obj = app.config['obj']
    del app.config['obj']
    return redirect(url_for('index'))

