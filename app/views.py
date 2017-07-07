from fileManager import allowed_extension, allowed_size, get_file_size, files_to_html_table, delete_tmp_folder, \
    create_tmp_folder
from flask import render_template, request, redirect, url_for, Response
from TwitterAPI import get_tweets
from werkzeug import secure_filename
from WordCount import WordCount
from app import app
import csv
import os


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def Upload():
    """
    Handles the functionality of the upload page. It uploads files to be used
    in the current session.
    :return: a render_template call.
    """
    corpus_extension_errors = ""
    corpus_size_errors = ""
    dictionary_extension_errors = ""
    dictionary_size_errors = ""
    if request.method == 'POST':
        if request.files.getlist("file[]"):
            files = request.files.getlist("file[]")
            for file in files:
                file_name = secure_filename(file.filename)
                file.save(os.path.join(app.config['TMP_DIRECTORY'], file_name))
                extension = allowed_extension(file.filename)
                size = allowed_size(os.path.join(app.config['TMP_DIRECTORY'], file_name))
                if extension and size:
                    if request.form['upload'] == "corpus":
                        os.rename(os.path.join(app.config['TMP_DIRECTORY'], file_name),
                                  os.path.join(app.config['CORPORA_UPLOAD_FOLDER'], file_name))
                        app.config['obj'].add_corpus(os.path.join(app.config['CORPORA_UPLOAD_FOLDER'], file_name))
                        app.config['active_corpora'].append("checked")
                    elif request.form['upload'] == "dictionary":
                        os.rename(os.path.join(app.config['TMP_DIRECTORY'], file_name),
                                  os.path.join(app.config['DICTIONARIES_UPLOAD_FOLDER'], file_name))
                        app.config['obj'].add_dictionary(
                            os.path.join(app.config['DICTIONARIES_UPLOAD_FOLDER'], file_name))
                        app.config['active_dictionaries'].append("checked")
                        """if len(app.config['formula']) > 0:
                            app.config['formula'][-1].append("+")
                            app.config['formula'].append([app.config['obj'].dictionaries_labels[-1], "", "", "+"])"""
                else:
                    os.remove(os.path.join(app.config['TMP_DIRECTORY'], file_name))
                    if request.form['upload'] == "corpus":
                        if not size:
                            corpus_size_errors += file.filename
                            corpus_size_errors += ", "
                        if not extension:
                            corpus_extension_errors += file.filename
                            corpus_extension_errors += ", "
                    elif request.form['upload'] == "dictionary":
                        if not size:
                            dictionary_size_errors += file.filename
                            dictionary_size_errors += ", "
                        if not extension:
                            dictionary_extension_errors += file.filename
                            dictionary_extension_errors += ", "
        elif 'search_query' and 'quantity' in request.form:
            search_query = request.form['search_query']
            quantity = request.form['quantity']
            tweets = get_tweets(search_query, int(quantity))
            default_name = search_query + "_tw_"
            count = 1

            for tweet in tweets:
                number_of_zeros = len(str(len(tweets))) - len(str(count))
                left_zeros = ""
                for i in range(number_of_zeros):
                    left_zeros += "0"
                file_name = default_name + left_zeros + str(count) + ".txt"
                count += 1
                file = open(app.config['CORPORA_UPLOAD_FOLDER'] + "/" + file_name, "w")
                file.write(tweet)
                file.close()
                app.config['obj'].add_corpus(os.path.join(app.config['CORPORA_UPLOAD_FOLDER'], file_name))
                app.config['active_corpora'].append("checked")
    corpora_sizes = []
    for filename in os.listdir(app.config['CORPORA_UPLOAD_FOLDER']):
        corpora_sizes.append(get_file_size(app.config['CORPORA_UPLOAD_FOLDER'] + "/" + filename))
    dictionaries_sizes = []
    for filename in os.listdir(app.config['DICTIONARIES_UPLOAD_FOLDER']):
        dictionaries_sizes.append(get_file_size(app.config['DICTIONARIES_UPLOAD_FOLDER'] + "/" + filename))
    return render_template("index.html",
                           title='Upload',
                           corpus_extension_errors=corpus_extension_errors[:-2],
                           corpus_size_errors=corpus_size_errors[:-2],
                           dictionary_extension_errors=dictionary_extension_errors[:-2],
                           dictionary_size_errors=dictionary_size_errors[:-2],
                           corpora=files_to_html_table(os.listdir(app.config['CORPORA_UPLOAD_FOLDER']), corpora_sizes),
                           dictionaries=files_to_html_table(os.listdir(app.config['DICTIONARIES_UPLOAD_FOLDER']),
                                                            dictionaries_sizes))


