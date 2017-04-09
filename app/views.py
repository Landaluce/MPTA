from fileManager import allowed_extension, allowed_size, get_file_size, files_to_html_table, delete_tmp_folder, create_tmp_folder
from flask import render_template, request, redirect, url_for, Response
from werkzeug import secure_filename
from WordCount import WordCount
from TwitterAPI import get_tweets, scrub_tweets
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
                        os.rename(os.path.join(app.config['TMP_DIRECTORY'], file_name), os.path.join(app.config['CORPORA_UPLOAD_FOLDER'], file_name))
                        app.config['obj'].add_corpus(os.path.join(app.config['CORPORA_UPLOAD_FOLDER'], file_name))
                        app.config['active_corpora'].append("checked")
                    elif request.form['upload'] == "dictionary":
                        os.rename(os.path.join(app.config['TMP_DIRECTORY'], file_name), os.path.join(app.config['DICTIONARIES_UPLOAD_FOLDER'], file_name))
                        app.config['obj'].add_dictionary(os.path.join(app.config['DICTIONARIES_UPLOAD_FOLDER'], file_name))
                        app.config['active_dictionaries'].append("checked")
                        if len(app.config['formula']) > 0:
                            app.config['formula'][-1].append("+")
                            app.config['formula'].append([app.config['obj'].dictionaries_labels[-1], "", "", "+"])
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
            tweets = tweets[:int(quantity)]
            tw_text = []
            for tweet in tweets:
                tw_text.append(tweet.text)
            tw_texts = scrub_tweets(tw_text)
            default_name = search_query + "_tw_"
            count = 1

            for tweet in tw_texts:
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
                           dictionaries=files_to_html_table(os.listdir(app.config['DICTIONARIES_UPLOAD_FOLDER']), dictionaries_sizes))


@app.route('/FileManager', methods=['GET', 'POST'])
def FileManager():
    """
    Handles the functionality of the FileManager page. Its primary role is to activate/deactivate
    specific corpora depending on the user's input.
    :return: a render_template call.
    """
    if request.method == 'POST':
        if 'index' and 'corpus' in request.form:
            index = int(request.form['index'].encode("utf-8"))
            corpus = request.form['corpus'].encode("utf-8")
            obj_index = 0
            count = 0
            for name in app.config['obj'].corpora_names:
                if name == corpus:
                    obj_index = count
                count += 1
            if app.config['active_corpora'][index] == "checked":
                app.config['active_corpora'][index] = ""
                app.config['obj'].deactivate_corpus(obj_index)
            else:
                app.config['active_corpora'][index] = "checked"
                app.config['obj'].activate_corpus(obj_index)

            temp = app.config['active_corpora'][0]
            all_chacked = True
            for i in app.config['active_corpora']:
                if i != temp:
                    all_chacked = False
            if all_chacked:
                if temp == "checked":
                    app.config['check_all_corpora'] = True
            else:
                app.config['check_all_corpora'] = False
            return render_template("fileManager.html",
                                   title='File Manager',
                                   check_all=app.config['check_all_corpora'],
                                   active_corpora=app.config['active_corpora'],
                                   labels=app.config['obj'].corpora_labels,
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
                            headers={"Content-disposition":"attachment; filename=" + file_name})
        elif 'delete' and 'del_index' in request.form:
            file_name = request.form['delete']
            index = int(request.form['del_index'].encode("utf-8"))
            del app.config['active_corpora'][index]
            del app.config['obj'].corpora_labels[index]
            app.config['obj'].delete_corpus(index)
            os.remove(app.config['CORPORA_UPLOAD_FOLDER'] + "/" + file_name)
        elif 'check_all' in request.form:
            if app.config['check_all_corpora'] == True:
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
            new_label_list = request.form['new_label_list'].split()
            for i in range(len(app.config['obj'].corpora_labels)):
                app.config['obj'].corpora_labels[i] = new_label_list[i]
    return render_template("fileManager.html",
                           title='File Manager',
                           active_corpora=app.config['active_corpora'],
                           check_all=app.config['check_all_corpora'],
                           labels=app.config['obj'].corpora_labels,
                           corpora=sorted(os.listdir(app.config['CORPORA_UPLOAD_FOLDER'])))


