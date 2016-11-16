Rensa is a framework for storing and modifying facts, and realizing facts into natural text.

.. image:: http://neurogirl.com/rensa/rensa-demo.gif
  :align: center
  :target: https://github.com/RensaProject/rensa-py

Features
================
- **Concept extraction.** Rensa can help you automatically glean some simple facts from natural text.
- **Data access and control.** You can add, remove, edit, or search for Rensa facts programmatically.
- **Realization.** Facts can be realized from their data structure format into natural language.
- **Actor support.** You can define actors (people) associated with a set of facts (their "brains").  Actors can persuade others to change their beliefs.
- **Story encoding.** You can build Story objects from a set of Rensa facts.  Just like brains, stories can be edited and realized into natural text.

You can encode most valid JSON name-value pairs with Rensa, but there is a recommended specification to follow.  Check out the `wiki
<https://github.com/RensaProject/rensapy/wiki>`_ for more.

Getting Started
================
Install Python 2.7
--------------------
At the moment, you will need Python 2.7 to run rensapy.  You can check what version of Python you have by running:

::

    python --version

If you do not have Python 2.7 installed, you can install it from the
`Python website <https://www.python.org/downloads/>`__.

Or, if you use Homebrew:

::

    brew install python

If you're worried about multiple Python versions existing in harmony, you can use `virtualenv
<http://docs.python-guide.org/en/latest/dev/virtualenvs/>`_.


Try the Demos
--------------------
Once you have Python 2.7 installed, clone or download the repository.  Next, take a look inside the demos folder.  The brain_demo.py file is a good place to start.  To run it, cd into the demos/ directory and type *python brain_demo.py*.

This file shows you how to load facts (*assertions*) from a JSON file into a Rensa brain.  It also steps through how to change and search through a brain, as well as how to realize its contents.

Making a brain is this easy::

    from Brain import *
    myBrain = Brain()

If you'd rather load Rensa assertions from JSON, use::

    myBrain = load_brain(['path/to/your_file.json'])

Now we can add a fact to our brain::

    myBrain.add_assertion(
      {
        "l":["you"],
        "relation":"has_property",
        "r":["awesome"]
      }
    )

Made a mistake?  You can find and edit the contents of any brain.  Let's change the tense of our first assertion::

    myBrain.edit_assertion(1,"tense","future")

We can realize all the assertions in a brain like this::

    for a in myBrain.get_assertions():
      print a.realize(myBrain,False)

Once we're done changing the brain, we can save it as a JSON file::

    myBrain.save_brain('your/save/path/')

The remaining three demos demonstrate the basics of extracting simple assertions, making actors with brains, and building stories.

Applications
================
Rensa is not meant to be able to represent all forms of meaning, but it can encode enough to be useful for a wide range of applications.  For example, it has been used to adapt `stories
<http://link.springer.com/chapter/10.1007/978-3-319-48279-8_16>`_, `games
<http://www.aaai.org/ocs/index.php/AIIDE/AIIDE16/paper/view/14061>`_, and legal forms.

License
================
Copyright (c) Sarah Harmon: this source code is free to use under the MIT License with author attribution.  Refer to LICENSE.txt for details.

If you use this repository, please cite:

- Harmon, SM.  *Narrative Adaptation* (Doctoral dissertation). University of Santa Cruz, 2017.