@app.route('/FileManager', methods=['GET', 'POST'])
def FileManager():
    """
    Handles the functionality of the FileManager page. Its primary role is to activate/deactivate
    specific corpora depending on the user's input.
    :return: a render_template call.
    """
    if request.method == 'POST':
        if 'corpus[]' in request.form:
            corpus = ''.join(request.form.getlist('corpus[]'))
            obj_index = 0
            count = 0
            for name in app.config['obj'].corpora_labels:
                if name == corpus:
                    obj_index = count
                count += 1
            if app.config['active_corpora'][obj_index] == "checked":
                app.config['active_corpora'][obj_index] = ""
                app.config['obj'].deactivate_corpus(obj_index)
            else:
                app.config['active_corpora'][obj_index] = "checked"
                app.config['obj'].activate_corpus(obj_index)

            temp = app.config['active_corpora'][0]
            all_same = True
            for i in range(len(app.config['active_corpora'])):
                if app.config['active_corpora'][i] != temp:
                    all_same = False
            if all_same and temp == "checked":
                app.config['check_all_corpora'] = True
            else:
                app.config['check_all_corpora'] = False

            zipped_data = zip(app.config['active_corpora'], app.config['obj'].corpora_labels,
                              sorted(os.listdir(app.config['CORPORA_UPLOAD_FOLDER'])))
            return render_template("fileManager.html",
                                   title='File Manager',
                                   zipped_data=zipped_data,
                                   check_all=app.config['check_all_corpora'],
                                   corpora=sorted(os.listdir(app.config['CORPORA_UPLOAD_FOLDER'])))
        elif 'download' in request.form:
            file_name = request.form['download']
            i = 0
            file_content = ""
            for name in app.config['obj'].corpora_names:
                if name == file_name:
                    file_content = app.config['obj'].corpora[i]
                i += 1
            return Response(file_content,
                            mimetype="text/plain",
                            headers={"Content-disposition": "attachment; filename=" + file_name})
        elif 'delete' in request.form:
            corpus = request.form['delete']
            index = 0
            count = 0
            for name in app.config['obj'].corpora_names:
                if name == corpus:
                    index = count
                count += 1
            del app.config['active_corpora'][index]
            del app.config['obj'].corpora_labels[index]
            app.config['obj'].delete_corpus(index)
            os.remove(app.config['CORPORA_UPLOAD_FOLDER'] + "/" + corpus)
        elif 'check_all' in request.form:
            if app.config['check_all_corpora']:
                for i in range(len(app.config['active_corpora'])):
                    app.config['active_corpora'][i] = ''
                    app.config['check_all_corpora'] = False
                    app.config['obj'].deactivate_corpus(i)
            else:
                for i in range(len(app.config['active_corpora'])):
                    app.config['active_corpora'][i] = "checked"
                    app.config['check_all_corpora'] = True
                    app.config['obj'].activate_corpus(i)
        elif 'label' and 'label_index' in request.form:
            new_label_list = request.form['new_label_list'].split(', ')
            for i in range(len(app.config['obj'].corpora_labels)):
                app.config['obj'].corpora_labels[i] = new_label_list[i]
    zipped_data = zip(app.config['active_corpora'], sorted(app.config['obj'].corpora_labels),
                      sorted(os.listdir(app.config['CORPORA_UPLOAD_FOLDER'])))
    return render_template("fileManager.html",
                           title='File Manager',
                           zipped_data=zipped_data,
                           check_all=app.config['check_all_corpora'],
                           corpora=sorted(os.listdir(app.config['CORPORA_UPLOAD_FOLDER'])))


