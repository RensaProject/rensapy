'''
This file helps to realize some basic types of assertions into natural text.
 - realize_brain_assertion(brain, a, isFragment) will realize an assertion a given a brain context.
 - realize_assertion(a, isFragment) will realize an assertion on its own as best as it can.

If the assertion is too complex to be translated into natural English by this simple realizer, both functions return an empty string.  In this case, you can use the functions to_dict() or to_pruned_dict() to print the contents of your assertion.

'''

import numbers
import en
import Assertion
from Entity import *
from data.wordCategories import *

def translate_owner_assertion(brain,a):
    toReturn = list_concepts_naturally(brain, a.owner) + " knows that "
    return toReturn

def translate_believed_assertion(brain,a):
    toReturn = list_concepts_naturally(brain, a.believer) + " believes that "
    return toReturn

# Realize an assertion "a" given a brain context "brain".
# If isFragment is false, will realize as a complete sentence.
# If isFragment is true, will realize without capitalizing the first letter, and
# will remove the last terminating punctuation.
def realize_brain_assertion(brain,a,isFragment):
    # try:
    toReturn = ""
    if is_owned_assertion(a):
        toReturn = translate_owner_assertion(brain,a)
    if is_believed_assertion(a):
        toReturn += translate_believed_assertion(brain,a)
    if is_discourse_assertion(a):
        toReturn += translate_discourse_assertion(brain,a,isFragment)
    elif is_action_assertion(a):
        toReturn += translate_action_assertion(brain,a)
    elif is_is_a_assertion(a):
        toReturn += translate_is_a_assertion(brain,a)
    elif is_located_assertion(a):
        toReturn += translate_located_assertion(brain,a)
    elif is_x_of_assertion(a):
        toReturn += translate_x_of_assertion(brain,a)
    elif is_has_assertion(a) or is_has_a_assertion(a):
        toReturn += translate_has_assertion(brain,a)
    elif is_has_x_assertion(a):
        toReturn += translate_has_x_assertion(brain,a)
    elif is_pf_assertion(a):
        toReturn += translate_pf_assertion(brain,a)
    elif is_x_for_assertion(a):
        toReturn += translate_x_for_assertion(brain,a)
    elif is_set_x_assertion(a):
        toReturn += translate_set_x_assertion(brain,a)
    elif is_implies_assertion(a):
        toReturn += translate_implies_assertion(brain,a)
    elif is_cause_assertion(a):
        toReturn += translate_cause_assertion(brain,a)

    elif is_verb_assertion(a):
        toReturn += translate_verb_assertion(brain,a)

    # Return the final realization, with the first letter capitalized.
    if toReturn=="":
        return toReturn
    else:
        if isFragment:
            # Remove terminating punctuation.
            return toReturn.rstrip('?:!.,;')
        else:
            # Return full sentence with capitalized first letter.
            return toReturn[0].upper() + toReturn[1:]
    # except:
        # return ""

''' Functions that determine the category of assertion to be realized. '''
# Returns true if every element of list_of_vals is either a string or a string array.
def vals_are_string_things(list_of_vals):
    for l in list_of_vals:
        if get_type(l)!="string" and get_type(l)!="string_array":
            return False
    return True

def is_action_assertion(a):
    return a.relation=="action" #and vals_are_string_things([a.l,a.r])

def is_discourse_assertion(a):
    # Note: we could retrieve these synonyms from WordNet directly (e.g. via en.verb.hypernym('say')), but to acquire a rich list we would already need
    # to have several synonyms under our belt - and we still might not reach a complete list.  Hence, here are some known synonyms for "say":
    saySynonyms = ["say", "sing", "utter", "mumble", "shout", "announce","answer","declare","speak","suggest","allege","affirm","remark",
    "whisper","scream","cheer","yell","shriek","bellow","bark","whoop","call",
    "roar","cry","screech","bawl"]

    actionSay = False
    for s in saySynonyms:
        if s in a.r:
            actionSay = True

    return is_action_assertion(a) and actionSay and hasattr(a,"discourse")

