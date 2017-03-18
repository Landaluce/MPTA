from fileManager import allowed_file, get_file_size, files_to_html_table, delete_tmp_folder, create_tmp_folder
from flask import render_template, request, redirect, url_for, Response, session
from werkzeug import secure_filename
from WordCount import WordCount
from app import app
import csv
import os


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def Upload():
    try:
        active_corpora = app.config['active_corpora']
    except:
        app.config['active_corpora'] = []
        active_corpora = []
    try:
        active_dictionaries = app.config['active_dictionaries']
    except:
        app.config['active_dictionaries'] = []
        active_dictionaries = []
    try:
        obj = app.config['obj']
    except:
        app.config['obj'] = WordCount()
        obj = app.config['obj']
    if request.method == 'POST':
        files = request.files.getlist("file[]")
        for file in files:
            file_extension = allowed_file(file.filename)
            if file_extension != "":
                filename = secure_filename(file.filename)
                if request.form['upload'] == "corpus":
                    file.save(os.path.join(app.config['CORPORA_UPLOAD_FOLDER'], filename))
                    obj.add_corpus(os.path.join(app.config['CORPORA_UPLOAD_FOLDER'], filename))
                    active_corpora.append("checked")
                elif request.form['upload'] == "dictionary":
                    file.save(os.path.join(app.config['DICTIONARIES_UPLOAD_FOLDER'], filename))
                    obj.add_dictionary(os.path.join(app.config['DICTIONARIES_UPLOAD_FOLDER'], filename))#, filename)
                    active_dictionaries.append("checked")
        app.config['active_corpora'] = active_corpora
        app.config['active_dictionaries'] = active_dictionaries
        return redirect(url_for('Upload'))

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
                    <div id="upload_title">File Upload</div>
                    <div id="formats">Formats Supported: .txt, .csv, .docx</div>
                </td>
                <td align="center">
                    <div id="upload_title">Dictionary Upload</div>
                    <div id="formats">Formats Supported: .txt, .csv, .docx</div>
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
                           title='Upload',
                           content=content)


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
                                   labels=obj.corpora_labels,
                                   corpora=sorted(os.listdir(app.config['CORPORA_UPLOAD_FOLDER'])))
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
                    active_corpora = app.config['active_corpora']
                    index = int(request.form['del_index'].encode("utf-8"))
                    del active_corpora[index]
                    del obj.corpora_labels[index]
                    app.config['active_corpora'] = active_corpora
                    obj.delete_corpus(index)
                    os.remove(app.config['CORPORA_UPLOAD_FOLDER'] + "/" + file_name)
                except:
                    try:
                        check_all = request.form['check_all']
                        active_corpora = app.config['active_corpora']
                        check_all_corpora = app.config['check_all_corpora']
                        if check_all_corpora == 1:
                            for i in range(len(active_corpora)):
                                active_corpora[i] = ''
                                check_all_corpora = 0
                                app.config['obj'].deactivate_corpus(i)
                        else:
                            for i in range(len(active_corpora)):
                                active_corpora[i] = "checked"
                                check_all_corpora = 1
                                app.config['obj'].activate_corpus(i)
                        app.config['active_corpora'] = active_corpora
                        app.config['check_all_corpora'] = check_all_corpora
                    except:
                        try:
                            label = request.form['label']
                            label_index = int(request.form['label_index'])
                            obj.corpora_labels[label_index] = label
                            app.config['obj'] = obj
                        except:
                            pass
    return render_template("fileManager.html",
                           title='File Manager',
                           active_corpora=app.config['active_corpora'],
                           check_all=app.config['check_all_corpora'],
                           labels=app.config['obj'].corpora_labels,
                           corpora=sorted(os.listdir(app.config['CORPORA_UPLOAD_FOLDER'])))


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
            print "check"
            return render_template("dictionaryManager.html",
                                   title='File Manager',
                                   actiactive_dictionaries=active_dictionaries,
                                   labels=app.config['obj'].dictionaries_labels,
                                   dictionaries=sorted(os.listdir(app.config['DICTIONARIES_UPLOAD_FOLDER'])))
        except:
            try:
                file_name = request.form['download']
                i = 0
                file_content = ""
                for name in obj.dictionaries_names:
                    if name == file_name:
                        file_content = ", ".join(obj.dictionaries[i])
                    i += 1

                return Response(
                    file_content,
                    mimetype="text/plain",
                    headers={"Content-disposition":
                                 "attachment; filename=" + file_name})
            except:
                try:
                    file_name = request.form['delete']
                    index = int(request.form['del_index'].encode("utf-8"))
                    del active_dictionaries[index]
                    del obj.dictionaries_labels[index]
                    app.config['active_corpora'] = active_dictionaries
                    obj.delete_dictionary(index)
                    os.remove(app.config['DICTIONARIES_UPLOAD_FOLDER'] + "/" + file_name)
                    return render_template("dictionaryManager.html",
                                           title='File Manager',
                                           active_dictionaries=app.config['active_dictionaries'],
                                           labels=app.config['obj'].dictionaries_labels,
                                           dictionaries=sorted(os.listdir(app.config['DICTIONARIES_UPLOAD_FOLDER'])))
                except:
                    try:
                        file_name = request.form['edit']
                        file_content = ""
                        for i in range(len(obj.dictionaries_names)):
                            if obj.dictionaries_names[i] == file_name:
                                file_content = ", ".join(obj.dictionaries[i])
                                label = obj.dictionaries_labels[i]
                        return render_template("edit.html",
                                               title='Edit',
                                               file_name=label,
                                               active_page='DictionaryManager',
                                               file_content=file_content)
                    except:
                        try:
                            file_name = request.form['save_filename']
                            file_content = request.form['save_content']
                            file = open(app.config['DICTIONARIES_UPLOAD_FOLDER'] + "/" + file_name, "w")
                            file.write(file_content)
                            file.close()
                        except:
                            try:
                                check_all = request.form['check_all']
                                active_dictionaries = app.config['active_dictionaries']
                                check_all_dictionaries = app.config['check_all_dictionaries']
                                if check_all_dictionaries == 1:
                                    for i in range(len(active_dictionaries)):
                                        active_dictionaries[i] = ''
                                        check_all_dictionaries = 0
                                        app.config['obj'].deactivate_dictionary(i)
                                else:
                                    for i in range(len(active_dictionaries)):
                                        active_dictionaries[i] = "checked"
                                        check_all_dictionaries = 1
                                        app.config['obj'].activate_dictionary(i)
                                app.config['active_dictionaries'] = active_dictionaries
                                app.config['check_all_dictionaries'] = check_all_dictionaries
                            except:
                                try:
                                    label = request.form['label']
                                    label_index = int(request.form['label_index'])
                                    obj.dictionaries_labels[label_index] = label
                                    app.config['obj'] = obj
                                except:
                                    pass
    return render_template("dictionaryManager.html",
                           title='File Manager',
                           active_dictionaries=app.config['active_dictionaries'],
                           check_all=app.config['check_all_dictionaries'],
                           labels=app.config['obj'].dictionaries_labels,
                           dictionaries=sorted(os.listdir(app.config['DICTIONARIES_UPLOAD_FOLDER'])))


