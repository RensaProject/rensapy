'''
This file defines the Entity and Actor classes.
'''

import sys
import os

from Brain import *
from GuessGender import *
import random

class Entity(object):
    def __init__(self, attributes):
        self.keyword = attributes['keyword']
        self.type = attributes['type']

class Actor(Entity):
    def __init__(self, attributes):
        self.name = attributes['name'] if "name" in attributes else get_random_name()
        if "keyword" in attributes:
            Entity.__init__(self, {"keyword":attributes['keyword'],"type":"actor"})
        else:
            Entity.__init__(self, {"keyword":self.name,"type":"actor"})

        self.brain = attributes['brain'] if "brain" in attributes else Brain()

        if "gender" in attributes:
            self.gender = attributes['gender']
        else:
            if self.name:
                self.gender = guess_gender(self.name)
        self.set_references()

    def set_name(self,name):
        self.name = name

    def believes(self,assertions):
        flag = True
        for a in assertions:
            if isinstance(a,dict):
                if not self.brain.has_assertion(a):
                    flag = False
            elif isinstance(a,basestring):
                words = a.split(" ")
                if words and len(words)==3:
                    left, relation, right = words[0], words[1], words[2]
                    if not self.brain.get_assertions_with({"l":[left],"relation":relation,"r":[right]}):
                        flag = False
        return flag

    def persuade(self,other,assertions):
        if assertions:
            if isinstance(assertions[0],dict):
                other.brain.add_assertions(assertions)
            elif isinstance(assertions[0],basestring):
                for a in assertions:
                    words = a.split(" ")
                    if words and len(words)==3:
                        left, relation, right = words[0], words[1], words[2]
                        other.brain.add_assertion({"l":[left],"relation":relation,"r":[right]})
            else:
                print "Warning: persuade() assertion(s) are neither string nor dict."

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)

    def intersect(self,other):
        return self.brain.intersect(other.brain)

    def set_references(self):
          refs = self.get_references()
          self.personal_pronoun = refs[0]
          self.object_pronoun = refs[1]
          self.possessive_adj = refs[2]
          self.possessive_pronoun = refs[3]

    def get_references(self):
      return get_references(self.gender)

def get_actors_from_brain(brain):
    people = []
    # for i in range(0,len(brain.assertions)):
    for i in brain.assertions.keys():
        # If the relation is instance_of, and if r contains "actor",
        if brain.assertions[i].relation=="instance_of" and "actor" in brain.assertions[i].r:
            # For every element in l,
            for j in range(0,len(brain.assertions[i].l)):
                e = brain.assertions[i].l[j]
                # Find all individuals for e
                indivs = brain.get_indivs([e])
                # If e is a group,
                if len(indivs) > 1:
                    # For each individual in the group,
                    for k in range(0, len(indivs)):
                        # Make a person given the keyword indivs[k]
                        p = make_person(brain, indivs[k])

                        # Add person to the array of people.
                        if p not in people:
                            people.append(p)
                # Otherwise, e is an individual.
                else:
                    # Make a person given the keyword e.
                    p = make_person(brain, e)
                    # Add the person to the array of people.
                    if p not in people:
                        people.append(p)
    return people

# Makes a single person given a brain and a keyword.
def make_person(brain,e):
    # Find the name of the Actor, if any.
    # (Assume only one name per person.)
    actorName = e
    name = brain.get_assertions_with({"l":[e],"relation":"has_name"})
    if name:
        if isinstance(name[0]["r"],basestring):
            actorName = name[0]["r"].title()
        else:
            actorName = name[0]["r"][0].title()

    # Find the gender of the person, if any.
       # (Assume only one gender per person.)
    gender = "unknown"
    genders = brain.get_assertions_with({"l":[e],"relation":"has_gender"})

    if genders:
        if isinstance(genders[0]["r"],basestring):
            gender = genders[0]["r"].title()
        else:
            gender = genders[0]["r"][0].title()

    # Find the brain of the person, if any.
      # (Assume only one brain assertion per person.)
    # (However, someone may have more than one brain.)
    brains = brain.get_assertions_with({"l":[e],"relation":"has_brain"})
    if brains:
        brainNames = brains[0].r
        brain = loadBrains(brainNames)

    # Find all assertions related to the person.
    assertions = []
    relatedAsserts = brain.get_assertions_related_to(e)
    for ra in relatedAsserts:
        assertions.append(ra[0])

    # Make a new Actor.
    p = Actor ({"keyword":e, "type":"actor", "name":actorName, "gender": gender, "brain":brain})

    # Set related assertions.
    p.assertions = assertions

    # Set references (like personal pronouns)
    p.set_references()

    return p