@app.route('/DictionaryManager', methods=['GET', 'POST'])
def DictionaryManager():
    """
    Handles the functionality of the DictionaryManager page. Its primary role is to activate/deactivate
    specific dictionaries depending on the user's input.
    :return: a render_template call.
    """
    if request.method == 'POST':
        if 'dictionary[]' in request.form and 'label[]' not in request.form:
            dictionary = ''.join(request.form.getlist('dictionary[]'))
            index = 0
            count = 0
            for name in app.config['obj'].dictionaries_names:
                if name == dictionary:
                    index = count
                count += 1
            if app.config['active_dictionaries'][index] == "checked":
                app.config['active_dictionaries'][index] = ""
                app.config['obj'].deactivate_dictionary(index)
            else:
                app.config['active_dictionaries'][index] = "checked"
                app.config['obj'].activate_dictionary(index)
            temp = app.config['active_dictionaries'][0]
            all_checked = True
            for i in app.config['active_dictionaries']:
                if i != temp:
                    all_checked = False
            if all_checked:
                if temp == "checked":
                    app.config['check_all_dictionaries'] = True
            else:
                app.config['check_all_dictionaries'] = False
            zipped_data = zip(app.config['active_dictionaries'], app.config['obj'].dictionaries_labels,
                              sorted(os.listdir(app.config['DICTIONARIES_UPLOAD_FOLDER'])))
            return render_template("dictionaryManager.html",
                                   title='Dictionary Manager',
                                   zipped_data=zipped_data,
                                   active_dictionaries=app.config['active_dictionaries'],
                                   check_all=app.config['check_all_dictionaries'],
                                   labels=app.config['obj'].dictionaries_labels,
                                   check_all_oh=app.config['check_all_oh'],
                                   active_oh=app.config['active_oh'],
                                   dictionaries=sorted(os.listdir(app.config['DICTIONARIES_UPLOAD_FOLDER'])))
        elif 'download' in request.form:
            file_name = request.form['download']
            i = 0
            file_content = ""
            for name in app.config['obj'].dictionaries_names:
                if name == file_name:
                    file_content = app.config['obj'].dictionaries[i]
                i += 1
            file_content = ', '.join(file_content)
            return Response(
                file_content,
                mimetype="text/plain",
                headers={'Content-disposition': "attachment; filename=" + file_name})
        elif 'delete[]' in request.form:
            dictionary = request.form['delete[]']
            index = 0
            for i in range(len(app.config['obj'].dictionaries_names)):
                if app.config['obj'].dictionaries_names[i] == dictionary:
                    index = i
            app.config['obj'].delete_dictionary(index)
            if index > app.config['first_oh_index'] >= 0:
                index -= app.config['first_oh_index'] + 4
            else:
                app.config['first_oh_index'] -= 1
            del app.config['active_dictionaries'][index]
            os.remove(app.config['DICTIONARIES_UPLOAD_FOLDER'] + "/" + dictionary)
        elif 'edit' in request.form:
            file_name = request.form['edit']
            file_content = ""
            for i in range(len(app.config['obj'].dictionaries_names)):
                if app.config['obj'].dictionaries_names[i] == file_name:
                    file_content = ', '.join(app.config['obj'].dictionaries[i])
                    label = app.config['obj'].dictionaries_labels[i]
            return render_template("edit.html",
                                   title='Edit',
                                   file_name=label,
                                   active_page='DictionaryManager',
                                   file_content=file_content)
        elif 'save_filename' and 'save_content' in request.form:
            file_name = request.form['save_filename']
            file_content = request.form['save_content']
            count = 0
            index = 0
            for i in range(0, len(app.config['obj'].dictionaries_names)):
                if app.config['obj'].dictionaries_labels[i] == file_name:
                    index = count
                count += 1

            file_extension = app.config['obj'].dictionaries_extensions[index]
            app.config['obj'].dictionaries[index] = file_content
            file = open(app.config['DICTIONARIES_UPLOAD_FOLDER'] + "/" + file_name + file_extension, "w")
            file.write(file_content)
            file.close()
        elif 'check_all' in request.form:
            if app.config['check_all_dictionaries']:
                for i in range(len(app.config['active_dictionaries'])):
                    app.config['active_dictionaries'][i] = ''
                    app.config['check_all_dictionaries'] = False
                    app.config['obj'].deactivate_dictionary(i)
            else:
                for i in range(len(app.config['active_dictionaries'])):
                    app.config['active_dictionaries'][i] = "checked"
                    app.config['check_all_dictionaries'] = True
                    app.config['obj'].activate_dictionary(i)
        elif ('label[]' and 'dictionary[]' in request.form) or ('oh_label' and 'dictionary' in request.form):

            if 'label[]' in request.form:
                new_label_list = request.form['new_label_array'].split(', ')
                count = 0
                if app.config['first_oh_index'] > -1:
                    for i in range(0, app.config['first_oh_index']):
                        app.config['obj'].dictionaries_labels[i] = new_label_list[count]
                        count += 1
                    for i in range(app.config['first_oh_index'] + 4, len(app.config['obj'].dictionaries_labels)):
                        app.config['obj'].dictionaries_labels[i] = new_label_list[count]
                        count += 1
                else:
                    for i in range(len(app.config['obj'].dictionaries_labels)):
                        app.config['obj'].dictionaries_labels[i] = new_label_list[i]

            else:
                new_oh_label_list = request.form['new_oh_label_list'].split(', ')
                for i in range(4):
                    app.config['obj'].dictionaries_labels[app.config['first_oh_index'] + i] = new_oh_label_list[i]
        elif 'check_all_oh' in request.form:
            if not app.config['oh_uploaded']:
                app.config['oh_uploaded'] = True
                app.config['check_all_oh'] = True
                app.config['active_oh'] = [True, True, True, True]
                if 'opportunity' not in app.config['obj'].dictionaries_names:
                    app.config['first_oh_index'] = len(app.config['obj'].dictionaries_names)
                    app.config['obj'].add_dictionary(os.path.join(app.config['OH_UPLOAD_FOLDER'], 'Opportunity.txt'))
                if 'threat' not in app.config['obj'].corpora_names:
                    app.config['obj'].add_dictionary(os.path.join(app.config['OH_UPLOAD_FOLDER'], 'Threat.txt'))
                if 'enactment' not in app.config['obj'].corpora_names:
                    app.config['obj'].add_dictionary(os.path.join(app.config['OH_UPLOAD_FOLDER'], 'Enactment.txt'))
                if 'Org_Id' not in app.config['obj'].corpora_names:
                    app.config['obj'].add_dictionary(os.path.join(app.config['OH_UPLOAD_FOLDER'], 'Org_Identity.txt'))
            elif app.config['check_all_oh']:
                app.config['check_all_oh'] = False
                app.config['active_oh'] = [False, False, False, False]
                for i in range(0, 4):
                    app.config['obj'].deactivate_dictionary(app.config['first_oh_index'] + i)
            elif not app.config['check_all_oh']:
                app.config['check_all_oh'] = True
                app.config['active_oh'] = [True, True, True, True]
                for i in range(0, 4):
                    app.config['obj'].activate_dictionary(app.config['first_oh_index'] + i)
        elif 'oh' in request.form:
            oh = request.form['oh']
            index = 0
            for i in range(0, len(app.config['obj'].dictionaries_names)):
                if app.config['obj'].dictionaries_names[i].lower() == oh + ".txt":
                    index = i
            if not app.config['active_oh'][index - app.config['first_oh_index']]:
                app.config['active_oh'][index - app.config['first_oh_index']] = True
                app.config['obj'].activate_dictionary(index)
            elif app.config['active_oh'][index - app.config['first_oh_index']]:
                app.config['active_oh'][index - app.config['first_oh_index']] = False
                app.config['obj'].deactivate_dictionary(index)
            temp = app.config['active_oh'][0]
            all_checked = True
            for i in app.config['active_oh']:
                if i != temp:
                    all_checked = False
            if all_checked:
                if temp != "checked":
                    app.config['check_all_oh'] = False

    zipped_data = zip(app.config['active_dictionaries'], app.config['obj'].dictionaries_labels, sorted(os.listdir(app.config['DICTIONARIES_UPLOAD_FOLDER'])))
    labels = app.config['obj'].dictionaries_labels
    oh_labels = ['Oportunity', 'Threat', 'Enactment', 'Org_Identity']
    if app.config['first_oh_index'] > -1:
        labels = app.config['obj'].dictionaries_labels[:app.config['first_oh_index']] + app.config['obj'].dictionaries_labels[app.config['first_oh_index']+4:]
        labels = sorted(labels)
        zipped_data = zip(app.config['active_dictionaries'], labels, sorted(os.listdir(app.config['DICTIONARIES_UPLOAD_FOLDER'])))
        oh_labels = app.config['obj'].dictionaries_labels[app.config['first_oh_index']:app.config['first_oh_index']+4]

    return render_template("dictionaryManager.html",
                           title='Dictionary Manager',
                           zipped_data=zipped_data,
                           active_dictionaries=app.config['active_dictionaries'],
                           check_all=app.config['check_all_dictionaries'],
                           labels=labels,
                           oh_labels=oh_labels,
                           oh_index=app.config['first_oh_index'],
                           check_all_oh=app.config['check_all_oh'],
                           active_oh=app.config['active_oh'],
                           dictionaries=sorted(os.listdir(app.config['DICTIONARIES_UPLOAD_FOLDER'])))