@app.route('/Analyze', methods=['GET', 'POST'])
def Analyze():
    if request.method == 'POST':
        file_name = request.form['results']
        file_content = ""
        with open(app.config['TMP_DIRECTORY'] + '/results.csv', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in spamreader:
                file_content += ', '.join(row) + '\n'
        return Response(
            file_content,
            mimetype="text/csv",
            headers={"Content-disposition":
                         "attachment; filename=" + file_name})
    obj = app.config['obj']
    os.chdir(app.config['CORPORA_UPLOAD_FOLDER'])
    obj.count_words()
    obj.generate_scores()
    os.chdir(app.config['TMP_DIRECTORY'])
    content = obj.to_html() + "<form method='POST'><input type='hidden' name='results' type='text' value='results'>" \
                   "<input class='button' id='download_scores' type='submit' value='Download'>" \
                   "</form>"
    #obj.display()
    obj.save_to_csv()
    return render_template("analyze.html",
                           title='Analyze',
                           active_page='Analyze',
                           corpus_count=len(obj.corpora),
                           dictionary_count=len(obj.dictionaries),
                           content=content)


@app.route('/Reset')
def Reset():
    session.clear()
    delete_tmp_folder()
    create_tmp_folder()
    del app.config['obj']
    del app.config['active_corpora']
    del app.config['active_dictionaries']
    app.config['check_all_corpora'] = 1
    app.config['check_all_dictionaries'] = 1
    return redirect(url_for('Upload'))
