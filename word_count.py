import csv
import itertools
import re


opportunity = ['advancement', 'advantage', 'befalling', 'break', 'chance', 'connection', 'contingency', 'convenience', 'cut', 'expect', 'expectation', 'expects', 'expediency', 'fair shake', 'favorability', 'favorable', 'fighting chance', 'fitness', 'fling', 'fortuity', 'fortune', 'hope', 'luck', 'momentous', 'momentum', 'momentus', 'occasion', 'opening', 'opportune', 'opportunisitic', 'opportunistic', 'opportunities', 'opportunity', 'optimism', 'optimist', 'optimistic', 'outlook', 'possibility', 'prospect', 'prospects', 'prosperity', 'prosperous', 'recourse', 'stimulating', 'successful', 'suitable', 'time', 'turn', 'upbeat', 'viable']
#                                  1                       1                                                             2/7      2/3                                                                                                                                                     0/1                                                                 1                                                             3 1\n           3                                                                                                                                                                                   3/6 2.   0/4
# JPM2001 = 16
threat = ['alarming', 'alarming fateful', 'apocalyptic', 'assault', 'baleful', 'baneful', 'black', 'cautionary', 'challenging', 'comminatory', 'conflict', 'constrained', 'crisis', 'crunch', 'danger', 'dangerous', 'demur', 'dire', 'fateful', 'foreboding', 'grim', 'hazard', 'ill-boding', 'imminent', 'impendent', 'impending', 'inauspicious', 'intimidating', 'jeopardy', 'looming', 'loss', 'loury', 'lowering', 'lowery', 'menace', 'minacious', 'minatory', 'negative', 'omen', 'peril', 'portending', 'portent', 'risk', 'sinister', 'stressful', 'sword of damocles', 'trial dire', 'ugly', 'unlucky', 'unpropitious', 'unsafe', 'urgent', 'warning']
# JPM2001 = 3                                                                                                                      1                                                                                                                                                                                                                                                                     0/2                                                                                                                              2

enactment = ['absorb', 'access', 'accomplish', 'accrue', 'achieve', 'acquire', 'acquisition', 'act', 'action', 'active', 'activity', 'actualize', 'advance', 'affect', 'affiliate', 'aggrandizement', 'agitate', 'alacrity', 'alertness', 'ally', 'alter', 'amalgamat', 'amalgamate', 'amass', 'amplif', 'annex', 'appeal', 'assimilate', 'attack', 'attain', 'attribute', 'augment', 'bankrupt', 'barnstorm', 'battle', 'blend', 'boost', 'campaign', 'cement', 'censure', 'centralize', 'change', 'charge', 'cite', 'coalesce', 'combat', 'combine', 'commission', 'complain', 'complete', 'compound', 'conflict', 'conglomerate', 'consolidate', 'consummate', 'contend', 'contest', 'converge', 'crusade', 'cultivate', 'deconstruct', 'denounce', 'develop', 'developing', 'develops', 'dilation', 'disassemble', 'disinherit', 'dismantle', 'dispute', 'distention', 'divest', 'divestiture', 'effect', 'enact', 'encounter', 'engage', 'engagement', 'enlarge', 'enterprise', 'environment', 'environs', 'execute', 'exercise', 'exert', 'expand', 'expands', 'expansion', 'exploit', 'extension', 'fight', 'finish', 'force', 'forfeit', 'fulfill', 'further', 'fuse', 'gradual increase', 'gradually increase', 'grow', 'grows', 'growth', 'impeach', 'implicate', 'impute', 'incorporate', 'incriminate', 'inculpate', 'indict', 'induce', 'industry', 'influence', 'intermingle', 'intervene', 'intervention', 'investment banker', 'join', 'league', 'lobby', 'manage', 'maneuver', 'manipulate', 'market', 'marry', 'meld', 'merge', 'mingle', 'modify', 'move', 'network', 'niche', 'nook', 'occupy', 'operate', 'operation', 'oust', 'perform', 'persuade', 'pitch', 'planted', 'plug', 'politick', 'pool', 'press', 'pressure', 'proceed', 'proceeds', 'process', 'procure', 'progress', 'progression', 'promote', 'prosecute', 'province', 'purchase', 'purview', 'react', 'realize', 'region', 'relinquish', 'remove', 'request', 'resist', 'resolve', 'respond', 'rival', 'rush', 'sacrifice', 'scope', 'sector', 'secure', 'sell', 'separate', 'solicit', 'stir', 'strive', 'struggle', 'sway', 'syndicate', 'synthesize', 'team', 'team up', 'terrain', 'territory', 'thrust', 'transact', 'turgescence', 'undertake', 'unite', 'urge', 'vie', 'win']
#                                                            2                      0/4s       3/15     0/5                                                                                                                                 0/1                                                                                                                 0/1s                                                                                                                         1/2       0/1      1/2                             0/4                                 1/2
# JPM2001 = 8...

