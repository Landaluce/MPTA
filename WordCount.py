from app.fileManager import get_file_type, strip_file_extension
import ntpath
import csv
import re


class WordCount(object):
    def __init__(self):
        self.opportunity = ['fair shake', 'fighting chance', 'advancement', 'advantage', 'befalling', 'break', 'chance', 'connection', 'contingency', 'convenience', 'cut', 'expect', 'expectation', 'expects', 'expediency', 'favorability', 'favorable', 'fitness', 'fling', 'fortuity', 'fortune', 'hope', 'luck', 'momentous', 'momentum', 'momentus', 'occasion', 'opening', 'opportune', 'opportunisitic', 'opportunistic', 'opportunities', 'opportunity', 'optimism', 'optimist', 'optimistic', 'outlook', 'possibility', 'prospect', 'prospects', 'prosperity', 'prosperous', 'recourse', 'stimulating', 'successful', 'suitable', 'time', 'turn', 'upbeat', 'viable']

        self.threat = ['sword of damocles', 'alarming fateful', 'trial dire', 'alarming', 'apocalyptic', 'assault', 'baleful', 'baneful', 'black', 'cautionary', 'challenging', 'comminatory', 'conflict', 'constrained', 'crisis', 'crunch', 'danger', 'dangerous', 'demur', 'dire', 'fateful', 'foreboding', 'grim', 'hazard', 'ill-boding', 'imminent', 'impendent', 'impending', 'inauspicious', 'intimidating', 'jeopardy', 'looming', 'loss', 'loury', 'lowering', 'lowery', 'menace', 'minacious', 'minatory', 'negative', 'omen', 'peril', 'portending', 'portent', 'risk', 'sinister', 'stressful', 'ugly', 'unlucky', 'unpropitious', 'unsafe', 'urgent', 'warning']

        self.enactment = ['gradual increase', 'gradually increase', 'investment banker', 'team up', 'absorb', 'access', 'accomplish', 'accrue', 'achieve', 'acquire', 'acquisition', 'act', 'action', 'active', 'activity', 'actualize', 'advance', 'affect', 'affiliate', 'aggrandizement', 'agitate', 'alacrity', 'alertness', 'ally', 'alter', 'amalgamat', 'amalgamate', 'amass', 'amplif', 'annex', 'appeal', 'assimilate', 'attack', 'attain', 'attribute', 'augment', 'bankrupt', 'barnstorm', 'battle', 'blend', 'boost', 'campaign', 'cement', 'censure', 'centralize', 'change', 'charge', 'cite', 'coalesce', 'combat', 'combine', 'commission', 'complain', 'complete', 'compound', 'conflict', 'conglomerate', 'consolidate', 'consummate', 'contend', 'contest', 'converge', 'crusade', 'cultivate', 'deconstruct', 'denounce', 'develop', 'developing', 'develops', 'dilation', 'disassemble', 'disinherit', 'dismantle', 'dispute', 'distention', 'divest', 'divestiture', 'effect', 'enact', 'encounter', 'engage', 'engagement', 'enlarge', 'enterprise', 'environment', 'environs', 'execute', 'exercise', 'exert', 'expand', 'expands', 'expansion', 'exploit', 'extension', 'fight', 'finish', 'force', 'forfeit', 'fulfill', 'further', 'fuse', 'grow', 'grows', 'growth', 'impeach', 'implicate', 'impute', 'incorporate', 'incriminate', 'inculpate', 'indict', 'induce', 'industry', 'influence', 'intermingle', 'intervene', 'intervention', 'join', 'league', 'lobby', 'manage', 'maneuver', 'manipulate', 'market', 'marry', 'meld', 'merge', 'mingle', 'modify', 'move', 'network', 'niche', 'nook', 'occupy', 'operate', 'operation', 'oust', 'perform', 'persuade', 'pitch', 'planted', 'plug', 'politick', 'pool', 'press', 'pressure', 'proceed', 'proceeds', 'process', 'procure', 'progress', 'progression', 'promote', 'prosecute', 'province', 'purchase', 'purview', 'react', 'realize', 'region', 'relinquish', 'remove', 'request', 'resist', 'resolve', 'respond', 'rival', 'rush', 'sacrifice', 'scope', 'sector', 'secure', 'sell', 'separate', 'solicit', 'stir', 'strive', 'struggle', 'sway', 'syndicate', 'synthesize', 'team', 'terrain', 'territory', 'thrust', 'transact', 'turgescence', 'undertake', 'unite', 'urge', 'vie', 'win']

        self.org_iden = ['abreast', 'accede', 'acceded', 'accedes', 'acceding', 'accept', 'accepted', 'accepting', 'accepts',
                'accommodate', 'accommodated', 'accommodates', 'accommodation', 'accompanied', 'accompanies',
                'accompany', 'accompanying', 'accord', 'accords', 'adhere', 'adhered', 'adheres', 'adhering', 'admit', 'admits',
                'admitted', 'admitting', 'affiliate', 'affiliated', 'affiliates', 'affiliating', 'affiliation',
                'affiliations', 'affinities', 'affinity', 'affirm', 'affirmed', 'affirming', 'affirms', 'aggregate',
                'aggregated', 'aggregates', 'aggregating', 'agree', 'agreeable', 'agreed', 'agreeing', 'agrees', 'akin',
                'align', 'aligned', 'aligning', 'alignment', 'alignments', 'aligns', 'alike', 'all', 'alliances',
                'allied', 'allies', 'allow', 'allowed', 'allowing', 'allows', 'ally', 'alongside', 'altogether', 'amalgamate',
                'amalgamated', 'amalgamating', 'amalgamation', 'amalgamations', 'ambience', 'analogies', 'analogous',
                'analogy', 'ancestry', 'annex', 'annexed', 'annexes', 'annexing', 'approve', 'approved', 'approves',
                'approving', 'arbitrate', 'arbitrated', 'arbitrating', 'arbitration', 'arbitrations', 'arrange',
                'arranged', 'arrangement', 'arrangements', 'arranges', 'arranging', 'assemblage', 'assemblages', 'assemble',
                'assembled', 'assemblies', 'assembling', 'assembly', 'assent', 'assented', 'assenting', 'assents',
                'associate', 'associated', 'associates', 'associating', 'association', 'associations', 'atmosphere',
                'aura', 'authentic', 'balance', 'balance-of-power', 'balanced', 'balances', 'balancing', 'bandwagon',
                'bandwagons', 'basic', 'bedfellow', 'bedfellows', 'bi-lateral', 'bilingual', 'bind', 'binding', 'binds', 'bipartisan',
                'birthright', 'blend', 'blended', 'blending', 'blends', 'bloc', 'blocs', 'bond', 'bonded', 'bonding',
                'bonds', 'bound', 'brotherhood', 'brotherhoods', 'buddies', 'buddy', 'cahoots', 'camaraderie',
                'cardinal', 'caretaker', 'caretakers', 'caretaking', 'categorical', 'caucus', 'caucused', 'caucuses', 'caucusing',
                'ceaseless', 'center', 'character', 'chief', 'chum', 'chums', 'circumstances', 'clan', 'clans', 'class',
                'class-action', 'class-based', 'classes', 'classification', 'classifications', 'classified',
                'classifies', 'classify', 'classifying', 'classmate', 'classmates', 'climate', 'clique', 'cliques', 'close',
                'closeness', 'closer', 'closest', 'club', 'clubs', 'cluster', 'clustered', 'clustering', 'clusters', 'co-worker',
                'coalition', 'coalitions', 'cohere', 'coherent', 'cohesive', 'cohort', 'cohorts', 'coincide',
                'coincided', 'coincides', 'coinciding', 'collaborate', 'collaborated', 'collaborates', 'collaboration',
                'collaborations', 'colleague', 'colleagues', 'collection', 'collections', 'collective', 'collectives', 'collude',
                'colluded', 'colludes', 'colluding', 'collusion', 'collusions', 'combination', 'combinations', 'combine',
                'combined', 'combines', 'combining', 'commend', 'commended', 'commending', 'commends', 'commission', 'commissions',
                'committee', 'committees', 'communal', 'commune', 'communes', 'communities', 'companion',
                'companionable', 'companions', 'companionship', 'comparable', 'comparably', 'compatibilities', 'compatibility',
                'compatible', 'complement', 'complemented', 'complementing', 'complements', 'complied', 'complies', 'compliment',
                'compliments', 'comply', 'complying', 'composite', 'composites', 'compromise', 'compromised',
                'compromises', 'compromising', 'comrade', 'comrades', 'concede', 'conceded', 'concedes', 'conceding', 'concert',
                'concerted', 'concession', 'concessions', 'concur', 'concurred', 'concurrent', 'concurring', 'concurs',
                'confirm', 'confirmation', 'confirmations', 'confirmed', 'confirming', 'confirms', 'conform',
                'conformed', 'conforming', 'conforms', 'congenial', 'congregate', 'congregates', 'congregating', 'congregations',
                'conjoin', 'conjoined', 'conjoining', 'conjoins', 'conjunction', 'conjunctions', 'connect', 'connected',
                'connecting', 'connection', 'connections', 'connects', 'consensus', 'consent', 'consented',
                'consenting', 'consents', 'consistencies', 'consistency', 'consistent', 'consolidate', 'consolidated', 'consolidates',
                'consolidating', 'consolidation', 'consolidations', 'consonance', 'conspiracies', 'conspiracy',
                'conspire', 'conspired', 'conspires', 'constant', 'contact', 'contacted', 'contacting', 'context', 'continual',
                'continuous', 'contracted', 'contracting', 'contributed', 'contributes', 'contribution',
                'contributions', 'convene', 'convened', 'convenes', 'convening', 'converge', 'converged', 'converges', 'converging',
                'cooperate', 'cooperated', 'cooperates', 'cooperation', 'cooperative', 'cooperatively', 'coordinate',
                'coordinated', 'coordinates', 'coordinating', 'coordination', 'copied', 'copies', 'copy', 'copying',
                'cordial', 'correlate', 'correlated', 'correlates', 'correlating', 'correlation', 'correlations',
                'corresponding', 'covenant', 'covenants', 'cronies', 'crony', 'culture', 'customary', 'customs',
                'dealings', 'definite', 'definitive', 'dependable', 'dependence', 'dependent', 'devote', 'devoted', 'devotes',
                'devoting', 'discrete', 'disparate', 'disposition', 'distinct', 'distinctive', 'divergent', 'diverse',
                'dominant', 'donate', 'donated', 'donates', 'donation', 'donations', 'duplicate', 'duplicated',
                'duplicates', 'duplicating', 'echo', 'echoed', 'echoes', 'echoing', 'elemental', #-------------------?
                'embrace', 'embraced', 'embraces', 'embracing', 'empathize', 'empathized', 'empathizes', 'empathizing', 'empathy',
                'endorse', 'endorsed', 'endorses', 'endorsing', 'enduring', 'environ', 'equal', 'equalities',
                'equality', 'equally', 'equate', 'equated', 'equating', 'equidistant', 'equivalence', 'equivalent', 'essential',
                'eternal', 'everybody', 'exchange', 'exchanged', 'exchanges', 'exchanging', 'experience', 'explicit',
                'express', 'facilitate', 'facilitated', 'facilitates', 'facilitating', 'faithful', 'familiar',
                'familiarity', 'families', 'federation', 'federations', 'feeling', 'fellowship', 'fellowships', 'focal',
                'folklore', 'folkways', 'foremost', 'friendliness', 'friendship', 'friendships', 'fundamental', 'fuse',
                'fused', 'fusing', 'fusion', 'genuine', 'get-together', 'get-togethers', 'give-and-take', 'go-between',
                'habitual', 'help', 'helped', 'helping', 'helpmate', 'helpmates', 'helps', 'homogeneity', 'homogeneous',
                'hospitable', 'hospitality', 'identical', 'illustrative', 'immutable', 'important', 'incessant',
                'include', 'included', 'includes', 'including', 'inclusion', 'incorporate', 'incorporated', 'incorporates',
                'incorporating', 'indispensable', 'indulge', 'indulged', 'indulgence', 'indulgences', 'indulges',
                'indulging', 'inherent', 'inmost', 'inner', 'integrate', 'integrated', 'integrates', 'integrating',
                'integration', 'interact', 'interacted', 'interacting', 'interaction', 'interactions', 'intercede',
                'interceded', 'intercedes', 'interceding', 'interchangeable', 'interconnect', 'interconnected',
                'interconnecting', 'interconnection', 'interconnections', 'interconnects', 'intercourse', 'interior',
                'intermesh', 'intermeshed', 'intermeshes', 'intermeshing', 'interrelate', 'interrelated',
                'interrelating', 'interrelations', 'intersect', 'intersected', 'intersecting', 'intersection', 'intersections',
                'intertwine', 'intertwined', 'intertwines', 'intertwining', 'intimacies', 'intimacy', 'intimate', 'intrinsic',
                'invariable', 'join', 'joined', 'joining', 'joins', 'joint', 'junction', 'junctions', 'key', 'kindred',
                'kinship', 'lasting', 'leading', 'liaison', 'liaisons', 'like-minded', 'like-mindedness', 'likeness',
                'likenesses', 'likewise', 'lineage', 'link', 'linked', 'linking', 'links', 'lucid', 'main', 'marked',
                'master', 'matched', 'matching', 'mate', 'mated', 'mates', 'mating', 'mediate', 'mediated', 'mediates',
                'mediating', 'medium', 'meetings', 'milieu', 'mingle', 'mingled', 'mingling', 'mood', 'mutual',
                'mutuality', 'negotiable', 'negotiate', 'negotiated', 'negotiating', 'negotiation', 'negotiations', 'networked',
                'networking', 'networks', 'noticeable', 'offer', 'offered', 'offering', 'offers', 'oneness',
                'organization', 'organizational', 'orientation', 'our', 'ourself', 'ourselves', 'palatable', 'parallel', 'parallels',
                'paramount', 'parity', 'partake', 'partakes', 'partaking', 'participate', 'participated',
                'participates', 'participation', 'particular', 'parties', 'partner', 'partners', 'partnership', 'partnerships',
                'partook', 'party', 'party-line', 'patent', 'patronage', 'peculiar', 'peer', 'peers', 'permanent', 'permission',
                'permit', 'permits', 'permitted', 'permitting', 'perpetual', 'persevering', 'persistent', 'pivotal',
                'pledge', 'pledged', 'pledges', 'pledging', 'predominant', 'primary', 'prime', 'principle',
                'public-interest', 'public-service', 'public-spirited', 'rapport', 'ratified', 'ratifies', 'ratify',
                'reciprocal', 'reciprocate', 'reciprocated', 'reciprocates', 'reciprocating', 'reciprocation',
                'reciprocity', 'recognizable', 'recruit', 'recruited', 'recruiting', 'recruits', 'regular', 'relate',
                'related', 'relates', 'relating', 'relations', 'relationship', 'relationships', 'rendezvous',
                'reproduce', 'reproduced', 'reproduces', 'reproducing', 'resemblance', 'resemblances', 'resemble', 'resembled',
                'resembling', 'resolute', 'reunite', 'reunited', 'reuniting', 'salient', 'same', 'sameness', 'scene',
                'schoolmate', 'schoolmates', 'self-denial', 'self-denying', 'self-effacement', 'self-effacing',
                'self-sacrifice', 'self-sacrificing', 'selfless', 'selfsame', 'setting', 'share', 'shared', 'shares',
                'sharing', 'significant', 'similar', 'similarities', 'sisterhood', 'sisterhoods', 'situation',
                'sociability', 'sociable', 'socialization', 'socialize', 'socialized', 'socializing', 'special',
                'specific', 'spirit', 'stable', 'staunch', 'steadfast', 'steady', 'subscribe', 'subscribed', 'subscribes',
                'subscribing', 'sufferance', 'surroundings', 'symmetrical', 'symmetry', 'sympathize', 'sympathized',
                'sympathizes', 'sympathizing', 'sympathy', 'synchronize', 'synchronized', 'synchronizes',
                'synchronizing', 'synchronous', 'syndicate', 'syndicates', 'synonymous', 'syntheses', 'synthesis', 'synthetic',
                'tantamount', 'teamed', 'teaming', 'teammate', 'teammates', 'teams', 'teamwork', 'temperament', 'tenor', 'terrain',
                'territory', 'their', 'them', 'they', 'tie-in', 'tie-ins', 'timbre', 'together', 'tolerance',
                'tolerant', 'tolerate', 'tolerates', 'tolerating', 'toleration', 'tone', 'townspeople', 'turf', 'twin', 'twins',
                'unalterable', 'unambiguous', 'unanimity', 'unanimous', 'unchanging', 'underlying', 'unequivocal',
                'unfailing', 'unflagging', 'unflappable', 'unfluctuating', 'unification', 'unified', 'uniform', 'unify',
                'unifying', 'uninterrupted', 'unions', 'unique', 'unison', 'unit', 'unite', 'unites', 'uniting',
                'units', 'unity', 'unmistakable', 'unrelenting', 'unremitting', 'unties', 'unvarying', 'unwavered', 'unwavering',
                'us', 'vital', 'vouch', 'vouched', 'vouches', 'vouching', 'warrant', 'warranted', 'warranting',
                'warrants', 'we', 'well-beloved', 'well-disposed', 'well-inclined', 'well-loved', 'well-wisher', 'well-wishers',
                'whole', 'wholly', 'willing', 'willingly']
        self.dictionaries = []
        self.dictionaries_names = []
        self.dictionaries_labels = []
        self.active_dictionaries = []
        self.corpora = []
        self.corpora_names = []
        self.corpora_labels = []
        self.active_corpora = []
        self.counts = []
        self.counters = []
        self.total_word_counts = []
        self.scores = []

    def add_corpus(self, filepath):
        file_name = ntpath.basename(filepath)
        self.corpora_names.append(file_name)
        self.corpora_labels.append(ntpath.basename(strip_file_extension(file_name)))
        corpus = self.utf8_to_ascii(read_txt(filepath)).decode('unicode_escape').encode('ascii', 'ignore')
        self.corpora.append(corpus)
        self.active_corpora.append(1)
        self.total_word_counts.append(len(str(corpus).split(" ")))

    def delete_corpus(self, index):
        del self.corpora[index]
        del self.corpora_names[index]
        del self.active_corpora[index]

    def delete_dictionary(self, index):
        del self.dictionaries[index]
        del self.dictionaries_names[index]
        del self.active_dictionaries[index]

    def deactivate_corpus(self, index):
        self.active_corpora[index] = 0

    def activate_corpus(self, index):
        self.active_corpora[index] = 1

    def deactivate_dictionary(self, index):
        self.active_dictionaries[index] = 0

    def activate_dictionary(self, index):
        self.active_dictionaries[index] = 1

    def scrub_list(self, lst):
        lst = list(map(lambda x: x.lower(), lst))
        return lst.sort(key=lambda x: len(x.split()), reverse=True)

    def utf8_to_ascii(self, text):
        text = text.replace(u'\u2014', '-')
        text = text.replace(u'\u2013', '-')
        exclude = set('!"#$%&()*+,./:;<=>?@[\]^_`{|}~')
        exclude.add(u'\u2018')  # '
        exclude.add(u'\u2019')  # '
        exclude.add(u'\u201c')  # "
        exclude.add(u'\u201d')  # "
        exclude.add(u'\u2022')  # bullet point
        exclude.add(u'\u2026')  # ...
        for c in exclude:
            text = text.replace(c, ' ')
        return text

    def add_dictionary(self, file_path):
        file_name = ntpath.basename(file_path)
        self.dictionaries_names.append(file_name)
        self.dictionaries_labels.append(ntpath.basename(strip_file_extension(file_name)))
        if get_file_type(file_path) == ".csv":
            with open(file_path, 'rb') as f:
                reader = csv.reader(f)
                rows = list(reader)
            new_list = []
            for row in rows:
                for cell in row:
                    cell = cell.strip()
                    new_list.append(cell)
        elif get_file_type(file_path) == ".txt":
            new_list = read_txt(file_path)
            new_list = new_list.split(", ")
            new_list = map(lambda x: x.encode("utf-8"), new_list)
        new_list.sort(key=lambda x: len(x.split()), reverse=True)
        self.dictionaries.append(new_list)
        self.active_dictionaries.append(1)

    def count_words(self):
        #delete previous results
        self.counts = []
        self.counters = []
        self.scores = []
        corpora = self.corpora
        for corpus in corpora:
            counts = []
            for i in range(len(self.dictionaries)):
                if self.active_dictionaries[i] == 1:
                    count = 0
                    for word in self.dictionaries[i]:
                        if corpus.startswith(word + " "):
                            count += 1
                        if corpus.endswith(" " + word + "\n") or corpus.endswith(" " + word):
                            count += 1
                        count += len(re.findall(" " + word + " ", corpus))
                        if ' ' in word:
                            corpus = corpus.replace(word, " ")
                    counts.append(count)
            self.counters.append(counts)

    def generate_scores(self):
        index = 0
        for counts in self.counters:
            sum = 0.0
            for count in counts:
                sum += count
            self.scores.append(sum/self.total_word_counts[index])
            index += 1

    def to_html(self):
        result = "<table id='analyze_table'><tr id='header'>"
        result += "<td align='center'>file</td>"
        for i in range(len(self.dictionaries_names)):
            if self.active_dictionaries[i] == 1:
                result += "<td align='center'>" + self.dictionaries_labels[i] + "</td>"
        result += "<td align='center'>total word count</td>"
        result += "<td align='center'>score</td>"
        result += "</tr><tr>"

        for i in range(len(self.corpora_names)):
            if self.active_corpora[i] == 1:
                result += "</tr>"
                if i % 2 == 0:
                    result += "<tr id='even'>"
                else:
                    result += "<tr id='odd'>"
                result += "<td align='center'>" + self.corpora_labels[i] + "</td>"
                for counts in self.counters[i] + [self.total_word_counts[i]] + [self.scores[i]]:
                    result += "<td align='center'>" + str(counts) + "</td>"
        result += "</tr></table>"
        return result

    def display(self):
        matrix = self.to_matrix()
        for row in matrix:
            print row

    def to_matrix(self):
        header = []
        header.append("file")
        for i in range(len(self.dictionaries_names)):
            if self.active_dictionaries[i] == 1:
                header.append(self.dictionaries_names[i])
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
                row.append(self.total_word_counts[i])
                row.append(self.scores[i])
                matrix.append(row)
        return matrix

    def save_to_csv(self):
        matrix = self.to_matrix()
        with open('results.csv', 'wb') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for row in matrix:
                spamwriter.writerow(row)
        csvfile.close()

    def save_list(self, list_name):
        index = -1
        count = 0
        for lst in self.dictionaries_names:
            if lst == list_name:
                index = count
            count += 1
        if index == -1:
            print "\nList", list_name, "not found"
        else:
            with open("Dictionaries/" + self.dictionaries_names[index], 'w') as file:
                file.write(", ".join(self.dictionaries[index]))
            file.close()


def read_txt(filepath):
    try:
        with open(filepath, 'r') as myfile:
            return myfile.read().decode("utf-8").lower()
    except IOError:
        print "could not read", filepath


def read_csv(filepath):
    result = ""
    with open(filepath, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            result += ', '.join(row)
        print result
    return result


def main():
    pass

if __name__ == "__main__":
    main()
