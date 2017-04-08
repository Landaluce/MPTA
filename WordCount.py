from app.fileManager import get_file_extension, strip_file_extension
#from docx import opendocx, getdocumenttext
import unicodedata
import ntpath
import csv
import re
import math


class WordCount(object):
    def __init__(self):
        self.dictionaries = []
        self.dictionaries_names = []
        self.dictionaries_labels = []
        self.active_dictionaries = []
        self.dictionaries_extensions = []
        self.corpora = []
        self.corpora_names = []
        self.corpora_labels = []
        self.active_corpora = []
        self.counts = []
        self.counters = []
        self.total_word_counts = []
        self.sums = []
        self.scores = []
        self.average = []

    def add_corpus(self, file_path):
        file_name = ntpath.basename(file_path)
        self.corpora_names.append(file_name)
        self.corpora_labels.append(ntpath.basename(strip_file_extension(file_name)))
        file_extension = get_file_extension(file_path)
        if file_extension == ".csv":
            new_corpus = read_csv(file_path)
        elif file_extension == ".txt" or " ":
            new_corpus = read_txt(file_path)
            new_corpus = self.utf8_to_ascii(new_corpus).decode('unicode_escape').encode('ascii', 'ignore')
        elif file_extension == ".docx":
            new_corpus = read_docx(file_path)
        self.corpora.append(new_corpus)
        self.active_corpora.append(1)
        self.total_word_counts.append(len(str(new_corpus).split(" ")))

    def add_dictionary(self, file_path):
        file_name = ntpath.basename(file_path)
        self.dictionaries_names.append(file_name)
        self.dictionaries_labels.append(ntpath.basename(strip_file_extension(file_name)))
        file_extension = get_file_extension(file_path)
        if file_extension == ".csv":
            with open(file_path, 'rb') as f:
                reader = csv.reader(f)
                rows = list(reader)
            new_list = []
            for row in rows:
                for cell in row:
                    cell = cell.strip()
                    new_list.append(cell)
        elif file_extension == ".txt" or " ":
            new_list = read_txt(file_path)
            new_list = new_list.split(", ")
            new_list = map(lambda x: x.encode("utf-8"), new_list)
        elif file_extension == ".docx":
            new_list = read_docx(file_path)
            new_list = new_list.split(", ")
            new_list = map(lambda x: x.encode("utf-8"), new_list)
        new_list.sort(key=lambda x: len(x.split()), reverse=True)
        new_list = list(map(lambda x: x.lower(), new_list))
        self.dictionaries.append(new_list)
        self.active_dictionaries.append(1)
        self.dictionaries_extensions.append(file_extension)

    def delete_corpus(self, index):
        del self.corpora[index]
        del self.corpora_names[index]
        del self.active_corpora[index]

    def delete_dictionary(self, index):
        del self.dictionaries[index]
        del self.dictionaries_names[index]
        del self.dictionaries_labels[index]
        del self.active_dictionaries[index]
        del self.dictionaries_extensions[index]

    def deactivate_corpus(self, index):
        self.active_corpora[index] = False

    def activate_corpus(self, index):
        self.active_corpora[index] = True

    def deactivate_dictionary(self, index):
        self.active_dictionaries[index] = False

    def activate_dictionary(self, index):
        self.active_dictionaries[index] = True

    def utf8_to_ascii(self, text):
        text = text.replace(u'\u2014', '-')
        text = text.replace(u'\u2013', '-')
        exclude = ['!', '"', '#', '$', '%', '&', '(', ')', '*', '+', ',', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']#, u'\u2018', u'\u2019', u'\u201c', u'\u201d', u'\u2022', u'\u2026']
        exclude.append(u'\u2018')  # '
        exclude.append(u'\u2019')  # '
        exclude.append(u'\u201c')  # "
        exclude.append(u'\u201d')  # "
        exclude.append(u'\u2022')  # bullet point
        exclude.append(u'\u2026')  # ...

        for c in exclude: #---------------------------------------
            text = text.replace(c, ' ')
        return ' '.join(text.split())

    def count_words(self):
        # delete previous results
        self.counts = []
        self.counters = []
        self.scores = []
        corpora = self.corpora
        for corpus in corpora:
            counts = []
            for i in range(len(self.dictionaries)):
                if self.active_dictionaries[i]:
                    count = 0
                    for word in self.dictionaries[i]:
                        if corpus.startswith(word + " "):
                            count += 1
                        if corpus.endswith(" " + word + "\n") or corpus.endswith(" " + word) or corpus.endswith(word):
                            count += 1
                        else:
                            count += len(re.findall(" " + word + " ", corpus))
                        if ' ' in word:
                            corpus = corpus.replace(word, " ")
                    counts.append(count)
            self.counters.append(counts)

    def generate_scores(self, formulas):
        index = 0
        if len(formulas) > 0:
            for i in range(len(self.counters)):
                sum = 0
                for x in range(len(self.counters[i])):
                    formula = formulas[x]
                    if x == 0:
                        next = '+'
                    else:
                        next = formulas[x-1][3]
                    op = eval(str(self.counters[i][x]) + str(formula[1])+str(formula[2]))
                    self.counters[i][x] = op
                    sum = eval(str(sum) + next + str(op))
                self.scores.append(float(sum)/self.total_word_counts[index])
                self.sums.append(sum)
                index += 1
        else:
            for counts in self.counters:
                sum = 0
                index = 0
                for count in counts:
                    sum += count
                self.scores.append(round(float(sum) / self.total_word_counts[index]), 1)
                self.sums.append(sum)
                index += 1
        self.generate_averages()

    def generate_averages(self):
        self.average = []
        sum = 0   # total hardiness score
        sum2 = 0  # total word count score
        sum3 = 0  # sum
        for i in range(len(self.scores)):
            sum += self.scores[i]
            sum2 += self.total_word_counts[i]
            sum3 += self.sums[i]
        avg = round((float(sum)/len(self.scores)), 3)
        avg2 = round((float(sum2)/(len(self.total_word_counts))), 1)
        avg3 = round((float(sum3)/len(self.sums)), 1)
        cat_count = 0
        self.average.append("Averages")
        for x in range(len(self.dictionaries)):
            for i in range(len(self.counters)):
                cat_count += self.counters[i][x]
            self.average.append(round(float(cat_count)/len(self.counters), 1))
            cat_count = 0
        self.average.append(avg3)
        self.average.append(avg2)
        self.average.append(avg)

    def to_html(self):
        result = "<table id='analyze_table'><tr id='header'>"
        result += "<td align='center'>Files</td>"
        for i in range(len(self.dictionaries_names)):
            if self.active_dictionaries[i] == 1:
                result += "<td align='center'>" + self.dictionaries_labels[i] + "</td>"
        result += "<td align='center'>Sums</td>"
        result += "<td align='center'>Total Word Counts</td>"
        result += "<td align='center'>Scores</td>"
        result += "</tr><tr>"
        for i in range(len(self.corpora_names)):
            if self.active_corpora[i] == 1:
                result += "</tr>"
                if i % 2 == 0:
                    result += "<tr id='even'>"
                else:
                    result += "<tr id='odd'>"
                result += "<td align='center'>" + self.corpora_labels[i] + "</td>"
                for counts in self.counters[i] + [self.sums[i]] + [self.total_word_counts[i]] + [self.scores[i]]:
                    result += "<td align='center'>" + str(counts) + "</td>"
        result += "</tr><tr>"
        for x in range(len(self.average)):
            result += "<td align='center'>" + str(self.average[x]) + "</td>"
        result += "</tr></table>"
        return result

    def display(self):
        matrix = self.to_matrix()
        for row in matrix:
            print(row)

    def to_matrix(self):
        header = []
        header.append("file")
        for i in range(len(self.dictionaries_names)):
            if self.active_dictionaries[i] == 1:
                header.append(self.dictionaries_names[i])
        header.append("sums")
        header.append("total_word_count")
        header.append("score")
        matrix = []
        matrix.append(header)
        for i in range(len(self.corpora_names)):
            if self.active_corpora[i] == 1:
                row = []
                row.append(self.corpora_names[i])
                for x in self.counters[i]:
                    row.append(x)
                row.append(self.sums[i])
                row.append(self.total_word_counts[i])
                row.append(self.scores[i])
                matrix.append(row)
        lrow = [] #last row 
        for i in range(len(self.average)):
            lrow.append(self.average[i])
        matrix.append(lrow)
                
        return matrix

    def save_to_csv(self):
        matrix = self.to_matrix()
        with open('results.csv', 'wb') as csv_file:
            spam_writer = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for row in matrix:
                spam_writer.writerow(row)
        csv_file.close()


def read_txt(file_path):
    try:
        with open(file_path, 'r') as txt_file:
            text = txt_file.read().decode("latin")
            return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')
    except IOError:
        print("could not read", file_path)


def read_csv(file_path):
    result = ""
    try:
        with open(file_path, 'rb') as csv_file:
            spam_reader = csv.reader(csv_file, delimiter=',')
            for row in spam_reader:
                result += ', '.join(row)
        return result
    except IOError:
        print("could not read", file_path)


def read_docx(file_path):
    document = opendocx(file_path)
    return " ".join(getdocumenttext(document)).encode("utf-8")