def is_owned_assertion(a):
    return hasattr(a,"owner")

def is_believed_assertion(a):
    return hasattr(a,"believer")

def is_located_assertion(a):
    return a.relation[0:9]=="location_"

def is_set_x_assertion(a):
    return a.relation[0:4]=="set_"

def is_x_of_assertion(a):
    return a.relation[-3:]=="_of"

def is_x_for_assertion(a):
    return a.relation[-4:]=="_for"

def is_has_x_assertion(a):
    return a.relation[0:4]=="has_" # or a.relation[0:8]=="can_has_"

def is_has_assertion(a):
    return a.relation=="has"

def is_has_a_assertion(a):
    return a.relation=="has_a"

def is_implies_assertion(a):
    return en.verb.infinitive(a.relation)=="imply"

def is_cause_assertion(a):
    return en.verb.infinitive(a.relation)=="cause"

def is_pf_assertion(a):
    return a.relation=="precondition_for"

def is_is_a_assertion(a):
    return a.relation=="is_a"

def is_verb_assertion(a):
    return en.is_verb(a.relation)

# TODO: more efficient way to enable this kind of accessible syntax.
def get_condition_xs(a):
    return get_variable_xs(a, "condition_")

def get_location_xs(a):
    return get_variable_xs(a, "location_")

def get_timespan_xs(a):
    return get_variable_xs(a, "timespan_")

def get_variable_xs(a,attributeName):
    xs = []
    length = len(attributeName)
    aDict = a.to_dict()
    for e in aDict.keys():
        if attributeName in e[0:length]:
            xs.append(e[length:])
    return xs

# Example:
# - set_value
def translate_set_x_assertion(brain,a):
    toReturn = ""
    setWhat = a.relation[4:]
    l_owner = ""
    if hasattr(a,"l_owner"):
        l_owner_list = [make_possessive(x) for x in a.l_owner]
        # l_owner = a.l_owner[0] + "'s "
        l_owner = list_concepts_naturally(brain,l_owner_list) + " "
    verb = get_tense(a, "is", a.l, brain)
    if (hasattr(a,"grammatical_mood") and a.grammatical_mood=="imperative"):
        if (a.l==["oven"] and setWhat=="value" and hasattr(a,"r_unit")):
            toReturn = "set the " + list_words_naturally(a.l) + " to " + str(a.r[0]) +" "+ str(a.r_unit)
        else:
            toReturn = "set the " + setWhat + " of " + l_owner + list_words_naturally(a.l) + " to " + str(a.r)
    else:
        toReturn = "the " + setWhat + " of " + l_owner + list_words_naturally(a.l) + " "+verb+" set to " + str(a.r)
        if hasattr(a,"r_unit"):
            toReturn += " " + str(a.r_unit)
    toReturn = add_end_marks(a, toReturn)
    return toReturn

# Examples:
# - Sarah => Sarah's
# - James => James'
def make_possessive(string):
    if string.endswith("s"):
        return string+"'"
    else:
        return string+"'s"

''' Functions that translate assertions by their category. '''
def translate_verb_assertion(brain,a):
    toReturn = ""
    verb = get_tense(a, a.relation, a.l, brain)
    toReturn = list_concepts_naturally(brain,a.l) + " " + verb + " "
    # Assume one number in num_r for now.
    if hasattr(a,"num_r"):
        if isinstance(a.num_r[0],int):
            number = en.number.spoken(a.num_r[0])
        else: # includes if isinstance(a.num_r[0],basestring)
            number = str(a.num_r[0])
        toReturn += number + " "
        newRights = a.r[:]
        if a.num_r[0]==1:
            # Make newRights elements singular.
            for i,nr in enumerate(newRights):
                newRights[i] = en.noun.singular(nr)
        else:
            # Make newRights elements plural.
            for i,nr in enumerate(newRights):
                newRights[i] = en.noun.plural(nr)
        toReturn += list_words_naturally(newRights)
    else:
        toReturn += list_concepts_naturally(brain,a.r)
    adverbs = []
    if hasattr(a, "with_property"):
        for j in range(0, len(a.with_property)):
            adverbs.append(adjective_to_adverb(a.with_property[j]))
    if len(adverbs) > 0:
        toReturn += " " + list_words_naturally(adverbs)
    toReturn = add_end_marks(a, toReturn)
    return toReturn

