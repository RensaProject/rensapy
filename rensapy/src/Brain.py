'''
This file defines the Brain class.
'''

from Assertion import *
import json
import time
import glob
import os
import numbers

'''
Brains store sets of assertions.
'''
class Brain(object):
	def __init__(self, attributes = {}):
		self.assertions = {}

	def __eq__(self, other):
		if type(other) is type(self):
			return len(self.assertions)==len(other.assertions) and len(self.intersect(other))==len(self.assertions)

	# Return a list of assertions that represents an intersection between two
	# brains.
	def intersect(self, other):
		return [v for k,v in self.assertions.iteritems() if other.has_assertion(v)]

	# Check if an assertion is already part of this Brain object's assertions list.
	def has_assertion(self,a):
		if isinstance(a,dict):
			return Assertion(a) in self.assertions.values()
		elif isinstance(a,Assertion):
			return a in self.assertions.values()
		else:
			print "RENSA: Error (has_assertion): " + a + " is not a dictionary or an Assertion."

	# Returns an array containing all assertions.
	def get_assertions(self):
		return list(self.assertions.values())

	# Add a new assertion to the assertions list.
	def add_assertion(self, a):
		# Find highest key value.
		# (May be greater than len(self.assertions)).
		if self.assertions:
			i = max(self.assertions.keys(), key=int)
		else:
			i=0

		if isinstance(a,dict):
			if not self.has_assertion(a):
				self.assertions[i+1] = Assertion(a)
				return True
		elif isinstance(a,Assertion):
			if not self.has_assertion(a):
				self.assertions[i+1] = a
		else:
			print "RENSA: Error (add_assertion): " + a + " is not a dictionary or an Assertion."
		return False

	# Add a group of assertions to the assertions list.
	def add_assertions(self, asserts):
		for a in asserts:
			self.add_assertion(a)

	# Remove an assertion from the assertions list.
	def remove_assertion(self,a):
		remove_keys = []
		for k,v in self.assertions.iteritems():
			if v==Assertion(a):
				remove_keys.append(k)
					# break - assumes duplicates aren't in list
		for r in remove_keys:
			# del self.assertions[r]
			self.assertions.pop(r, None)

	# Remove an assertion by ID.
	def remove_assertion_with_id(self,idn):
		# del self.assertions[idn]
		self.assertions.pop(idn, None)

	# Remove all assertions from the assertions list.
	def clear_assertions(self,a):
		self.assertions.clear()

	# Write all known assertions to file.
	def save_assertions(self,path):
		asserts=[]
		for k,a in self.assertions.iteritems():
			asserts.append(a.to_dict())
		output=open(path+"assertions-"+time.strftime("%Y%m%d-%H%M%S")+".json","w")
		json.dump(asserts,output,indent=2)

	# Write all new knowledge to file.
	def save_brain(self,path):
		self.save_assertions(path)

	# Returns an assertion's ID.
	def get_assertion_ID(self,a):
		for k, v in self.assertions.iteritems():
			if v==Assertion(a):
				return k

	# Return an assertion given an ID.
	def get_assertion_by_ID(self,idn):
		return self.assertions.get(idn)

	# Edit any attribute of an assertion to have a new value.
	def edit_assertion(self,idn,attr,value):
		setattr(self.assertions[idn],attr,value)

	# Returns list of all assertions IDs with the specified values for attributes.
	def get_assertion_ids_with(self,d):
		l = []
		for k,a in self.assertions.iteritems():
			flag = True
			for m,b in d.iteritems():
				for item in b:
					# Check if m is a property of the assertion.
					if hasattr(a,m):
						if item not in getattr(a,m):
							flag = False
					else:
						flag = False
			if flag:
				l.append(k)
		return l

	# Returns list of all assertions with the specified values for attributes.
	def get_assertions_with(self,d):
		asserts = []
		ids = self.get_assertion_ids_with(d)
		for i in ids:
			asserts.append(self.get_assertion_by_ID(i).to_pruned_dict())
		return asserts

	# Returns list of all assertions IDs with the list of attributes.
	def get_assertion_ids_with_attributes(self,properties):
		l = []
		for k,a in self.assertions.iteritems():
			flag = True
			for p in properties:
				if not hasattr(a,p):
					flag = False
			if flag:
				l.append(k)
		return l

	# Returns list of all assertions that have the specified tag.
	def get_assertion_ids_with_tag(self,tags):
		l = []
		for k, v in self.assertions.iteritems():
			if hasattr(v,'tag'):
				for t in tags:
					if t in v.tag:
						l.append(k)
		return l

	# Returns list of all assertions that have the specified tag.
	def get_assertions_with_tag(self,tags):
		l = []
		for k, v in self.assertions.iteritems():
			if hasattr(v,'tag'):
				for t in tags:
					if t in v.tag:
						l.append(v.to_pruned_dict())
		return l

	# Takes in a string concept, and returns a list of all
	# assertions that involve that concept, and how they are related.

	# Example:
	# If concept is "prince" and prince instance_of actor, returns
	# [ [{"l":["prince"], "relation":"instance_of", "r":["actor"]}, "l"] ]
	def get_assertions_related_to(self, concept):
		l = []
		for k,a in self.assertions.iteritems():
			# For each property in the current assertion,
			for prop, value in a.__dict__.iteritems():
				''' Find out if this is worth keeping. '''
				if (concept_in_assertion(k,a,prop,value,concept)):
					l.append([a, prop])
		return l

	# Same as get_assertions_related_to, except returns the ids of the assertions related to the concept.
	def get_assertion_ids_related_to(self, concept):
		l = []
		for k,a in self.assertions.iteritems():
			# For each property in the current assertion,
			for prop, value in a.__dict__.iteritems():
				''' Find out if this is worth keeping. '''
				if (concept_in_assertion(k,a,prop,value,concept)):
					l.append(k)
		return l

	# Find the most specific individuals for a group name.
	def get_indivs(self,group):
		indivs = []
		flag = True
		while (flag):
		  flag = False
		  for g in group:
			ids = self.get_assertions_with({"relation":"type_of","r":g})
			if ids:
			  group = self.get_concept_list(ids,"l")
			  flag = True
			else:
			  indivs.append(g)
		return indivs

