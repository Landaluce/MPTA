import csv
import itertools
import re

opportunity = ["advantage", "befalling", "break", "chance","connection",
               "contingency", "convenience", "cut", "fair shake", "favorable",
               "fighting chance", "fitness", "fling", "fortuity", "hope",
               "luck", "recourse", "advancement", "break", "chance", "favorable",
               "fortune", "occasion", "opening", "possibility", "prospect",
               "prosperity", "time", "turn", "stimulating", "successful",
               "viable", "chance", "expect", "expectation", "expects", "expediency",
               "favorability", "favorable", "luck", "momentum", "momentus", "opportune",
               "opportunisitic", "opportunities", "opportunity", "optimism", "optimist",
               "optimistic", "outlook", "prospects", "suitable", "upbeat", "advancement",
                "break", "chance", "favorable", "fortune", "occasion", "opening",
               "possibility", "prospect", "prosperity", "time", "turn", "stimulating",
               "successful", "viable","advantage", "befalling", "break", "chance",
               "connection", "contingency", "convenience", "cut", "fair shake", "favorable",
               "fighting chance", "fitness", "fling", "fortuity", "hope", "luck", "recourse",
               "chance", "expect", "expectation", "expects", "expediency", "favorability",
               "favorable", "luck", "momentum", "momentus", "opportune", "opportunisitic",
               "opportunities", "opportunity", "optimism", "optimist", "optimistic", "outlook",
               "prospects", "suitable", "upbeat","advancement", "advantage","befalling",
               "break", "chance", "connection", "contingency", "convenience", "cut", "expect",
               "expectation", "expects", "expediency", "fair shake", "favorability", "favorable",
               "fighting chance", "fitness", "fling", "fortuity", "fortune", "hope", "luck",
               "momentum",  "momentous", "occasion", "opening", "opportune", "opportunistic",
               "opportunities", "opportunity", "optimism", "optimist", "optimistic", "outlook",
               "possibility", "prospect", "prospects", "prosperity", "prosperous", "recourse",
               "stimulating", "successful", "suitable", "time", "turn", "upbeat", "viable"]

threat = ["alarming fateful", "apocalyptic", "baleful", "baneful", "black",
          "cautionary", "challenging", "comminatory", "crisis", "dangerous",
          "demur", "dire", "grim", "ill-boding", "imminent", "impendent",
          "impending", "inauspicious", "intimidating", "looming", "loury",
          "lowering", "lowery", "minacious", "minatory", "portending", "portent",
          "sinister", "trial dire", "ugly", "unlucky", "unpropitious", "unsafe",
          "warning","assault", "conflict", "constrained", "crisis", "crunch", "danger",
          "foreboding", "hazard", "jeopardy", "loss", "menace", "negative", "omen", "peril",
          "portent", "risk", "stressful", "sword of damocles", "urgent","assault", "conflict",
          "constrained", "crisis", "crunch", "danger", "foreboding", "hazard", "jeopardy",
          "loss", "menace", "negative", "omen", "peril", "portent", "risk", "stressful",
          "sword of damocles", "urgent", "alarming", "apocalyptic", "baneful", "black",
          "cautionary", "challenging", "comminatory", "crisis", "dangerous", "demur", "dire",
          "grim", "ill-boding", "imminent", "impendent", "impending", "inauspicious",
          "intimidating", "looming", "loury", "lowering", "lowery", "minacious", "minatory",
          "portending", "portent", "sinister", "trial dire", "ugly", "unlucky", "unpropitious",
          "unsafe", "warning", "fateful", "demur", "dire", "fateful", "foreboding", "grim",
          "hazard", "ill-boding", "imminent", "impendent", "impending", "inauspicious",
          "intimidating", "jeopardy", "looming", "loss", "loury", "lowering", "lowery", "menace",
          "minacious", "minatory", "negative", "omen", "peril", "portending", "portent", "risk",
          "sinister", "stressful", "sword of damocles", "trial dire", "ugly", "unlucky",
          "unpropitious", "unsafe", "urgent", "warning"]

