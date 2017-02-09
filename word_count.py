from numpy import random
from collections import Counter


# For testing
# return: a string with 2 character words
def generate_random_string():
    random.seed(1834)
    string = ""
    for j in range(100):
        string += chr(random.randint(97, 122))
        if j%2 == 0:
            string += " "
    return string


# input:  string
# return: Counter object
def count_words(text):
    return Counter(text.split())



# Delete useless words
# input: Counter object
# return: Counter object
def stop_words(counter):
    ignore = ['the', 'a', 'if', 'in', 'it', 'of', 'or']
    for word in list(counter):
        if word in ignore:
            del counter[word]
    return counter


def main():
    #text = generate_random_string()
    with open('TestSuite/BankOfNYMellon2012', 'r') as myfile:
        text = myfile.read().decode("utf-8").replace('\n', '').lower()
    #print text
    count = count_words(text)
    #print count
    #count = stop_words(count)
    #print len(count)
    print count
    print "Total # of words:    ", len(text.split())
    print "# of words repeated: ", len(count)
    print "# of 'we':           ", count['we']
    print "# of 'our':          ", count['our']

if __name__ == "__main__":
    main()