def translate_discourse_assertion(brain, a, isFragment):
    # For now, we assume there is only one verb used.
    sayVerb = get_tense(a, a.r[0], a.l, brain)
    toReturn = ""
    if isFragment:
        toReturn = list_concepts_naturally(brain, a.l) + " " + sayVerb + ", '" + a.discourse + "'."
    else:
        toReturn = "'" + a.discourse + "' " + list_concepts_naturally(brain, a.l) + " " + sayVerb + ".";
    return toReturn

def translate_action_assertion(brain, a):
    if hasattr(a,"grammatical_mood"):
        if a.grammatical_mood=="imperative":
            toReturn = translate_imperative_action_assertion(brain,a)
        else:
            toReturn = translate_indicative_action_assertion(brain,a)
    else:
        toReturn = translate_indicative_action_assertion(brain,a)

    toReturn = add_end_marks(a, toReturn)
    return toReturn

def translate_imperative_action_assertion(brain,a):
    actions = []
    toReturn = ""
    for i in range(0,len(a.r)):
        verb = get_tense(a, a.r[i], a.l, brain)
        actions.append(verb)
    adverbs = []
    if hasattr(a, "with_property"):
        for j in range(0, len(a.with_property)):
            adverbs.append(adjective_to_adverb(a.with_property[j]))
    toReturn = list_words_naturally(actions)
    if hasattr(a, "action_object") and len(a.action_object)>0:
        # Assume one number in num_action_object for now.
        if hasattr(a,"num_action_object"):
            if isinstance(a.num_action_object[0],int):
                number = en.number.spoken(a.num_action_object[0])
            else:
                number = str(a.num_action_object[0])
            toReturn += " " + number + " "
            newRights = a.action_object[:]
            if a.num_action_object[0]==1:
                # Make newRights elements singular.
                for i,nr in enumerate(newRights):
                    newRights[i] = en.noun.singular(nr)
            else:
                # Make newRights elements plural.
                for i,nr in enumerate(newRights):
                    newRights[i] = en.noun.plural(nr)
            toReturn += list_words_naturally(newRights)
        else:
            toReturn += " " + list_concepts_naturally(brain, a.action_object)
    if hasattr(a, "action_recipient") and len(a.action_object)>0:
        toReturn += " to " + list_concepts_naturally(brain, a.action_recipient)
    if len(adverbs) > 0:
        toReturn += " " + list_words_naturally(adverbs)
    toReturn = add_locations(brain, a, toReturn)
    toReturn += add_conditions(brain,a)
    return toReturn

