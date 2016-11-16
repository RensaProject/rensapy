'''
This file defines the Assertion class.  Assertions represent
conceptual knowledge.
'''

from SimpleRealizer import realize_brain_assertion
import json

class Assertion(object):
	def __init__(self, attributes = {}):
		for k, v in attributes.items():
			setattr(self,k,v)

	def __eq__(self, other):
		if type(other) is type(self):
			return self.__dict__ == other.__dict__

	# Returns a dictionary with the attributes of this assertion.
	def to_dict(self):
		d = {}
		for attr, value in self.__dict__.iteritems():
			d[attr] = value
		return d

	# Same as to_dict(), except returns a dict with the non-default values.
	def to_pruned_dict(self):
		d = {}
		for attr, value in self.__dict__.iteritems():
			if value != "":
				d[attr] = value
		return d

	# Same as to_dict(), except with pretty indentation.
	def prettyprint(self):
		print json.dumps(self.to_dict(), indent=2)

	# Realize the assertion given a brain and a Boolean which represents
	# whether the realization is a sentence fragment or not.
	def realize(self, brain, isFragment):
		return realize_brain_assertion(brain,self,isFragment)
