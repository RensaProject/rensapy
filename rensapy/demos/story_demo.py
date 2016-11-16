'''
This example demonstrates how to load, modify, and save a Rensa story.
'''

print "Importing libraries..."
import os
import sys
memory_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'src'))
sys.path.insert(0, memory_path)
from Brain import *
from Story import *

def main():
    ''' Make a new Brain given a list of JSON files.'''
    myBrain = load_brain([
        'assertions/story_demo/littlemermaid_people.json',
        'assertions/story_demo/littlemermaid_scene1.json',
        'assertions/story_demo/littlemermaid_scene2.json'
    ])

    ''' Make a Story from this Brain. '''
    littleMermaid = Story(myBrain)

    ''' Retrieve or remove scenes. '''
    # Retrieve all scenes (as a list of Scene objects) in littleMermaid.
    # print littleMermaid.get_scenes()

    # Retrieve a scene object by its number.
    # Example: retrieve scene 2.
    # print littleMermaid.get_scene(2)

    # Retrieve certain scenes by their scene number.
    # Example: retrieve scene objects 1 and 2.
    # print littleMermaid.get_scenes_by_nums([1,2])

    # Remove a scene by its number.
    # Example: Remove scene 2.
    # littleMermaid.remove_scene(2)

    # Remove all scenes.
    # littleMermaid.remove_scenes()

    # Remove certain scenes by their scene number.
    # Example: remove scenes 1 and 3, if they exist.
    # littleMermaid.remove_scenes([1,3])

    ''' Add, remove, or retrieve assertions or StoryPoints (objects that store the assertions at distinct story time points) in a scene. '''
    # Retrieve a scene's StoryPoints.
    # Example: retrieve StoryPoint objects from scene 1.
    # print littleMermaid.get_storypoints(1)

    # Retrieve assertion objects from a given scene and StoryPoint.
    # Example: retrieve assertions from scene 1, storypoint 2.
    # print littleMermaid.get_storypoint_assertions(1,2)

    # Add a StoryPoint to a scene.
    # Example: add a storypoint to scene 1.
    #  - You can also use this command to add any assertion to the Story.
    # newAssertion = {
    #     "l": ["Eric","sailors"],
    #     "relation": "action",
    #     "r": ["pat"],
    #     "action_object": ["Grimsby"],
    #     "location":["on"],
    #     "location_object":["the back"],
    #     "location_object_owner":["Grimsby"],
    #     "with_property": ["sympathetic"],
    #     "storypoints": [
    #       {"at": 5}
    #     ],
    #     "scene":"1",
    #     "tense":"past"
    # }
    # littleMermaid.add_assertion(newAssertion)

    ''' Access, add, edit, or remove a scene setting. '''
    # Access a scene's setting.
    # Example: retrieve the setting for scene 2, if any.
    #  - This will return "" if there is no setting.
    # littleMermaid.get_setting(2)

    # Add/edit a full setting to a scene.
    # Example: add a setting to scene 3.
    #  - Parameters are sceneNum, time, place, and general_place.
    #  - Use the empty string if you don't want to list part of a setting.
    #  - You can also use this command to replace a prior setting instead of using edit_setting.
    # littleMermaid.add_setting(3, "evening", "lighthouse", "INT.")

    # Edit one part of a setting.
    # Example: change the time for scene 2.
    # littleMermaid.edit_setting(2, "time", "morning")

    # Remove a setting.
    # Example: remove scene 2's setting.
    # littleMermaid.remove_setting(2)

    ''' Find, add, edit, or remove an actor. '''
    # Retrieve all actors (as a list of Actor objects) in the story.
    # print littleMermaid.get_actors()

    # Retrieve the names of all actors in the story.
    # print littleMermaid.get_actor_names()

    # Retrieve an actor object given the actor's name or keyword.
    # print littleMermaid.get_actor("Seahorse Herald")

    # Remove a single actor from the story by their keyword or name.
    # littleMermaid.remove_actor("Grimsby")

    ''' Realize the story, or parts of the story. '''
    # Realize the entire story.
    # (Only assertions with specified scenes/storypoints will be realized.)
    print "\n* * *"
    littleMermaid.realize()
    print "* * *\n"

    # Realize a story assertion, given the story brain.
    # Example: realize the 0th assertion in Scene 1, StoryPoint 2.
    # assertion = littleMermaid.get_storypoint_assertions(1,2)[0]
    # assertion.realize(littleMermaid.brain, False)

    # Example 2: realize a custom assertion.
    # assertion2 = Assertion.Assertion({
    #     "l": ["porpoises"],
    #     "relation": "action",
    #     "r": ["swim"],
    #     "with_property":["happy"],
    #     "storypoints": [{"begin": 0, "end": 1}]
    # })
    # assertion2.realize(littleMermaid.brain, False)

    print "Process completed."

if __name__ == '__main__':
    main()
