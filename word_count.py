import re

opportunity = ['advancement', 'advantage', 'befalling', 'break', 'chance', 'connection', 'contingency', 'convenience', 'cut', 'expect', 'expectation', 'expects', 'expediency', 'fair shake', 'favorability', 'favorable', 'fighting chance', 'fitness', 'fling', 'fortuity', 'fortune', 'hope', 'luck', 'momentous', 'momentum', 'momentus', 'occasion', 'opening', 'opportune', 'opportunisitic', 'opportunistic', 'opportunities', 'opportunity', 'optimism', 'optimist', 'optimistic', 'outlook', 'possibility', 'prospect', 'prospects', 'prosperity', 'prosperous', 'recourse', 'stimulating', 'successful', 'suitable', 'time', 'turn', 'upbeat', 'viable']
#                                  1                       1                                                             2/7      2/3                                                                                                                                                     0/1                                                                 1                                                             3 1\n           3                                                                                                                                                                                   3/6 2.   0/4
# JPM2001 = 16
threat = ['alarming', 'alarming fateful', 'apocalyptic', 'assault', 'baleful', 'baneful', 'black', 'cautionary', 'challenging', 'comminatory', 'conflict', 'constrained', 'crisis', 'crunch', 'danger', 'dangerous', 'demur', 'dire', 'fateful', 'foreboding', 'grim', 'hazard', 'ill-boding', 'imminent', 'impendent', 'impending', 'inauspicious', 'intimidating', 'jeopardy', 'looming', 'loss', 'loury', 'lowering', 'lowery', 'menace', 'minacious', 'minatory', 'negative', 'omen', 'peril', 'portending', 'portent', 'risk', 'sinister', 'stressful', 'sword of damocles', 'trial dire', 'ugly', 'unlucky', 'unpropitious', 'unsafe', 'urgent', 'warning']
# JPM2001 = 3                                                                                                                      1                                                                                                                                                                                                                                                                     0/2                                                                                                                              2

enactment = ['absorb', 'access', 'accomplish', 'accrue', 'achieve', 'acquire', 'acquisition', 'act', 'action', 'active', 'activity', 'actualize', 'advance', 'affect', 'affiliate', 'aggrandizement', 'agitate', 'alacrity', 'alertness', 'ally', 'alter', 'amalgamat', 'amalgamate', 'amass', 'amplif', 'annex', 'appeal', 'assimilate', 'attack', 'attain', 'attribute', 'augment', 'bankrupt', 'barnstorm', 'battle', 'blend', 'boost', 'campaign', 'cement', 'censure', 'centralize', 'change', 'charge', 'cite', 'coalesce', 'combat', 'combine', 'commission', 'complain', 'complete', 'compound', 'conflict', 'conglomerate', 'consolidate', 'consummate', 'contend', 'contest', 'converge', 'crusade', 'cultivate', 'deconstruct', 'denounce', 'develop', 'developing', 'develops', 'dilation', 'disassemble', 'disinherit', 'dismantle', 'dispute', 'distention', 'divest', 'divestiture', 'effect', 'enact', 'encounter', 'engage', 'engagement', 'enlarge', 'enterprise', 'environment', 'environs', 'execute', 'exercise', 'exert', 'expand', 'expands', 'expansion', 'exploit', 'extension', 'fight', 'finish', 'force', 'forfeit', 'fulfill', 'further', 'fuse', 'gradual increase', 'gradually increase', 'grow', 'grows', 'growth', 'impeach', 'implicate', 'impute', 'incorporate', 'incriminate', 'inculpate', 'indict', 'induce', 'industry', 'influence', 'intermingle', 'intervene', 'intervention', 'investment banker', 'join', 'league', 'lobby', 'manage', 'maneuver', 'manipulate', 'market', 'marry', 'meld', 'merge', 'mingle', 'modify', 'move', 'network', 'niche', 'nook', 'occupy', 'operate', 'operation', 'oust', 'perform', 'persuade', 'pitch', 'planted', 'plug', 'politick', 'pool', 'press', 'pressure', 'proceed', 'proceeds', 'process', 'procure', 'progress', 'progression', 'promote', 'prosecute', 'province', 'purchase', 'purview', 'react', 'realize', 'region', 'relinquish', 'remove', 'request', 'resist', 'resolve', 'respond', 'rival', 'rush', 'sacrifice', 'scope', 'sector', 'secure', 'sell', 'separate', 'solicit', 'stir', 'strive', 'struggle', 'sway', 'syndicate', 'synthesize', 'team', 'team up', 'terrain', 'territory', 'thrust', 'transact', 'turgescence', 'undertake', 'unite', 'urge', 'vie', 'win']
#                                                            2                      0/4s       3/15     0/5                                                                                                                                 0/1                                                                                                                 0/1s                                                                                                                         1/2       0/1      1/2                             0/4                                 1/2
# JPM2001 = 8...
def scrub_list(lst):
    lst = list(map(lambda x: x.lower(), lst))
    lst = list(sorted(set(lst)))
    return lst


#enactment = scrub_list(enactment)
#print enactment
#with open("Dictionaries/opportunity", 'w') as file:
#    file.write((", ").join(opportunity))
#file.close()
#print (", ").join(enactment)


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
    #text = text.replace('\n', ' ')
    exclude = set('!"#$%&()*+,./:;<=>?@[\]^_`{|}~')
    exclude.add(u'\u2018')  # '
    exclude.add(u'\u2019')  # '
    exclude.add(u'\u201c')  # "
    exclude.add(u'\u201d')  # "
    exclude.add(u'\u2022')  # bullet point
    exclude.add(u'\u2026')  # ...

    for c in exclude:
        text = text.replace(c, ' ')
    #text = ''.join(ch for ch in text if ch not in exclude)

    return text


def find_words(text):
    op_count = 0
    for word in opportunity:
        op_count += len(re.findall(" " + word + " ", text))
    en_count = 0
    for word in enactment:
        en_count += len(re.findall(" " + word + " ", text))
    th_count = 0
    for word in threat:
        th_count += len(re.findall(" " + word + " ", text))
    tup = (th_count, en_count, op_count)
    return tup


def read_txt(filepath):
    try:
        with open(filepath, 'r') as myfile:
            return myfile.read().decode("utf-8").lower()
    except IOError:
        print "could not read", filepath

# test case
def get_jpm_op_th():
    print "JPM"
    print "file, th, en, op"
    for i in range(2001, 2009 + 1):
        # docx
        text = read_txt("TestSuite/JP Morgan/JP Morgan" + str(i) + "docx.txt")
        # pdf
        #text = read_txt("TestSuite/JP Morgan/JP Morgan" + str(i) + ".txt")
        if text:
            text = utf8_to_ascii(text)
            tup = find_words(text.decode('unicode_escape').encode('ascii','ignore'))
            print str(i) + ", " + str(tup[0]) + ", " + str(tup[1]) + ", " + str(tup[2])


def main():
    get_jpm_op_th()

    pass


if __name__ == "__main__":
    main()