enactment = ["aggrandizement", "amplif", "augment", "cultivate", "develop", "develops",
             "developing", "DILATION", "DISTENTION", "ENLARGE", "EXPAND", "EXPANDS", "EXPANSION",
             "EXTENSION", "GRADUALLY INCREASE", "GRADUAL INCREASE", "GROW", "GROWS", "GROWTH",
             "PLANTED", "PROGRESSION", "PROGRESS", "TURGESCENCE", "ACQUIRE", "ACQUISITION",
             "AMALGAMAT", "COALESCE", "INVESTMENT BANKER", "MERGE", "POOL", "PROCEEDS", "SYNDICATE",
             "PURCHASE", "accomplish", "achieve", "act", "action", "active", "activity", "alacrity",
             "alertness", "battle", "combat", "commission", "conflict", "contest", "encounter", "engage",
             "engagement", "enterprise", "execute", "exercise", "exert", "exploit", "fight", "force",
             "influence", "intervene", "intervention", "maneuver", "manipulate", "move", "occupy",
             "operate", "operation", "perform", "proceed", "process", "react", "respond", "rush",
             "stir", "thrust", "transact", "undertake", "absorb", "affiliate", "ally", "assimilate",
             "blend", "cement", "centralize", "coalesce", "combine", "compound", "conglomerate",
             "consolidate", "converge", "fuse", "incorporate", "intermingle", "join", "league",
             "marry", "meld", "mingle", "network", "pool", "synthesize", "team", "team up", "unite",
             "access", "accrue", "achieve", "acquire", "amalgamate", "amass", "annex", "attain",
             "procure", "secure", "accomplish", "achieve", "actualize", "attain", "complete", "consummate",
             "effect", "enact", "execute", "finish", "fulfill", "manage", "realize", "resolve", "win",
             "appeal", "attack", "attribute", "censure", "charge", "cite", "complain", "contend", "contest",
             "denounce", "dispute", "impeach", "implicate", "impute", "incriminate", "inculpate", "indict",
             "prosecute", "resist", "rival", "strive", "struggle", "vie", "lobby", "advance", "affect",
             "agitate", "alter", "barnstorm", "boost", "campaign", "change", "crusade", "exert", "further",
             "induce", "influence", "lobby", "modify", "persuade", "pitch", "plug", "politick", "press",
             "pressure", "procure", "promote", "request", "solicit", "sway", "urge", "bankrupt",
             "deconstruct", "disassemble", "disinherit", "dismantle", "divest", "divestiture", "forfeit",
             "oust", "relinquish", "remove", "sacrifice", "sell", "separate", "Environment",
             "environs", "industry", "market", "niche", "nook", "province", "purview", "region", "scope",
             "sector", "terrain", "territory"]