def translate_indicative_action_assertion(brain,a):
    actions = []
    toReturn = ""
    for i in range(0,len(a.r)):
        verb = get_tense(a, a.r[i], a.l, brain)
        actions.append(verb)
    adverbs = []
    if hasattr(a, "with_property"):
        for j in range(0, len(a.with_property)):
            adverbs.append(adjective_to_adverb(a.with_property[j]))
    toReturn = list_concepts_naturally(brain, a.l) + " " + list_words_naturally(actions)
    if hasattr(a, "action_object_owner"):
        poss_list = []
        for own in a.action_object_owner:
            if own in a.l and len(a.l)==1:
                genderAsserts = brain.get_assertions_with({"l":[own],"relation":"has_gender"})
                if genderAsserts:
                    possToAdd = get_references(genderAsserts[0]["r"][0])[2]
                else:
                    possToAdd = get_references(guess_gender(own))[2]
            else:
                possToAdd = make_possessive(own)
        poss_list.append(possToAdd)
        toReturn += " " + list_concepts_naturally(brain, poss_list)
    if hasattr(a, "action_object") and len(a.action_object)>0:
        if hasattr(a,"num_action_object"):
            if isinstance(a.num_action_object[0],int):
                number = en.number.spoken(a.num_action_object[0])
            else:
                number = str(a.num_action_object[0])
            toReturn += " " + number + " "
            newRights = a.action_object[:]
            if a.num_action_object[0]==1:
                # Make newRights elements singular.
                for i,nr in enumerate(newRights):
                    newRights[i] = en.noun.singular(nr)
            else:
                # Make newRights elements plural.
                for i,nr in enumerate(newRights):
                    newRights[i] = en.noun.plural(nr)
            toReturn += list_words_naturally(newRights)
        else:
            if hasattr(a, "action_object_owner"):
                toReturn += " " + list_words_naturally(a.action_object)
            else:
                toReturn += " " + list_concepts_naturally(brain, a.action_object)
    if hasattr(a, "action_recipient"):
        if hasattr(a, "action_object"):
            toReturn += " to"
        toReturn += " " + list_concepts_naturally(brain, a.action_recipient)
    if len(adverbs) > 0:
        toReturn += " " + list_words_naturally(adverbs)
    toReturn = add_locations(brain, a, toReturn)
    toReturn += add_conditions(brain,a)
    return toReturn

def translate_located_assertion(brain,a):
    # Extract how the left concepts are located.
    howLocated = a.relation[9:]
    # Convert any underscores to spaces.
    howLocated = howLocated.replace("_"," ")
    verb = get_tense(a, "is", a.l, brain)
    toReturn = list_concepts_naturally(brain,a.l) + " "+verb+" " + howLocated + " " + list_concepts_naturally(brain, a.r)
    toReturn = add_end_marks(a, toReturn)
    return toReturn

# Examples:
# - instance_of
# - part_of
# - member_of
# - symbol_of
# - reminds_of
# - capable_of
def translate_x_of_assertion(brain,a):
    prefix = a.relation[:-3]
    prefix_article = en.noun.article(prefix)
    # prefix_article_only = prefix_article.split(" ")[0]
    verb = get_tense(a, "was", a.l, brain)

    toReturn = ""
    if en.is_noun(en.noun.singular(prefix)):
        if is_plural(a.l, brain):
            prefix_article = en.noun.plural(prefix)
        toReturn = list_concepts_naturally(brain,a.l) + " "+verb+" " + prefix_article + " of " + list_words_naturally(a.r)
    elif en.is_verb(en.verb.infinitive(prefix)) and en.verb.infinitive(prefix) !="":
        if hasattr(a,"owner") and len(a.owner)>0:
            owner = list_concepts_naturally(brain, a.owner)
        else:
            owner = "everyone"
        toReturn = list_concepts_naturally(brain, a.l) + " "+prefix +" "+owner+ " of " + list_concepts_naturally(brain, a.r)
    elif en.is_adjective(prefix):
        # TODO for capable_of >> deal with action, action_object, action_recipient...
        # Similar for used_for >> when used_for is action / verbs
        toReturn = list_concepts_naturally(brain,a.l) + " "+verb+" " + prefix + " of " + list_words_naturally(a.r)
    toReturn = add_end_marks(a, toReturn)
    return toReturn

# Example:
# {
#   "l":["power bracelet","boomerang"],
#   "relation":"is_a",
#   "r":["equippable_item"]
# } => The power bracelet and the boomerang are equippable items.
def translate_is_a_assertion(brain,a):
    toReturn = ""
    verb = get_tense(a, "is", a.l, brain)
    article = en.noun.article(a.r[0]).split(" ")[0] + " "
    a.r = [e.replace("_"," ") for e in a.r]
    if is_plural(a.l, brain):
        # Note: took out "if en.is_noun(e.replace("_"," ")) and...".
        # That check limited what got placed in the list.
        a.r = [en.noun.plural(e) for e in a.r if en.noun.plural(e)!=""]
        article = ""
    toReturn = list_concepts_naturally(brain, a.l) + " " + verb + " " + article + list_words_naturally(a.r)
    toReturn = add_end_marks(a, toReturn)
    return toReturn