@app.route('/DictionaryManager', methods=['GET', 'POST'])
def DictionaryManager():
    """
    Handles the functionality of the DictionaryManager page. Its primary role is to activate/deactivate
    specific dictionaries depending on the user's input.
    :return: a render_template call.
    """
    if request.method == 'POST':
        if 'index' and 'dictionary' in request.form:
            index = int(request.form['index'].encode("utf-8"))
            dictionary = request.form['dictionary'].encode("utf-8")
            obj_index = 0
            count = 0
            for name in app.config['obj'].dictionaries_names:
                if name == dictionary:
                    obj_index = count
                count += 1
            if app.config['active_dictionaries'][index] == "checked":
                app.config['active_dictionaries'][index] = ""
                app.config['obj'].deactivate_dictionary(obj_index)
            else:
                app.config['active_dictionaries'][index] = "checked"
                app.config['obj'].activate_dictionary(obj_index)

            temp = app.config['active_dictionaries'][0]
            all_chacked = True
            for i in app.config['active_dictionaries']:
                if i != temp:
                    all_chacked = False
            if all_chacked:
                if temp == "checked":
                    app.config['check_all_dictionaries'] = True
            else:
                app.config['check_all_dictionaries'] = False
            return render_template("dictionaryManager.html",
                                   title='Dictionary Manager',
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

            return Response(
                file_content,
                mimetype="text/plain",
                headers={"Content-disposition":
                             "attachment; filename=" + file_name})
        elif 'delete' and 'del_index' in request.form:
            file_name = request.form['delete']
            index = int(request.form['del_index'].encode("utf-8"))
            del app.config['active_dictionaries'][index]
            del app.config['obj'].dictionaries_labels[index]
            app.config['obj'].delete_dictionary(index)
            os.remove(app.config['DICTIONARIES_UPLOAD_FOLDER'] + "/" + file_name)
            return render_template("dictionaryManager.html",
                                   title='Dictionary Manager',
                                   active_dictionaries=app.config['active_dictionaries'],
                                   labels=app.config['obj'].dictionaries_labels,
                                   check_all_oh=app.config['check_all_oh'],
                                   active_oh=app.config['active_oh'],
                                   dictionaries=sorted(os.listdir(app.config['DICTIONARIES_UPLOAD_FOLDER'])))
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
            if app.config['check_all_dictionaries'] == True:
                for i in range(len(app.config['active_dictionaries'])):
                    app.config['active_dictionaries'][i] = ''
                    app.config['check_all_dictionaries'] = False
                    app.config['obj'].deactivate_dictionary(i)
            else:
                for i in range(len(app.config['active_dictionaries'])):
                    app.config['active_dictionaries'][i] = "checked"
                    app.config['check_all_dictionaries'] = True
                    app.config['obj'].activate_dictionary(i)
        elif 'label' and 'label_index' in request.form:
            label = request.form['label']
            label_index = int(request.form['label_index'])
            app.config['obj'].dictionaries_labels[label_index] = label
        elif 'check_all_oh' in request.form:
            first_oh_index = 0
            for i in range(0, len(app.config['obj'].dictionaries_names)):
                if app.config['obj'].dictionaries_names[i] == "Opportunity.txt":
                    if app.config['obj'].dictionaries_names[i + 1] == "Threat.txt" and \
                                    app.config['obj'].dictionaries_names[i + 2] == "Enactment.txt" and \
                                    app.config['obj'].dictionaries_names[i + 3] == "Org_Identity.txt":
                        first_oh_index = i
            if app.config['oh_uploaded'] == False:
                app.config['oh_uploaded'] = True
                app.config['check_all_oh'] = True
                app.config['active_oh'] = [True, True, True, True]
                if 'opportunity' not in app.config['obj'].corpora_names:
                    app.config['obj'].add_dictionary(os.path.join(app.config['OH_UPLOAD_FOLDER'], 'Opportunity.txt'))
                if 'threat' not in app.config['obj'].corpora_names:
                    app.config['obj'].add_dictionary(os.path.join(app.config['OH_UPLOAD_FOLDER'], 'Threat.txt'))
                if 'enactment' not in app.config['obj'].corpora_names:
                    app.config['obj'].add_dictionary(os.path.join(app.config['OH_UPLOAD_FOLDER'], 'Enactment.txt'))
                if 'Org_Id' not in app.config['obj'].corpora_names:
                    app.config['obj'].add_dictionary(os.path.join(app.config['OH_UPLOAD_FOLDER'], 'Org_Identity.txt'))
            elif app.config['check_all_oh'] == True:
                app.config['check_all_oh'] = False
                app.config['active_oh'] = [False, False, False, False]
                for i in range(0, 4):
                    app.config['obj'].deactivate_dictionary(first_oh_index + i)
            elif app.config['check_all_oh'] == False:
                app.config['check_all_oh'] = True
                app.config['active_oh'] = [True, True, True, True]
                for i in range(0, 4):
                    app.config['obj'].activate_dictionary(first_oh_index + i)
        elif 'oh' in request.form:
            oh = request.form['oh']
            index = 0
            first_oh_index = 0
            for i in range(0, len(app.config['obj'].dictionaries_names)):
                if app.config['obj'].dictionaries_names[i] == "Opportunity.txt":
                    if app.config['obj'].dictionaries_names[i + 1] == "Threat.txt" and app.config['obj'].dictionaries_names[i + 2] == "Enactment.txt" and app.config['obj'].dictionaries_names[i + 3] == "Org_Identity.txt":
                        first_oh_index = i
                if app.config['obj'].dictionaries_names[i].lower() == oh + ".txt":
                    index = i
            if not app.config['active_oh'][index - first_oh_index]:
                app.config['active_oh'][index - first_oh_index] = True
                app.config['obj'].activate_dictionary(index)
            elif app.config['active_oh'][index - first_oh_index]:
                app.config['active_oh'][index - first_oh_index] = False
                app.config['obj'].deactivate_dictionary(index)
            temp = app.config['active_oh'][0]
            all_chacked = True
            for i in app.config['active_oh']:
                if i != temp:
                    all_chacked = False
            if all_chacked:
                if temp != "checked":
                    app.config['check_all_oh'] = False

    return render_template("dictionaryManager.html",
                           title='Dictionary Manager',
                           active_dictionaries=app.config['active_dictionaries'],
                           check_all=app.config['check_all_dictionaries'],
                           labels=app.config['obj'].dictionaries_labels,
                           check_all_oh=app.config['check_all_oh'],
                           active_oh=app.config['active_oh'],
                           dictionaries=sorted(os.listdir(app.config['DICTIONARIES_UPLOAD_FOLDER'])))


def Generate_formula(is_default=0):
    if is_default == 0:
        active_dictionaries = app.config['obj'].active_dictionaries
        labels = app.config['obj'].dictionaries_labels
        if request.method == 'POST':
            formula = []
            for i in range(0, len(labels)):
                if active_dictionaries[i]:
                    if i == len(labels) - 1:
                        formula.append([labels[i], request.form['op' + str(i) + '1'], request.form['quantity' + str(i)]])
                    else:
                        formula.append([labels[i], request.form['op' + str(i) + '1'], request.form['quantity' + str(i)],
                                        request.form['op' + str(i) + '2']])
                app.config['formula'] = formula
    else:
        active_dictionaries = app.config['obj'].active_dictionaries
        labels = app.config['obj'].dictionaries_labels
        formula = []
        for i in range(0, len(labels)):
            if active_dictionaries[i]:
                if i == len(labels):
                    formula.append([labels[i], "*", "1"])
                else:
                    formula.append([labels[i], "*", "1", "+"])
            app.config['formula'] = formula


@app.route('/Test', methods=['GET', 'POST'])
def Test():
    Generate_formula()

    return render_template("test.html",
                           title='Test',
                           active_page='Test',
                           formula=app.config['formula'],
                           dictionaries=app.config['obj'].dictionaries_labels,
                           active_dictionaries=app.config['obj'].active_dictionaries)


@app.route('/Analyze', methods=['GET', 'POST'])
def Analyze():
    """
    Handles the functionality of the Analyze page. It generates a table with raw count for
    each corpus and its final score.
    :return: a render_template call.
    """
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
            headers={"Content-disposition": "attachment; filename=" + file_name})
    if len(app.config['formula']) == 0:
        Generate_formula(1)
    os.chdir(app.config['CORPORA_UPLOAD_FOLDER'])
    app.config['obj'].count_words()
    app.config['obj'].generate_scores(app.config['formula'])
    os.chdir(app.config['TMP_DIRECTORY'])
    content = app.config['obj'].to_html() + "<form method='POST'><input type='hidden' name='results' type='text' value='results'>" \
                   "<input class='button' id='download_scores' type='submit' value='Download'>" \
                   "</form>"
    app.config['obj'].save_to_csv()
    return render_template("analyze.html",
                           title='Analyze',
                           active_page='Analyze',
                           corpus_count=len(app.config['obj'].corpora),
                           dictionary_count=len(app.config['obj'].dictionaries),
                           content=content)


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
    app.config['formula'] = []
    return redirect(url_for('Upload'))
