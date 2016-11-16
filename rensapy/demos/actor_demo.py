'''
This is a demonstration of Rensa actors.
'''

print "Importing libraries..."
import os
import sys
memory_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'src'))
sys.path.insert(0, memory_path)
from Entity import *

def main():
	''' Initializing actors. '''
	print "* * *"
	# An "actor" is an agent that has intentions and can perform actions.
	# In Rensa, actors have brains (sets of assertions) which let them reason about the world they know, as well as their intentions and actions.

	# Initialize an actor like so:
	maria =  Actor({
		"name":"Maria",
		"brain":load_brain([ 'assertions/actor_demo/maria_brain.json']),
		"gender":"female"
	})

	# If we initialize another actor, we can have the two interact.
	#  - Because we don't specify a brain, Rensa will initialize an empty one.
	#  - Because we don't specify a gender, Rensa will guess one.
	abe =  Actor({"name":"Abe"})

	#  - If we don't specify a name, the system will choose one that it knows at random.
	wildcard = Actor({})
	print "The wildcard's name is " + wildcard.name + "."
	print "The wildcard's gender is " + wildcard.gender + "."

	''' Checking an actor's beliefs. '''
	print "* * *"
	# Use actor.believes(assertions) to determine whether an actor has an exact set of assertions inside their brain.
	#  - Same as: maria.brain.has_assertion().
	if (maria.believes([
		{"l":["pie"],"relation":"has_property","r":["tasty"]}
	])):
		print "Maria thinks pie is tasty."
	else:
		print "Maria doesn't think pie is tasty."

	# You can also write each assertion in the list as a string of three words, where each word is the value for (1) "l" (left), (2) relation, and (3) "r" (right).
	if (abe.believes(["pie has_property tasty"])):
		print "Abe thinks pie is tasty."
	else:
		print "Abe doesn't think pie is tasty."

	''' Interaction between actors. '''
	# Use actor.persuade(other, assertions) to have one actor copy a set of assertions into another actor's brain.
	if (not abe.believes(["maria instance_of liar"])):
		maria.persuade(abe, ["pie has_property tasty"])
		# maria.persuade(abe, [{"l":["pie"],"relation":"has_property","r":["tasty"]}]) is also valid, if you wish to persuade someone of a more complex assertion.

	# Now Abe also believes cake is tasty.
	if (abe.believes(["pie has_property tasty"])):
		print "Maria persuaded Abe that pie is tasty."
	else:
		print "Abe doesn't think pie is tasty."

	# Check what two people agree on.
	print "Here's what Maria and Abe agree on:"
	agreed = abe.intersect(maria)
	for e in agreed:
		print " > " + e.realize(abe.brain,False)

	''' Retrieving words associated with an actor's gender. '''
	print "* * *"
	# You can retrieve gender references for an actor.
	# - Actors of unknown gender use singular they.
	# - If you wish to further personalize gendered references, edit get_references() in Entity.py.

	print "Maria's personal pronoun is: " + maria.personal_pronoun
	print "Abe's object pronoun is: " + abe.object_pronoun
	print "Abe's possessive adjective is: " + abe.possessive_adj
	print "Maria's possessive pronoun is: " + maria.possessive_pronoun

	print "* * *"
	print "Process completed."

if __name__ == '__main__':
	main()
