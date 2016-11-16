'''
This example demonstrates how to extract simple Rensa assertions from natural text.
'''

print "Importing libraries..."
import sys
import os
memory_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'src'))
sys.path.insert(0, memory_path)
from Brain import *
from ConceptExtractor import *

def main():
    ''' Extract story assertions. '''
    # Here is an example string.
    string = "Once upon a time, Ariel was a mermaid.  Ariel has the gender female.  Ariel had a shell.  Ariel loved the land. Ariel happily sang a song.  Ariel also loved Eric. So, Ariel gave her voice to Ursula."

    # Extract Rensa assertions with extract_story_concepts().
    print "I'm reading: " + string + "\n* * * "
    learned = extract_story_concepts(string)

    # Store the assertions in a brain.
    Rensa = make_brain(learned)

    # Realize the assertions we learned.
    print "Here's what I learned:"
    for a in Rensa.get_assertions():
        print " > " + a.realize(Rensa,False)

    print "* * *\nProcess completed."

if __name__ == '__main__':
    main()
