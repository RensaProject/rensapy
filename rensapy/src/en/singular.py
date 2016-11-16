# SINGULAR - last updated for NodeBox 1.9.4

# Adapted from Bermi Ferrer's Inflector for Python:
# http://www.bermi.org/inflector/

# Copyright (c) 2006 Bermi Ferrer Martinez
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software to deal in this software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of this software, and to permit
# persons to whom this software is furnished to do so, subject to the following
# condition:
#
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THIS SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THIS SOFTWARE.

import re

singular_rules = [
    ['(?i)(.)ae$' , '\\1a'],
    ['(?i)(.)itis$' , '\\1itis'],
    ['(?i)(.)eaux$' , '\\1eau'],
    ['(?i)(quiz)zes$' , '\\1'],
    ['(?i)(matr)ices$' , '\\1ix'],
    ['(?i)(vert|ind)ices$' , '\\1ex'],
    ['(?i)^(ox)en' , '\\1'],
    ['(?i)(alias|status)es$' , '\\1'],
    ['(?i)([octop|vir])i$' , '\\1us'],
    ['(?i)(cris|ax|test)es$' , '\\1is'],
    ['(?i)(shoe)s$' , '\\1'],
    ['(?i)(o)es$' , '\\1'],
    ['(?i)(bus)es$' , '\\1'],
    ['(?i)([m|l])ice$' , '\\1ouse'],
    ['(?i)(x|ch|ss|sh)es$' , '\\1'],
    ['(?i)(m)ovies$' , '\\1ovie'],
    ['(?i)ombies$' , '\\1ombie'],
    ['(?i)(s)eries$' , '\\1eries'],
    ['(?i)([^aeiouy]|qu)ies$' , '\\1y'],

	# Certain words ending in -f or -fe take -ves in the plural (lives, wolves).
    ["([aeo]l)ves$", "\\1f"],
    ["([^d]ea)ves$", "\\1f"],
    ["arves$", "arf"],
    ["erves$", "erve"],
    ["([nlw]i)ves$", "\\1fe"],   
    ['(?i)([lr])ves$' , '\\1f'],
    ["([aeo])ves$", "\\1ve"],
    ['(?i)(sive)s$' , '\\1'],
    ['(?i)(tive)s$' , '\\1'],
    ['(?i)(hive)s$' , '\\1'],
    ['(?i)([^f])ves$' , '\\1fe'],
    
    ['(?i)(^analy)ses$' , '\\1sis'],
    ['(?i)((a)naly|(b)a|(d)iagno|(p)arenthe|(p)rogno|(s)ynop|(t)he)ses$' , '\\1\\2sis'],
    ['(?i)(.)opses$' , '\\1opsis'],
    ['(?i)(.)yses$' , '\\1ysis'],
    ['(?i)(h|d|r|o|n|b|cl|p)oses$' , '\\1ose'],
    ['(?i)(fruct|gluc|galact|lact|ket|malt|rib|sacchar|cellul)ose$' , '\\1ose'],
    ['(?i)(.)oses$' , '\\1osis'],
    
    ['(?i)([ti])a$' , '\\1um'],
    ['(?i)(n)ews$' , '\\1ews'],
    ['(?i)s$' , ''],
];

singular_uninflected = ["bison", "bream", "breeches", "britches", "carp", "chassis", "clippers", "cod", "contretemps", "corps", "debris", "diabetes", "djinn", "eland", "elk", "flounder", "gallows", "graffiti", "headquarters", "herpes", "high-jinks", "homework", "innings", "jackanapes", "mackerel", "measles", "mews", "mumps", "news", "pincers", "pliers", "proceedings", "rabies", "salmon", "scissors", "series", "shears", "species", "swine", "trout", "tuna", "whiting", "wildebeest"]
singular_uncountable = ["advice", "bread", "butter", "cheese", "electricity", "equipment", "fruit", "furniture", "garbage", "gravel", "happiness", "information", "ketchup", "knowledge", "love", "luggage", "mathematics", "mayonnaise", "meat", "mustard", "news", "progress", "research", "rice", "sand", "software", "understanding", "water"]