org_iden = ['abreast', 'accede', 'acceded', 'accedes', 'acceding', 'accept', 'accepted', 'accepting', 'accepts', 'accommodate', 'accommodated', 'accommodates', 'accommodation', 'accompanied', 'accompanies', 'accompany', 'accompanying', 'accord', 'accords', 'adhere', 'adhered', 'adheres', 'adhering', 'admit', 'admits', 'admitted', 'admitting', 'affiliate', 'affiliated', 'affiliates', 'affiliating', 'affiliation', 'affiliations', 'affinities', 'affinity', 'affirm', 'affirmed', 'affirming', 'affirms', 'aggregate', 'aggregated', 'aggregates', 'aggregating', 'agree', 'agreeable', 'agreed', 'agreeing', 'agrees', 'akin', 'align', 'aligned', 'aligning', 'alignment', 'alignments', 'aligns', 'alike', 'all', 'alliances', 'allied', 'allies', 'allow', 'allowed', 'allowing', 'allows', 'ally', 'alongside', 'altogether', 'amalgamate', 'amalgamated', 'amalgamating', 'amalgamation', 'amalgamations', 'ambience', 'analogies', 'analogous', 'analogy', 'ancestry', 'annex', 'annexed', 'annexes', 'annexing', 'approve', 'approved', 'approves', 'approving', 'arbitrate', 'arbitrated', 'arbitrating', 'arbitration', 'arbitrations', 'arrange', 'arranged', 'arrangement', 'arrangements', 'arranges', 'arranging', 'assemblage', 'assemblages', 'assemble', 'assembled', 'assemblies', 'assembling', 'assembly', 'assent', 'assented', 'assenting', 'assents', 'associate', 'associated', 'associates', 'associating', 'association', 'associations', 'atmosphere', 'aura', 'authentic', 'balance', 'balance-of-power', 'balanced', 'balances', 'balancing', 'bandwagon', 'bandwagons', 'basic', 'bedfellow', 'bedfellows', 'bi-lateral', 'bilingual', 'bind', 'binding', 'binds', 'bipartisan', 'birthright', 'blend', 'blended', 'blending', 'blends', 'bloc', 'blocs', 'bond', 'bonded', 'bonding', 'bonds', 'bound', 'brotherhood', 'brotherhoods', 'buddies', 'buddy', 'cahoots', 'camaraderie', 'cardinal', 'caretaker', 'caretakers', 'caretaking', 'categorical', 'caucus', 'caucused', 'caucuses', 'caucusing', 'ceaseless', 'center', 'character', 'chief', 'chum', 'chums', 'circumstances', 'clan', 'clans', 'class', 'class-action', 'class-based', 'classes', 'classification', 'classifications', 'classified', 'classifies', 'classify', 'classifying', 'classmate', 'classmates', 'climate', 'clique', 'cliques', 'close', 'closeness', 'closer', 'closest', 'club', 'clubs', 'cluster', 'clustered', 'clustering', 'clusters', 'co-worker', 'coalition', 'coalitions', 'cohere', 'coherent', 'cohesive', 'cohort', 'cohorts', 'coincide', 'coincided', 'coincides', 'coinciding', 'collaborate', 'collaborated', 'collaborates', 'collaboration', 'collaborations', 'colleague', 'colleagues', 'collection', 'collections', 'collective', 'collectives', 'collude', 'colluded', 'colludes', 'colluding', 'collusion', 'collusions', 'combination', 'combinations', 'combine', 'combined', 'combines', 'combining', 'commend', 'commended', 'commending', 'commends', 'commission', 'commissions', 'committee', 'committees', 'communal', 'commune', 'communes', 'communities', 'companion', 'companionable', 'companions', 'companionship', 'comparable', 'comparably', 'compatibilities', 'compatibility', 'compatible', 'complement', 'complemented', 'complementing', 'complements', 'complied', 'complies', 'compliment', 'compliments', 'comply', 'complying', 'composite', 'composites', 'compromise', 'compromised', 'compromises', 'compromising', 'comrade', 'comrades', 'concede', 'conceded', 'concedes', 'conceding', 'concert', 'concerted', 'concession', 'concessions', 'concur', 'concurred', 'concurrent', 'concurring', 'concurs', 'confirm', 'confirmation', 'confirmations', 'confirmed', 'confirming', 'confirms', 'conform', 'conformed', 'conforming', 'conforms', 'congenial', 'congregate', 'congregates', 'congregating', 'congregations', 'conjoin', 'conjoined', 'conjoining', 'conjoins', 'conjunction', 'conjunctions', 'connect', 'connected', 'connecting', 'connection', 'connections', 'connects', 'consensus', 'consent', 'consented', 'consenting', 'consents', 'consistencies', 'consistency', 'consistent', 'consolidate', 'consolidated', 'consolidates', 'consolidating', 'consolidation', 'consolidations', 'consonance', 'conspiracies', 'conspiracy', 'conspire', 'conspired', 'conspires', 'constant', 'contact', 'contacted', 'contacting', 'context', 'continual', 'continuous', 'contracted', 'contracting', 'contributed', 'contributes', 'contribution', 'contributions', 'convene', 'convened', 'convenes', 'convening', 'converge', 'converged', 'converges', 'converging', 'cooperate', 'cooperated', 'cooperates', 'cooperation', 'cooperative', 'cooperatively', 'coordinate', 'coordinated', 'coordinates', 'coordinating', 'coordination', 'copied', 'copies', 'copy', 'copying', 'cordial', 'correlate', 'correlated', 'correlates', 'correlating', 'correlation', 'correlations', 'corresponding', 'covenant', 'covenants', 'cronies', 'crony', 'culture', 'customary', 'customs', 'dealings', 'definite', 'definitive', 'dependable', 'dependence', 'dependent', 'devote', 'devoted', 'devotes', 'devoting', 'discrete', 'disparate', 'disposition', 'distinct', 'distinctive', 'divergent', 'diverse', 'dominant', 'donate', 'donated', 'donates', 'donation', 'donations', 'duplicate', 'duplicated', 'duplicates', 'duplicating', 'd\xe9tente', 'echo', 'echoed', 'echoes', 'echoing', 'elemental', 'embrace', 'embraced', 'embraces', 'embracing', 'empathize', 'empathized', 'empathizes', 'empathizing', 'empathy', 'endorse', 'endorsed', 'endorses', 'endorsing', 'enduring', 'environ', 'equal', 'equalities', 'equality', 'equally', 'equate', 'equated', 'equating', 'equidistant', 'equivalence', 'equivalent', 'essential', 'eternal', 'everybody', 'exchange', 'exchanged', 'exchanges', 'exchanging', 'experience', 'explicit', 'express', 'facilitate', 'facilitated', 'facilitates', 'facilitating', 'faithful', 'familiar', 'familiarity', 'families', 'federation', 'federations', 'feeling', 'fellowship', 'fellowships', 'focal', 'folklore', 'folkways', 'foremost', 'friendliness', 'friendship', 'friendships', 'fundamental', 'fuse', 'fused', 'fusing', 'fusion', 'genuine', 'get-together', 'get-togethers', 'give-and-take', 'go-between', 'habitual', 'help', 'helped', 'helping', 'helpmate', 'helpmates', 'helps', 'homogeneity', 'homogeneous', 'hospitable', 'hospitality', 'identical', 'illustrative', 'immutable', 'important', 'incessant', 'include', 'included', 'includes', 'including', 'inclusion', 'incorporate', 'incorporated', 'incorporates', 'incorporating', 'indispensable', 'indulge', 'indulged', 'indulgence', 'indulgences', 'indulges', 'indulging', 'inherent', 'inmost', 'inner', 'integrate', 'integrated', 'integrates', 'integrating', 'integration', 'interact', 'interacted', 'interacting', 'interaction', 'interactions', 'intercede', 'interceded', 'intercedes', 'interceding', 'interchangeable', 'interconnect', 'interconnected', 'interconnecting', 'interconnection', 'interconnections', 'interconnects', 'intercourse', 'interior', 'intermesh', 'intermeshed', 'intermeshes', 'intermeshing', 'interrelate', 'interrelated', 'interrelating', 'interrelations', 'intersect', 'intersected', 'intersecting', 'intersection', 'intersections', 'intertwine', 'intertwined', 'intertwines', 'intertwining', 'intimacies', 'intimacy', 'intimate', 'intrinsic', 'invariable', 'join', 'joined', 'joining', 'joins', 'joint', 'junction', 'junctions', 'key', 'kindred', 'kinship', 'lasting', 'leading', 'liaison', 'liaisons', 'like-minded', 'like-mindedness', 'likeness', 'likenesses', 'likewise', 'lineage', 'link', 'linked', 'linking', 'links', 'lucid', 'main', 'marked', 'master', 'matched', 'matching', 'mate', 'mated', 'mates', 'mating', 'mediate', 'mediated', 'mediates', 'mediating', 'medium', 'meetings', 'milieu', 'mingle', 'mingled', 'mingling', 'mood', 'mutual', 'mutuality', 'negotiable', 'negotiate', 'negotiated', 'negotiating', 'negotiation', 'negotiations', 'networked', 'networking', 'networks', 'noticeable', 'offer', 'offered', 'offering', 'offers', 'oneness', 'organization', 'organizational', 'orientation', 'our', 'ourself', 'ourselves', 'palatable', 'parallel', 'parallels', 'paramount', 'parity', 'partake', 'partakes', 'partaking', 'participate', 'participated', 'participates', 'participation', 'particular', 'parties', 'partner', 'partners', 'partnership', 'partnerships', 'partook', 'party', 'party-line', 'patent', 'patronage', 'peculiar', 'peer', 'peers', 'permanent', 'permission', 'permit', 'permits', 'permitted', 'permitting', 'perpetual', 'persevering', 'persistent', 'pivotal', 'pledge', 'pledged', 'pledges', 'pledging', 'predominant', 'primary', 'prime', 'principle', 'public-interest', 'public-service', 'public-spirited', 'rapport', 'ratified', 'ratifies', 'ratify', 'reciprocal', 'reciprocate', 'reciprocated', 'reciprocates', 'reciprocating', 'reciprocation', 'reciprocity', 'recognizable', 'recruit', 'recruited', 'recruiting', 'recruits', 'regular', 'relate', 'related', 'relates', 'relating', 'relations', 'relationship', 'relationships', 'rendezvous', 'reproduce', 'reproduced', 'reproduces', 'reproducing', 'resemblance', 'resemblances', 'resemble', 'resembled', 'resembling', 'resolute', 'reunite', 'reunited', 'reuniting', 'salient', 'same', 'sameness', 'scene', 'schoolmate', 'schoolmates', 'self-denial', 'self-denying', 'self-effacement', 'self-effacing', 'self-sacrifice', 'self-sacrificing', 'selfless', 'selfsame', 'setting', 'share', 'shared', 'shares', 'sharing', 'significant', 'similar', 'similarities', 'sisterhood', 'sisterhoods', 'situation', 'sociability', 'sociable', 'socialization', 'socialize', 'socialized', 'socializing', 'special', 'specific', 'spirit', 'stable', 'staunch', 'steadfast', 'steady', 'subscribe', 'subscribed', 'subscribes', 'subscribing', 'sufferance', 'surroundings', 'symmetrical', 'symmetry', 'sympathize', 'sympathized', 'sympathizes', 'sympathizing', 'sympathy', 'synchronize', 'synchronized', 'synchronizes', 'synchronizing', 'synchronous', 'syndicate', 'syndicates', 'synonymous', 'syntheses', 'synthesis', 'synthetic', 'tantamount', 'teamed', 'teaming', 'teammate', 'teammates', 'teams', 'teamwork', 'temperament', 'tenor', 'terrain', 'territory', 'their', 'them', 'they', 'tie-in', 'tie-ins', 'timbre', 'together', 'tolerance', 'tolerant', 'tolerate', 'tolerates', 'tolerating', 'toleration', 'tone', 'townspeople', 'turf', 'twin', 'twins', 'unalterable', 'unambiguous', 'unanimity', 'unanimous', 'unchanging', 'underlying', 'unequivocal', 'unfailing', 'unflagging', 'unflappable', 'unfluctuating', 'unification', 'unified', 'uniform', 'unify', 'unifying', 'uninterrupted', 'unions', 'unique', 'unison', 'unit', 'unite', 'unites', 'uniting', 'units', 'unity', 'unmistakable', 'unrelenting', 'unremitting', 'unties', 'unvarying', 'unwavered', 'unwavering', 'us', 'vital', 'vouch', 'vouched', 'vouches', 'vouching', 'warrant', 'warranted', 'warranting', 'warrants', 'we', 'well-beloved', 'well-disposed', 'well-inclined', 'well-loved', 'well-wisher', 'well-wishers', 'whole', 'wholly', 'willing', 'willingly']