# Example:
# - used_for
def translate_x_for_assertion(brain,a):
    if hasattr(a,"grammatical_mood"):
        if a.grammatical_mood=="imperative":
            return translate_imperative_x_for_assertion(brain,a)
        else:
            return translate_indicative_x_for_assertion(brain,a)
    else:
        return translate_indicative_x_for_assertion(brain,a)
    return toReturn

def translate_imperative_x_for_assertion(brain,a):
    toReturn=""
    prefix = a.relation[:-4]
    verb = get_tense(a, prefix, a.l, brain)
    if vals_are_string_things(a.r):
        useWords = []
        for useWord in a.r:
            if en.is_verb(useWord):
                useWords.append(en.verb.present_participle(useWord))
            else:
                useWords.append(useWord)
        uses=list_words_naturally(useWords)
        toReturn = verb + " " + list_concepts_naturally(brain,a.l) + " for " + uses
    elif get_type(a.r)=="hash_array":
        if a.l[0]==a.r[0]["l"][0]:
            newRights = []
            for newRight in a.r:
                newRight["tense"] = "present participle"
                newRight["grammatical_mood"] = "imperative"
                newRights.append(newRight)
            newRights = list_clauses_naturally(brain, newRights)
            toReturn = verb + " " + list_concepts_naturally(brain,a.l) + " for " + newRights
    toReturn = add_end_marks(a, toReturn)
    return toReturn

def translate_indicative_x_for_assertion(brain,a):
    toReturn=""
    prefix = a.relation[:-4]
    verb = get_tense(a, "was", a.l, brain)
    if vals_are_string_things(a.r):
        useWords = []
        for useWord in a.r:
            if en.is_verb(useWord):
                useWords.append(en.verb.present_participle(useWord))
            else:
                useWords.append(useWord)
        uses=list_words_naturally(useWords)
        toReturn = list_concepts_naturally(brain,a.l) + " "+verb+" " + prefix + " for " + uses
        toReturn = add_end_marks(a, toReturn)
    elif get_type(a.r)=="hash_array":
        if a.l[0]==a.r[0]["l"][0]:
            newRights = []
            for newRight in a.r:
                newRight["tense"] = "present participle"
                newRight["grammatical_mood"] = "imperative"
                newRights.append(newRight)
            newRights = list_clauses_naturally(brain, newRights)
            toReturn = list_concepts_naturally(brain,a.l) + " "+verb+" " + prefix + " for " + newRights
            toReturn = add_end_marks(a, toReturn)
    return toReturn

# Examples:
# - has_property    >> L has/have the property/properties R.
# - has_name, has_gender, has_belief, has_goal, has_intention, has_value
# - has_secret_identity, has_flavor_profile
def translate_has_x_assertion(brain,a):
    hasWhat = a.relation[4:]
    verb = get_tense(a, "has", a.l, brain)
    # Convert any underscores to spaces.
    hasWhat = hasWhat.replace("_"," ")
    if vals_are_string_things(a.r):
        if hasWhat=="property":
            toReturn = list_concepts_naturally(brain,a.l)+" "+get_tense(a, "is", a.l, brain)+" "+ list_words_naturally(a.r)
            toReturn = add_locations(brain, a, toReturn)
        else:
            if is_plural(a.r,brain):
                hasWhat = en.noun.plural(hasWhat)
            toReturn = list_concepts_naturally(brain,a.l) + " "+verb+" the " + hasWhat + " " + list_words_naturally(a.r)
    elif get_type(a.r)=="hash_array":
        newRights = []
        if hasWhat=="goal":
            for newRight in a.r:
                newRight["tense"]="future"
                newRights.append(newRight)
        else:
            newRights = a.r
        newRights = list_clauses_naturally(brain, newRights)
        toReturn = list_concepts_naturally(brain,a.l) + " "+verb+" the " + hasWhat + " that " + newRights
    else:
        toReturn = list_concepts_naturally(brain,a.l) + " "+verb+" the " + hasWhat + " " + str(a.r)
    toReturn = add_end_marks(a, toReturn)
    return toReturn