singular_ie = ["algerie", "auntie", "beanie", "birdie", "bogie", "bombie", "bookie", "cookie", "cutie", "doggie", "eyrie", "freebie", "goonie", "groupie", "hankie", "hippie", "hoagie", "hottie", "indie", "junkie", "laddie", "laramie", "lingerie", "meanie", "nightie", "oldie", "^pie", "pixie", "quickie", "reverie", "rookie", "softie", "sortie", "stoolie", "sweetie", "techie", "^tie", "toughie", "valkyrie", "veggie", "weenie", "yuppie", "zombie"]

singular_irregular = {
    "men" : "man",
    "people" : "person",
    "children" : "child",
    "sexes" : "sex",
    "moves" : "move",
    "teeth" : "tooth",
    "geese" : "goose",
    "feet" : "foot",
    "zoa" : "zoon",
    "atlantes" : "atlas", 
    "atlases" : "atlas", 
    "beeves" : "beef", 
    "brethren" : "brother", 
    "children" : "child", 
    "corpora" : "corpus", 
    "corpuses" : "corpus", 
    "kine" : "cow", 
    "ephemerides" : "ephemeris", 
    "ganglia" : "ganglion", 
    "genii" : "genie", 
    "genera" : "genus", 
    "graffiti" : "graffito", 
    "helves" : "helve",
    "leaves" : "leaf",
    "loaves" : "loaf", 
    "monies" : "money", 
    "mongooses" : "mongoose", 
    "mythoi" : "mythos", 
    "octopodes" : "octopus", 
    "opera" : "opus", 
    "opuses" : "opus", 
    "oxen" : "ox", 
    "penes" : "penis", 
    "penises" : "penis", 
    "soliloquies" : "soliloquy", 
    "testes" : "testis", 
    "trilbys" : "trilby", 
    "turves" : "turf", 
    "numena" : "numen", 
    "occipita" : "occiput", 
}

# Prepositions are used to solve things like
# "mother-in-law" or "man-at-arms"
plural_prepositions = ["about", "above", "across", "after", "among", "around", "at", "athwart", "before", "behind", "below", "beneath", "beside", "besides", "between", "betwixt", "beyond", "but", "by", "during", "except", "for", "from", "in", "into", "near", "of", "off", "on", "onto", "out", "over", "since", "till", "to", "under", "until", "unto", "upon", "with"]

def singular(word, custom={}):

    if word in custom.keys():
		return custom[word]

	# Recursion of compound words (e.g. mothers-in-law). 
    if "-" in word:
        words = word.split("-")
        if len(words) > 1 and words[1] in plural_prepositions:
	        return singular(words[0], custom)+"-"+"-".join(words[1:])

    lower_cased_word = word.lower()
    for w in singular_uninflected:
        if w.endswith(lower_cased_word):
            return word
    for w in singular_uncountable:
        if w.endswith(lower_cased_word):
            return word
    for w in singular_ie:
        if lower_cased_word.endswith(w+"s"):
            return w

    for w in singular_irregular.keys():
        match = re.search('('+w+')$',word, re.IGNORECASE)
        if match:
            return re.sub(
                '(?i)'+w+'$', 
                singular_irregular[w], word)

    for rule in range(len(singular_rules)):
        match = re.search(singular_rules[rule][0], word, re.IGNORECASE)
        if match:
            groups = match.groups()
            for k in range(0,len(groups)):
                if groups[k] == None:
                    singular_rules[rule][1] = singular_rules[rule][1].replace('\\'+str(k+1), '')
            return re.sub(
                singular_rules[rule][0], 
                singular_rules[rule][1], word)

    return word

def noun_singular(word, custom={}):
    return singular(word, custom)