@app.route('/Analyze', methods=['GET', 'POST'])
def Analyze():
    """
    Handles the functionality of the Analyze page. It generates a table with raw count for
    each corpus and its final score.
    :return: a render_template call.
    """
    if request.method == 'POST':
        if "results" in request.form:
            file_name = request.form['results']
            file_content = ""
            with open(app.config['TMP_DIRECTORY'] + '/results.csv', 'rb') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                for row in spamreader:
                    file_content += ', '.join(row) + '\n'
            return Response(
                file_content,
                mimetype="text/csv",
                headers={"Content-disposition": "attachment; filename=" + file_name})
        elif 'Save formula' in request.form:
            op1 = request.form.getlist('op1[]')
            quantity = request.form.getlist('quantity[]')
            op2 = request.form.getlist('op2[]')

            for i in range(len(op1) - 1):
                if op1[i] == '*':
                    op1[i] = 'x'
                if op2[i] == '*':
                    op2[i] = 'x'
                op1[i] = op1[i].encode('ascii', 'ignore')
                op2[i] = op2[i].encode('ascii', 'ignore')
                quantity[i] = quantity[i].encode('ascii', 'ignore')

            labels = []
            for label in app.config['obj'].dictionaries_labels:
                if len(label) > 18:
                    labels.append(label[:16] + "...")
                else:
                    labels.append(label)

            count = 0
            rows = []
            for i in range(len(labels)):
                if count == 3:
                    rows.append("</tr><tr>")
                    count = -1
                else:
                    rows.append("")
                count += 1
            app.config['formula'] = zip(labels, op1, quantity, op2, rows)

            app.config['tem_labels'] = labels
            app.config['op1'] = op1
            app.config['quantity'] = quantity
            app.config['op2'] = op2
            return render_template("analyze.html",
                                   zipped_data=app.config['formula'],
                                   labels=labels,
                                   title='Analyze',
                                   active_page='Analyze',
                                   corpus_count=len(app.config['obj'].corpora),
                                   dictionary_count=len(app.config['obj'].dictionaries),
                                   content=app.config['content'],
                                   active_dictionaries=app.config['obj'].active_dictionaries)
        elif 'analyze' in request.form:
            os.chdir(app.config['CORPORA_UPLOAD_FOLDER'])
            app.config['obj'].count_words()
            app.config['obj'].generate_scores(app.config['tem_labels'], app.config['op1'], app.config['quantity'],
                                              app.config['op2'])
            os.chdir(app.config['TMP_DIRECTORY'])
            app.config['content'] = "<form method='POST'><input type='hidden' name='results' type='text' value='results'><input class='button' id='download_scores' type='submit' value='Download'></form>" + app.config['obj'].to_html()
            app.config['obj'].save_to_csv()

    #if len(app.config['op1']) == 0:
    labels = []
    for label in app.config['obj'].dictionaries_labels:
        if len(label) > 18:
            labels.append(label[:16] + "...")
        else:
            labels.append(label)
    op1 = []
    quantity = []
    op2 = []

    active_dictionaries = app.config['obj'].active_dictionaries
    labels = app.config['obj'].dictionaries_labels
    for i in range(len(labels)):
        if active_dictionaries[i]:
            op1.append('x')
            quantity.append('1')
            op2.append('+')

    count = 0
    rows = []
    for i in range(len(labels)):
        if count == 3:
            rows.append("new row")
            count = -1
        else:
            rows.append("")
        count += 1
    app.config['formula'] = zip(labels, op1, quantity, op2, rows)
    app.config['tem_labels'] = labels
    app.config['op1'] = op1
    app.config['quantity'] = quantity
    app.config['op2'] = op2
    return render_template("analyze.html",
                           zipped_data=app.config['formula'],
                           labels=app.config['tem_labels'],
                           title='Analyze',
                           active_page='Analyze',
                           corpus_count=len(app.config['obj'].corpora),
                           dictionary_count=len(app.config['obj'].dictionaries),
                           content=app.config['content'],
                           active_dictionaries=app.config['obj'].active_dictionaries)


@app.route('/Reset')
def Reset():
    """
    Deletes all files uploaded and resets all variables to their default values.
    :return: a render_template call.
    """
    delete_tmp_folder()
    create_tmp_folder()
    app.config['obj'] = WordCount()
    app.config['active_corpora'] = []
    app.config['active_dictionaries'] = []
    app.config['check_all_corpora'] = True
    app.config['check_all_dictionaries'] = True
    app.config['check_all_oh'] = False
    app.config['active_oh'] = [False, False, False, False]
    app.config['oh_uploaded'] = False
    app.config['tem_labels'] = []
    app.config['op1'] = []
    app.config['quantity'] = []
    app.config['op2'] = []
    app.config['formula'] = []
    app.config['content'] = ""
    return redirect(url_for('Upload'))