def translate_has_assertion(brain,a):
    verb = get_tense(a, "has", a.l, brain)
    toReturn = list_concepts_naturally(brain,a.l)+" "+verb+" "

    # Assume one number in num_r for now.
    if hasattr(a,"num_r"):
        if isinstance(a.num_r[0],int):
            number = en.number.spoken(a.num_r[0])
        else: # includes if isinstance(a.num_r[0],basestring)
            number = str(a.num_r[0])
        toReturn += number + " "
        newRights = a.r[:]
        if a.num_r[0]==1:
            # Make newRights elements singular.
            for i,nr in enumerate(newRights):
                newRights[i] = en.noun.singular(nr)
        else:
            # Make newRights elements plural.
            for i,nr in enumerate(newRights):
                newRights[i] = en.noun.plural(nr)
        toReturn += list_words_naturally(newRights)
    else:
        toReturn += list_concepts_naturally(brain,a.r)
    toReturn = add_end_marks(a, toReturn)
    return toReturn

def translate_implies_assertion(brain,a):
    imply = get_tense(a, "imply", ["singular"], brain)
    newLefts = list_clauses_naturally(brain, a.l)
    newRights = list_clauses_naturally(brain, a.r)

    return "the fact that " + newLefts + " " + imply + " that " + newRights + "."

def translate_cause_assertion(brain,a):
    newLefts = list_clauses_naturally(brain, a.l)
    newRights = []
    for newRight in a.r:
        newRight["tense"] = "future"
        newRights.append(newRight)
    newRights = list_clauses_naturally(brain, newRights)

    if hasattr(a,"prefix"):
        if "might" in a.prefix:
            return "if " + newLefts + ", it's possible that " + newRights + "."
        else:
            return "because " + newLefts + ", " + newRights + "."
    return "because " + newLefts + ", " + newRights + "."

def translate_pf_assertion(brain,a):
    newLefts = list_clauses_naturally(brain, a.l)
    newRights = list_clauses_naturally(brain, a.r)
    return "'" + newLefts + "' is a precondition for '" + newRights + "'."

''' Miscellaneous helper functions. '''
# Add terminal punctuation to the string.
def add_end_marks(a, toReturn):
    if hasattr(a,"grammatical_mood"):
        if a.grammatical_mood=="interrogative":
            toReturn += "?"
        else:
            toReturn += "."
    else:
        toReturn += "."
    return toReturn

# Helper function that adds location_x attributes.
def add_locations(brain, a, toReturn):
    xs = get_location_xs(a)
    if xs:
        for i,x in enumerate(xs):
            if not x.endswith("_owner") and not x.endswith("_property"):
                locs = getattr(a,"location_"+x)[:]
                toReturn += " " + x + " " + list_concepts_naturally(brain,locs)
                if i<len(xs)-1:
                    toReturn += " and"
    return toReturn

# Helper function that deals with condition_x attributes.
def add_conditions(brain,a):
    toReturn = ""
    xs = get_condition_xs(a)
    ys = get_timespan_xs(a)
    if xs:
        for x in xs:
            subAs = getattr(a,"condition_"+x)[:]
            newSubAs = []
            for sa in subAs:
                sa["grammatical_mood"] = "indicative"
                newSubAs.append(sa)
            realizedSubA = list_clauses_naturally(brain, newSubAs)
            if realizedSubA != "":
                toReturn += " " + x + " " + realizedSubA
    if ys:
        for y in ys:
            subA = getattr(a,"timespan_"+y)[:]
            realizedSubA = list_words_naturally(subA)
            if realizedSubA != "":
                toReturn += " " + y + " " + str(realizedSubA)
    return toReturn