org_iden = ["abiding", "acclimated", "acclimation", "accountability", "accountable", "accustomed",
            "all-inclusive", "authentic", "authenticity", "authorized", "base", "basics",
            "bureaucracies", "bureaucracy", "bureaucrat", "centers", "central", "centralization",
            "center", "changeless", "characteristic", "characteristically", "characteristics",
            "chief", "chiefly", "chronic", "chronically", "climate", "climates", "clone", "clones",
            "code", "codes", "common", "commonality", "commonly", "commonplace", "comprehensive",
            "comprehensively", "comprise", "comprised", "comprises", "comprising", "concentrated",
            "conditioned", "confined", "confining", "conform", "conformed", "conformity", "congruence",
            "congruent", "consistencies", "consistency", "consistent", "constancy", "constant", "constantly",
            "continuation", "continuities", "continuity", "conventional", "conventionally", "core",
            "correct", "correctly", "custom", "customarily", "customary", "customs", "decorum",
            "deep-seated", "destinies", "destiny", "domestic", "domesticated", "due-process",
            "element", "elementary", "elements", "enduring", "entitled", "entitlement", "entitlements",
            "entrenched", "entrenchment", "environment", "essence", "essential", "essentials",
            "established", "establishment", "example", "examples", "exemplified", "exemplify",
            "expected", "expectedly", "extensive", "extensively", "familiarize", "familiarized",
            "familiarizes", "familiarizing", "foundation", "foundational", "foundations",
            "fundamental", "fundamentals", "general", "generalities", "generality", "generalizable",
            "generalization", "generalizations", "generalize", "generalized", "generally", "grassroots",
            "grass-roots", "groove", "grooves", "grounding", "habit", "habits", "habitual",
            "habitually", "habituated", "homebody", "home-grown", "homemade", "humanity", "humankind",
            "identical", "identities", "identity", "incumbency", "incumbent", "incumbents",
            "indigenous", "inevitability", "inevitable", "ingrained", "innate", "innately", "inner",
            "inside", "interior", "internal", "internally", "intrinsic", "intrinsically", "invariability",
            "invariable", "inveterate", "inveterately", "involuntary", "inward", "inwardly", "inwards",
            "kernel", "kernels", "landmark", "landmarks", "lasting", "lawful", "legitimacy", "legitimate",
            "legitimated", "legitimately", "legitimating", "limited", "long-standing", "main",
            "mainly", "mainstream", "maintain", "maintained", "maintaining", "maintains",
            "maintenance", "majorities", "majority", "mandate", "mandated", "mandates",
            "mankind", "matter-of-fact", "methodical", "native", "native-born", "natives",
            "natural", "naturalize", "naturalized", "naturally", "norm", "normal", "normalcy",
            "normalities", "normality", "normative", "normatively", "norms", "nucleus",
            "obligatory", "oblige", "obliged", "obliges", "obliging", "officeholder", 
            "officeholders", "oneness", "ordered", "ordinary", "organize", "organized",
            "organizes", "orthodox", "orthodoxy", "paradigm", "paradigms", "pattern",
            "patterned", "patterns", "perennial", "perennially", "permanent", "permanently",
            "persistent", "persistently", "plainly", "pre-arranged", "preconceived",
            "predictability", "predictable", "predominant", "preordained", "prescribed",
            "prevalence", "prevalent", "primarily", "primary", "proverbial", "proverbially",
            "rampant", "rampantly", "ratified", "ratifies", "ratify", "ratifying", "recognized",
            "recurrent", "recurrently", "regime", "regular", "regularities", "regularity",
            "regularly", "reliability", "reliable", "reliably", "repeat", "repeated",
            "repeatedly", "repeating", "repeats", "representative", "require", "required",
            "requires", "requiring", "rhythmic", "rhythmically", "routine", "routinely",
            "rule", "rules", "rut", "ruts", "sanction", "sanction able", "sanctioned",
            "sanctioning", "sanctions", "single-issue", "stability", "stable", "standard",
            "standard-bearer", "standardize", "standardized", "standardizing", "standards",
            "steadfast", "steadfastly", "steadier", "steadiest", "steadily", "steady",
            "substantiate", "substantiated", "substantiates", "substantiating", "substantive",
            "substantively", "systematic", "systematically", "thematic", "thematically", "theme",
            "themes", "trait", "traits", "typical", "typified", "typifies", "typify", "typifying",
            "unadulterated", "unanimity", "unanimous", "unavoidable", "unavoidably", "unchangeable",
            "underlying", "unexceptional", "unified", "unifies", "uniform", "uniformities", "uniformity",
            "uniformly", "unify", "unifying", "uninterruptedly", "universal", "universalize", "universally",
            "usual", "usually", "valid", "validated", "validly", "womankind"]

#Uploading all Organizational Identity words into a list called new_list
empt_list = []
iter_count = 0
with open('OrgID.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter= ' ')
    for row in reader:
        empt_list.append(row)
        iter_count += 1
    org_iden = list(itertools.chain(*empt_list))
    print org_iden
    print iter_count

def scrub_list(lst):
    for i in lst:
        i = i.lower()
    lst = list(sorted(set(lst)))
    return lst


print len(opportunity)
opportunity = scrub_list(opportunity)
print len(opportunity)
print len(threat)
threat = scrub_list(threat)
print len(threat)
print len(enactment)
enactment = scrub_list(enactment)
print len(enactment)



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

    pass


if __name__ == "__main__":
    main()