'''
Helper for get_assertions_related_to() and get_assertions_related_to().
'''
def concept_in_assertion(k,a,prop,value,concept):
	# If the value of that property is an array with at least one element
	if value and isinstance(value,list):
		# If the value of the current assertion's property contains concept,
		if concept in value:
			# Add this assertion and the property to the list.
			return True
		# For each element in the array,
		for v in value:
			# If the element is a dictionary,
			if isinstance(v,dict):
				# If any of that dictionary's values contain concept,
				for prop2, value2 in v.iteritems():
					if value2 and isinstance(value2,list):
						if concept in value2:
							# Add this assertion and the property to the list.
							return True
					# If the value of that property is a string,
					elif isinstance(value2,basestring):
						# If the value of the current assertion's property is concept,
						if (value2==concept):
							# Add this assertion and the property to the list.
							return True
	# If the value of that property is a string,
	elif isinstance(value,basestring):
		# If the value of the current assertion's property is concept,
		if (value==concept):
			# Add this assertion and the property to the list.
			return True
	else:
		if not isinstance(value,numbers.Number):
			print "Warning: type of " + a[prop] + " is not string, list, or number."
	return False

'''
This function loads all available data into a Brain object,
and returns that object.
'''
def load_brain(assertion_files):
	brain = Brain()
	print "RENSA: Brain initialized."
	for assertions_file in assertion_files:
		with open(assertions_file) as data_file:
			try:
				assertions = json.load(data_file)
			except ValueError as e:
				print('RENSA: Invalid assertions file: %s' % e)
				assertions = None
			if assertions != None:
				print "RENSA: Loading knowledge from " + assertions_file + "..."
				for d in assertions:
					# If we're looking at a scene file, edit all assertions to include a scene specification.
					if "_scene" in assertions_file:
						d["scene"] = assertions_file[assertions_file.index("_scene")+6: assertions_file.index(".json")]
					brain.add_assertion(d)
	return brain

'''
Makes a brain out of a list of assertions.
'''
def make_brain(assertions):
	brain = Brain()
	for a in assertions:
		brain.add_assertion(a)
	return brain

'''
Deletes all assertion files except for the most recent one.
'''
def delete_old_assertions(path):
  userInput = raw_input("\nThis will delete all generated assertion files except for the most recent one.  Do you wish to continue (Y\N)? " + "\n")
  if userInput.lower()=="y":
	dates = []
	for fn in glob.glob(path + "*.json"):
	  if fn.find("assertions-") != -1:
		date = fn[fn.find("assertions-")+11:-5]
		dates.append(date)

	for d in dates:
	  if d != max(dates):
		os.remove(path + "assertions-" + d + ".json")
	print "Old assertion files deleted."
  else:
	print "No assertion files deleted."
  return True
