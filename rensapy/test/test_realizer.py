'''
This file tests the SimpleRealizer.
'''

print "Importing libraries..."
import unittest
import sys
import os
memory_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'src'))
sys.path.insert(0, memory_path)
from Brain import *

# Initialize an empty brain to use for testing.
emptyBrain = Brain()

class TestUM(unittest.TestCase):
    def setUp(self):
        pass

    def test_is_a(self):
        tests = {
            "The bird is an animal.":Assertion({"l":["bird"],"relation":"is_a","r":["animal"]}),

            "The bird will be an animal.":Assertion({"l":["bird"],"relation":"is_a","r":["animal"],"tense":"future"}),

            "The dinosaur was an animal.":Assertion({"l":["dinosaur"],"relation":"is_a","r":["animal"],"tense":"past"}),

            "The dinosaurs were animals.":Assertion({"l":["dinosaurs"],"relation":"is_a","r":["animal"],"tense":"past"}),

            "Calvin and Hobbes are philosophers.":Assertion({"l":["Calvin","Hobbes"],"relation":"is_a","r":["philosopher"]}),

            "Eric, Grimsby, and the sailors are actors and fictional characters.":Assertion({"l":["Eric","Grimsby","sailors"],"relation":"is_a","r":["actor","fictional character"]}),

            "Cimorene is an actor, hero, and princess.":Assertion({"l":["Cimorene"],"relation":"is_a","r":["actor","hero","princess"]}),

            "I am a scientist.":Assertion({"l":["I"],"relation":"is_a","r":["scientist"]}),
        }
        for k,v in tests.iteritems():
            self.assertItemsEqual(k, v.realize(emptyBrain,False))

    def test_location(self):
        tests = {
            "Eric, Grimsby, and the sailors were on the ship.":Assertion({"l":["Eric","Grimsby","sailors"],"relation":"location_on","r":["ship"],"tense":"past"}),
            "The cookie jar was on top of the refrigerator.":Assertion({"l":["cookie jar"],"relation":"location_on_top_of","r":["refrigerator"],"tense":"past"}),
        }
        for k,v in tests.iteritems():
            self.assertItemsEqual(k, v.realize(emptyBrain,False))

    def test_x_of(self):
        tests = {
            "The acorn is a symbol of strength.":Assertion({"l":["acorn"],"relation":"symbol_of","r":["strength"]}),
            "The acorn reminds everyone of the tree.":Assertion({"l":["acorn"],"relation":"reminds_of","r":["tree"]}),
            "Link knows that the acorn reminds Link of the tree.":Assertion({"owner":["Link"], "l":["acorn"],"relation":"reminds_of","r":["tree"]}),
        }
        for k,v in tests.iteritems():
            self.assertItemsEqual(k, v.realize(emptyBrain,False))

    def test_has_x(self):
        tests = {
            "I have two pennies.":Assertion({"l":["I"],"relation":"has","r":["penny"],"num_r":["two"]}),

            "Matilda has the book.":Assertion({"l":["Matilda"],"relation":"has","r":["book"]}),

            "Matilda will have the book.":Assertion({"l":["Matilda"],"relation":"has","r":["book"],"tense":"future"}),

            "Matilda had the book and the pencil.":Assertion({"l":["Matilda"],"relation":"has","r":["book","pencil"],"tense":"past"}),

            "Matilda had three books and pencils.":Assertion({"l":["Matilda"],"relation":"has","r":["book","pencil"],"tense":"past","num_r":[3]}),

            "Alberta was cool and collected.":Assertion({"l":["Alberta"],"relation":"has_property","r":["cool","collected"],"tense":"past"}),

            "The moon was high in the sky.":Assertion({
                "l":["moon"],"relation":"has_property","r":["high"],"location_in":["sky"],"tense":"past"
            }),
        }
        for k,v in tests.iteritems():
            self.assertItemsEqual(k, v.realize(emptyBrain,False))

    def test_precondition_for(self):
        tests = {
            "'Ariel is a human' is a precondition for 'Ariel explores the land'.":Assertion({
              "l":  [{"l":["Ariel"], "relation":"is_a", "r":["human"]}],
              "relation":  "precondition_for",
              "r":  [{"l":["Ariel"], "relation":"action", "r":["explore"],"action_object":["land"]}]
            }),
        }
        for k,v in tests.iteritems():
            self.assertItemsEqual(k, v.realize(emptyBrain,False))

    def test_implies(self):
        tests = {
            "The fact that the acorn is tough implied that the acorn was a symbol of strength.":Assertion({
            "l":[{"l":["acorn"], "relation":"has_property","r":["tough"]}],
            "relation":"implies",
            "r":[{"l":["acorn"], "relation":"symbol_of","r":["strength"],"tense":"past"}],
            "tense":"past"
          }),
        }
        for k,v in tests.iteritems():
            self.assertItemsEqual(k, v.realize(emptyBrain,False))

    def test_causes(self):
        myBrain = Brain()
        myBrain.add_assertion({"l":["Ariel"],"relation":"has_gender","r":["female"]})
        tests = {
            "If Ariel gives her voice to Ursula, it's possible that Ariel will be a human.":Assertion({
              "l":  [{"l":["Ariel"], "relation":"action", "r":["give"],"action_object":["voice"],"action_object_owner":["Ariel"], "action_recipient":["Ursula"]}],
              "relation":  "causes",
              "r":  [{"l":["Ariel"], "relation":"is_a", "r":["human"]}],
              "prefix":["might"]
          }),
          "Because the acorn is tough, everyone will have the belief that the acorn is a symbol of strength.":Assertion({
            "l":  [{"l":["acorn"], "relation":"has_property", "r":["tough"]}],
            "relation":  "causes",
            "r":  [{"l":["$(everyone)"], "relation":"has_belief", "r":[{"l":["acorn"],"relation":"symbol_of","r":["strength"]}]}]
        }),

        }
        for k,v in tests.iteritems():
            self.assertItemsEqual(k, v.realize(myBrain,False))

    def test_x_for(self):
        tests = {
            "The knife is used for mincing, chopping, dicing, and slicing.":Assertion({
                "l":  ["knife"],
                "relation":  "used_for",
                "r":  ["mince","chop","dice","slice"]
            }),
            "Use the knife for mincing, chopping, dicing, and slicing.":Assertion({
                "l":  ["knife"],
                "relation":  "used_for",
                "r":  ["mince","chop","dice","slice"],
                "grammatical_mood":"imperative"
            }),
            "The spoon is used for scooping the ice cream.":Assertion({
                "l":["spoon"],
                "relation":"used_for",
                "r":[{"l":["spoon"], "relation":"action","r":["scoop"],"action_object":["ice cream"]}]
            }),
            "Use the spoon for scooping the ice cream.":Assertion({
                "l":["spoon"],
                "relation":"used_for",
                "r":[{"l":["spoon"], "relation":"action","r":["scoop"],"action_object":["ice cream"]}],
                "grammatical_mood":"imperative"
            })

        }
        for k,v in tests.iteritems():
            self.assertItemsEqual(k, v.realize(emptyBrain,False))

    def test_set_x(self):
        tests = {
            "The value of the enemy's and the player's health is set to [100].":Assertion({
            "l":["health"],"relation":"set_value","r":[100],"l_owner":["enemy","player"]
            }),
            "Set the oven to 350 degrees F.":Assertion({
            "l":["oven"],
            "relation":"set_value",
            "r":[350],
            "r_unit": "degrees F",
            "grammatical_mood":"imperative"
            }),

        }
        for k,v in tests.iteritems():
            self.assertItemsEqual(k, v.realize(emptyBrain,False))

    def test_action_imperative(self):
        tests = {
            "Mince the onion and the garlic.":Assertion({
              "l":  ["chef"],
              "relation":  "action",
              "r":  ["mince"],
              "action_object":["onion","garlic"],
              "grammatical_mood": "imperative"
          }),

            "Bake the bread until the bread is golden brown.":Assertion({
                "l":["chef"],
                "relation":"action",
                "r":["bake"],
                "action_object":["bread"],
                "condition_until":[{"l":["bread"],"relation":"has_property", "r":["golden brown"]}],
                "grammatical_mood":"imperative"
            }),
            "Boil the egg for three minutes.":Assertion({
                "l":["chef"],
                "relation":"action",
                "r":["boil"],
                "action_object":["egg"],
                "timespan_for":["three minutes"],
                "grammatical_mood":"imperative"
            }),
            "Pour the milk into the bowl if the sugar is in the bowl.":Assertion({
                "l":  ["chef"],
                "relation":  "action",
                "r":  ["pour"],
                "action_object":["milk"],
                "location_into":["bowl"],
                "condition_if":[{"l":["sugar"],"relation":"location_in", "r":["bowl"]}],
                "grammatical_mood": "imperative"
            }),
            "Don't throw the cards on the floor and at the ceiling.":Assertion({
                "l":  ["player"],
                "relation":  "action",
                "r":  ["throw"],
                "action_object":["cards"],
                "location_on":["floor"],
                "location_at":["ceiling"],
                "prefix":["not"],
                "grammatical_mood": "imperative"
            }),
        }
        for k,v in tests.iteritems():
            self.assertItemsEqual(k, v.realize(emptyBrain,False))

    def test_action_indicative(self):
        tests = {
            "The chef minces the onion and the garlic.":Assertion({
              "l":  ["chef"],
              "relation":  "action",
              "r":  ["mince"],
              "action_object":["onion","garlic"]
          }),

            "The chef bakes the bread until the bread is golden brown.":Assertion({
                "l":["chef"],
                "relation":"action",
                "r":["bake"],
                "action_object":["bread"],
                "condition_until":[{"l":["bread"],"relation":"has_property", "r":["golden brown"]}]
            }),
            "The chef boils the egg for three minutes.":Assertion({
                "l":["chef"],
                "relation":"action",
                "r":["boil"],
                "action_object":["egg"],
                "timespan_for":["three minutes"]
            }),
            "The chef pours the milk into the bowl if the sugar is in the bowl.":Assertion({
                "l":  ["chef"],
                "relation":  "action",
                "r":  ["pour"],
                "action_object":["milk"],
                "location_into":["bowl"],
                "condition_if":[{"l":["sugar"],"relation":"location_in", "r":["bowl"]}]
            }),
            "I didn't steal Cindy's four salt shakers.":Assertion({
                "l":["I"],"relation":"action","r":["steal"],"action_object":["salt shaker"], "num_action_object":[4], "action_object_owner":["Cindy"],"prefix":["not"],"tense":"past"
            }),
        }
        for k,v in tests.iteritems():
            self.assertItemsEqual(k, v.realize(emptyBrain,False))

    def test_verb(self):
        tests = {
            "The player consumes the ice cream happily.":Assertion({
                "l":["player"],"relation":"consume","r":["ice cream"],"with_property":["happy"]
            }),
        }
        for k,v in tests.iteritems():
            self.assertItemsEqual(k, v.realize(emptyBrain,False))

    def test_discourse(self):
        tests = {
            "'Isn't this great?  The salty sea air, the wind blowing in your face...a perfect day to be at sea!' Eric said.":Assertion({
                "l": ["Eric"],
                "relation": "action",
                "r": ["say"],
                "tense":"past",
                "discourse": "Isn't this great?  The salty sea air, the wind blowing in your face...a perfect day to be at sea!"
          }),
        }
        for k,v in tests.iteritems():
            self.assertItemsEqual(k, v.realize(emptyBrain,False))

        self.assertItemsEqual("Grimsby said, 'Oh yes...delightful...'", Assertion({
            "l":["Grimsby"],
            "relation": "action",
            "r": ["say"],
            "tense":"past",
            "discourse": "Oh yes...delightful..."
        }).realize(emptyBrain,True))

if __name__ == '__main__':
    # Run all tests.
    unittest.main()