# Determines the tense of a verb based on the context.
# Note: negate only works for: be, can, do, will, must, have, may, need, dare, ought.
def get_tense(a, verb, subjArr, brain):
    newVerb = verb
    tense="present"
    negate_flag = False
    if hasattr(a,"prefix"):
        if "not" in a.prefix:
            negate_flag = True
    if hasattr(a,"tense"):
        tense = a.tense
    person_num=3
    if is_plural(subjArr, brain) or (hasattr(a,"grammatical_mood") and a.grammatical_mood=="imperative"):
        person_num=2
    elif "I" in subjArr:
        person_num=1
    if tense=="present":
        newVerb = en.verb.present(verb,person=person_num,negate=negate_flag)
        if newVerb=='':
            newVerb = en.verb.present("do",person=person_num,negate=negate_flag) + " " + en.verb.infinitive(verb)
    elif tense=="past":
        newVerb = en.verb.past(verb,person=person_num,negate=negate_flag)
        if newVerb=='':
            newVerb = en.verb.past("do",person=person_num,negate=negate_flag) + " " + en.verb.infinitive(verb)
    elif tense=="present participle":
        if negate_flag:
            newVerb = "not " + en.verb.present_participle(verb)
        else:
            newVerb = en.verb.present_participle(verb)
    elif tense=="past participle":
        if negate_flag:
            newVerb = "not " + en.verb.past_participle(verb)
        else:
            newVerb = en.verb.past_participle(verb)
    elif tense=="future":
        if negate_flag:
            newVerb = "will not " + en.verb.infinitive(verb)
        else:
            newVerb = "will " + en.verb.infinitive(verb)
    return newVerb

# Returns the type of a value from the name/value pair.
# A value can be a Boolean, a number, a string literal, another assertion (hash), or an array containing either Boolean, number, string, or hash elements.
# In this simple realizer, we assume an array contains all elements of the same type.
# We also assume (for now) that we are only dealing with simple arrays of strings, bools, numbers, or hashes.
def get_type(val):
    try:
        if val==[]:
            return "empty_array"
        if isStringArray(val):
            return "string_array"
        elif isBoolArray(val):
            return "bool_array"
        elif isNumArray(val):
            return "num_array"
        elif isDictArray(val):
            return "hash_array"
        else:
            return None
    except:
        return None

# Returns true if all elements of the input array are strings.
def isStringArray(arr):
    return isTypeArray(arr, basestring)

# Returns true if all elements of the input array are dictionaries.
def isDictArray(arr):
    return isTypeArray(arr, dict)

# Returns true if all elements of the input array are numbers.
def isNumArray(arr):
    return isTypeArray(arr, numbers.Number)

# Returns true if all elements of the input array are numbers.
def isBoolArray(arr):
    return isTypeArray(arr, bool)

# Returns true if all elements of the input array are of the input type.
def isTypeArray(arr,type):
    for i in range(0,len(arr)):
        if not isinstance(arr[i],type):
            return False
    return True

# Takes in an array, and determines if this array is plural or singular.
# The array is plural if it has more than one element and/or one of its elements
# is a plural concept.
# Examples:
#  - ["friend","enemy"] is plural   (returns True)
#  - ["friends"] is plural          (returns True)
#  - ["friend"] is singular         (returns False)
def is_plural(arr, brain):
    uncountable = get_uncountables()
    return len(arr) > 1 or len(brain.get_indivs([arr[0]])) > 1 or (en.noun.plural(en.noun.singular(arr[0]))==arr[0] and arr[0] not in uncountable)

# Lists a list of words directly into a natural format.
# Examples:
#  - ["one"] => "one"
#  - ["one","two"] => "one and two"
#  - ["one","two","three"] => "one, two, and three"
def list_words_naturally(arr):
    finalString = ""
    if arr:
        for i in range(0, len(arr)):
            concept=arr[i]
            if (i<len(arr)-2):
                finalString += concept + ", "
            elif (i==len(arr)-2):
                if (len(arr)==2):
                    finalString+= concept + " and "
                else:
                    finalString += concept + ", and "
            else:
                finalString += concept
    return finalString

