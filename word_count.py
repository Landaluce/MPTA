import re
from collections import Counter

opportunity = ["advantage", "befalling", "break", "chance","connection",
               "contingency", "convenience", "cut", "fair shake", "favorable",
               "fighting chance", "fitness", "fling", "fortuity", "hope",
               "luck", "recourse"]
threat = ["alarming fateful", "apocalyptic", "baleful", "baneful", "black",
          "cautionary", "challenging", "comminatory", "crisis", "dangerous",
          "demur", "dire", "grim", "ill-boding", "imminent", "impendent",
          "impending", "inauspicious", "intimidating", "looming", "loury",
          "lowering", "lowery", "minacious", "minatory", "portending", "portent",
          "sinister", "trial dire", "ugly", "unlucky", "unpropitious", "unsafe",
          "warning",]


# Delete useless words
# input: Counter object
# return: Counter object
def stop_words(counter):
    ignore = ['the', 'a', 'if', 'in', 'it', 'of', 'or']
    for word in list(counter):
        if word in ignore:
            del counter[word]
    return counter

# don't need it anymore
def utf8_to_ascii(text):
    text = text.replace(u'\u2014', '-')
    text = text.replace(u'\u2013', '-')
    exclude = set('!"#$%&()*+,./:;<=>?@[\]^_`{|}~')
    exclude.add(u'\u2018')  # '
    exclude.add(u'\u2019')  # '
    exclude.add(u'\u201c')  # "
    exclude.add(u'\u201d')  # "
    exclude.add(u'\u2022')  # bullet point
    exclude.add(u'\u2026')  # ...
    exclude.add(u'\u00A5')

    exclude.add(u'\u00F0')
    exclude.add(u'\u00F1')
    exclude.add(u'\u00F2')
    exclude.add(u'\u00F3')
    exclude.add(u'\u00F4')
    exclude.add(u'\u00F5')

    exclude.add(u'\u00A1')
    exclude.add(u'\u00BC')
    exclude.add(u'\u00A3')
    exclude.add(u'\u00E9')
    exclude.add(u'\u2021')
    exclude.add(u'\u0161')
    exclude.add(u'\u0142')
    exclude.add(u'\u00BF')
    exclude.add(u'\u2030')
    exclude.add(u'\u2044')
    exclude.add(u'\u00A8')
    exclude.add(u'\u00A9')
    exclude.add(u'\u00AA')
    exclude.add(u'\u00FE')
    exclude.add(u'\u00DF')
    exclude.add(u'\u2122')
    exclude.add(u'\u0153')
    exclude.add(u'\uFB01')
    exclude.add(u'\uFB02')
    exclude.add(u'\u102A')
    exclude.add(u'\u201A')
    exclude.add(u'\u00AE')
    exclude.add(u'\u00E7')
    exclude.add(u'\u00F8')
    exclude.add(u'\u00FC')
    exclude.add(u'\u02DC')

    text = ''.join(ch for ch in text if ch not in exclude)

    return text


def find_words(text):
    op_count = 0
    for word in opportunity:
        op_count += len(re.findall(word, text))
    th_count = 0
    for word in threat:
        th_count += len(re.findall(word, text))
    tup = (th_count, op_count)
    return tup


def read_txt(filepath):
    try:
        with open(filepath, 'r') as myfile:
            return myfile.read().decode("utf-8").replace('\n', '').lower()
    except IOError:
        print "could not read", filepath

# test case
def get_jpm_op_th():
    print "JPM"
    print "file, th, op"
    for i in range(2001, 2009 + 1):
        # docx
        text = read_txt("TestSuite/JP Morgan/JP Morgan" + str(i) + "docx.txt")
        # pdf
        #text = read_txt("TestSuite/JP Morgan/JP Morgan" + str(i) + ".txt")
        if text:
            text = utf8_to_ascii(text)
            tup = find_words(text.decode('unicode_escape').encode('ascii','ignore'))
            print str(i) + ", " + str(tup[0]) + ", " + str(tup[1])


def main():
    get_jpm_op_th()

if __name__ == "__main__":
    main()
