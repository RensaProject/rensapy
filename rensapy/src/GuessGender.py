'''
Super lightweight file that references a dataset of baby names used in the
United States (1880-2008).  Provides functions for guessing the gender of a
name and obtaining a random name of a certain gender.
'''

import random
import sys
import os

memory_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'src'))
sys.path.insert(0, memory_path)

baby_names = {}
female_names = []
male_names = []

ins = open( memory_path + "/data/names.csv", "r" )
for i, line in list(enumerate(ins)):
  if i==0:
    continue
  else:
    row = line.split(",")
    name = str(row[0])
    numFemale = int(row[1])
    numMale = int(row[2])
    baby_names[name] = [numFemale, numMale]
    if numFemale > 0:
        female_names.append(name)
    if numMale > 0:
        male_names.append(name)
ins.close()

# Given a name, search list of baby names for matching gender.
# If there are more instances of females being given the name,
# guess female.  If there are more instances of males, guess male.
# Otherwise, assume unisex / unknown.
def guess_gender(name):
    return guess_gender_with_threshold(name,0)

# Same as guess_gender, except allow user to specify how
# many instances of one gender over the other need to have
# been observed.
def guess_gender_with_threshold(name,thresh):
    if baby_names.__contains__(name):
        if baby_names[name][0] > baby_names[name][1]+thresh:
            return "female"
        elif baby_names[name][1] > baby_names[name][0]+thresh:
            return "male"
        else:
            return "unisex"
    return "unknown"

# Same as guess_gender_with_threshold, except consider the
# threshold to be a percentage instead of a count.
def guess_gender_with_percent(name,perc):
    if baby_names.__contains__(name):
        percFemale = get_perc_female(name)
        percMale = get_perc_male(name)
        if percFemale > percMale+perc:
            return "female"
        elif percMale > percFemale+perc:
            return "male"
        else:
            return "unisex"
    return "unknown"

# Returns how often over the span of 1880-2008
# that that this name was considered female in the US.
def get_perc_female(name):
    if baby_names.__contains__(name):
        return (baby_names[name][0] * 100.0) / (baby_names[name][0] + baby_names[name][1])
    return 0

# Returns how often over the span of 1880-2008
# that that this name was considered male in the US.
def get_perc_male(name):
    if baby_names.__contains__(name):
        return (baby_names[name][1] * 100.0 / total) / (baby_names[name][0] + baby_names[name][1])
    return 0

# Returns true if the name has been used for a female.
def is_female_name(name):
    return name in female_names

# Returns true if the name has been used for a male.
def is_male_name(name):
    return name in male_names

# Returns true if the name has been used for both genders.
def is_unisex_name(name):
    return name in female_names and name in male_names

# Given a reference, determine the gender (or point of view if self).
def gender_from_reference(ref):
    if ref in ["I","me","my","mine"]:
        return "self"
    elif ref in ["she","her","her","hers"]:
        return "female"
    elif ref in ["he","him","his","his"]:
        return "male"
    else:
        return "unknown"

# Given a gender, determine the references for a person of that gender.
def get_references(gender):
    if gender=="self":
        return ["I","me","my","mine"]
    elif gender=="female":
        return ["she","her","her","hers"]
    elif gender=="male":
        return ["he","him","his","his"]
    else:
        return ["they","them","their","theirs"]

# Return a random name of any gender.
def get_random_name():
    return random.choice(baby_names.keys())

# Return a random female name.
def get_random_female():
    return random.choice(female_names)

# Return a random male name.
def get_random_male():
    return random.choice(male_names)

# Return a random unisex name.
def get_random_unisex():
    return random.choice(list(set(female_names) & set(male_names)))