# Similar to list_words_naturally, except accounts for how to deal with abstract
# concepts.
# Examples:
#  - ["Ariel","prince"] => "Ariel and Eric"  (if prince has_name Eric)
#  - ["Ariel","sky"] => "Ariel and the sky"
def list_concepts_naturally(brain,arr):
    finalString=""
    for i in range(0, len(arr)):
        concept = str(arr[i])
        # Remove keyword specifiers, if any.
        concept = concept.lstrip("$(").rstrip(")")

        # Refer to arr[i] by actual name.
        name = brain.get_assertions_with({"l":[concept],"relation":"has_name"})
        if name:
            if isinstance(name[0]["r"],basestring):
                concept = name[0]["r"].title()
            else:
                concept = name[0]["r"][0].title()
        else:
            # TODO: Retrieve the article for concept ("the", "a", "an", or "").
            # article = get_article_for(concept, brain)
            # Due to the number of rules about article omission, we're going to use "the" for now as a simple solution.
            article = "the"
            if article!="":
                article = article + " "
            # Remove possessiveness if necessary for parsing.
            main_concept = concept
            if concept.endswith("'s"):
                main_concept=concept[:-2]
            main_concept = main_concept.rstrip("?:!.,;'")
            # Determine if we should use an article, either definite or indefinite.
            if main_concept != "his":
                if en.is_noun(en.noun.singular(main_concept)):
                    concept = article + concept

                else: # e.g. gingerbread house >> a gingerbread house
                    words = main_concept.split(" ")
                    allNouns = True
                    for w in words:
                        if not en.is_noun(en.noun.singular(w)):
                            allNouns = False
                    if allNouns:
                        concept = article + concept
        if (i<len(arr)-2):
            finalString += concept + ", "
        elif (i==len(arr)-2):
            if len(arr)==2:
                finalString+= concept + " and "
            else:
                finalString += concept + ", and "
        else:
            finalString += concept
    return finalString

# Uses list_words_naturally to connect assertion clauses.
# Example:
# [
    # {"l":["milk"], "relation":"has_property","r":["blue"]},
    # {"l":["sand"], "relation":"has_property","r":["coarse","irritating"]}
# ]
# =>
# The milk is blue and the sand is coarse and irritating
def list_clauses_naturally(brain, arr):
    newArr = []
    for e in arr:
        newArr.append(realize_brain_assertion(brain, Assertion.Assertion(e), True))
    return list_words_naturally(newArr)

# Determine if the potential article is definite or indefinite.
# Note: this function is currently not being used due to the number of complex
# rules for article omission.
# Use a definite article if an assertion in the brain exists where:
#  - left-hand ("l") value contains concept
#  - relation is is_a, type_of, or instance_of
def get_article_for(concept, brain):
    declaration = brain.get_assertions_with({"l":[concept],"relation":"is_a"}) + brain.get_assertions_with({"l":[concept],"relation":"instance_of"})
    if declaration: # definite article
        return "the"
    else: # indefinite article
        uncountable = get_uncountables()
        if en.noun.plural(en.noun.singular(concept))==concept or concept in uncountable:
            return ""
        else:
            return en.noun.article(concept).split(" ")[0]

# Changes an adjective to its adverb form.
def adjective_to_adverb(word):
    if word=="good":
        return "well"
    elif word=="fast" or word=="hard":
        return word
    elif word[-2:]=="hy":
        return word + "ly"
    elif word[-2:]=="ly":
        return word
    elif word[-1:]=="y":
        return word[0:-1] + "ily"
    elif word[-2:]=="le":
        return word[0:-1] + "y"
    elif word[-2:]=="ic":
        return word + "ally"
    else:
        return word + "ly"