#Uploading all Organizational Identity words into a list called new_list
empt_list = []
iter_count = 0
with open('OrgID.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter= ',')
    for row in reader:
        empt_list.append(row)
        iter_count += 1
    org_iden = list(itertools.chain(*empt_list))
    #print org_iden
    #print iter_count


def scrub_list(lst):
    lst = list(map(lambda x: x.lower(), lst))
    lst = list(sorted(set(lst)))
    return lst


#org = scrub_list(org_iden)
#print org
#with open("Dictionaries/org_id", 'w') as file:
#    file.write((", ").join(org))
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
    or_count = 0
    for word in org_iden:
        or_count += len(re.findall(" " + word + " ", text))
    tup = (th_count, en_count, op_count, or_count)
    return tup


def read_txt(filepath):
    try:
        with open(filepath, 'r') as myfile:
            return myfile.read().decode("utf-8").lower()
    except IOError:
        print "could not read", filepath

# test case
def get_jpm():
    print "JPM"
    print '{:>8} {:>8} {:>8} {:>8} {:>10}'.format("year", "threat", "enactment", "opportunity", "org identity")
    for i in range(2000, 2009 + 1):
        # docx
        text = read_txt("TestSuite/JP Morgan/JP Morgan" + str(i) + "docx.txt")
        # pdf
        #text = read_txt("TestSuite/JP Morgan/JP Morgan" + str(i) + ".txt")
        if text:
            text = utf8_to_ascii(text)
            tup = find_words(text.decode('unicode_escape').encode('ascii','ignore'))
            print '{:>8} {:>8} {:>8} {:>8} {:>10}'.format(str(i), str(tup[0]), str(tup[1]), str(tup[2]), str(tup[3]))


def main():
    get_jpm()

    pass


if __name__ == "__main__":
    main()
