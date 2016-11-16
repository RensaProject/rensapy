'''
This example demonstrates how to load, modify, search, print, and save a Rensa brain.
'''

print "Importing libraries..."
import sys
import os
memory_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'src'))
sys.path.insert(0, memory_path)
from Brain import *

def main():
    ''' Load a brain from JSON. '''
    Rensa = load_brain(['assertions/brain_demo/demo.json'])

    ''' Add a new assertion. '''
    # Add a new assertion to the brain.
    Rensa.add_assertion({
        "l":  ["Alaea salt"],
        "relation":  "type_of",
        "r":  ["salt"]
    })

    ''' Remove an assertion. '''
    # To remove an assertion by id, use remove_assertion_with_id().
    # To remove ALL assertions, use Rensa.clear_assertions().
    Rensa.remove_assertion({
        "l":  ["my favorite pie"],
        "relation":  "is_a",
        "r":  ["pumpkin pie"]
    })

    ''' Edit an assertion. '''
    # Refer to the assertion by its ID, which you can retrieve
    # with Rensa.get_assertion_ID(your_assertion).
    # When editing, you may change any attribute of the assertion.
    Rensa.edit_assertion(5,"r",["pie","cake"])

    ''' Find a group of assertions. '''
    # Find assertions with a certain tag.
    # This will return any assertions that contain any (but not necessarily all) of the tags within an input list.
    appleAsserts = Rensa.get_assertions_with_tag(["apple"])
    print "\nThe following assertions are tagged with 'apple':"
    for a in appleAsserts:

        print " > " + str(a) + "\n"

    # Find assertions with certain (exact) attribute values.
    minceAsserts = Rensa.get_assertions_with({"relation":"used_for","r":["mince"]})
    print "The following tools are used for mincing:"
    for r in minceAsserts:
        for l in r["l"]:
            print " > " + str(l) + "\n"

    ''' Print or realize an assertion. '''
    # Pretty print an assertion (JSON format).
    print "Let's prettyprint an assertion: "
    a = Rensa.get_assertions()[0]
    a.prettyprint()

    # Realize an assertion given a brain.
    # Here, the Boolean flag indicates whether the statement should be realized
    # as a fragment (True) or a full sentence (False).
    print "Let's realize all the assertions we know:"
    for a in Rensa.get_assertions():
        print " > " + a.realize(Rensa,False)

    ''' Save new knowledge to file. '''
    Rensa.save_brain("assertions/brain_demo/")

    ''' Remove old assertion files. '''
    delete_old_assertions("assertions/brain_demo/")

    print "Process completed."

if __name__ == '__main__':
    main()
