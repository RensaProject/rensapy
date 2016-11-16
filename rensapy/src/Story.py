'''
A Story contains:
 - brain: a Rensa brain containing all of the Story's assertions.
 - size: the size of the Story, based on the brain.
 - points: each time point of the Story
 - scenes: points may be grouped into scenes of the Story
 - actors: all actors mentioned in the Story.

To assign a brain to an actor with the name "x", name the JSON file containing their brain assertions "x_brain.json".

To indicate which scene an assertion belongs to, you may either:
  1) Give that assertion a property called "scene".  The property's value should be the scene number.

  OR

  2) Place all the assertions for a scene in a single JSON file called "yourStoryName_sceneY.json", where Y is the scene number for those assertions.
'''

from Brain import *
from Entity import *
from SimpleRealizer import *

class Story(object):
    def __init__(self, brain):
        self.brain = brain
        self.update()

    def update(self):
        self.size = get_max_size(self.brain)
        self.scenes = self.init_scenes()
        if (len(self.scenes)==0):
            self.points = get_points(self.brain,self.size)
        self.actors = get_actors_from_brain(self.brain)

    # Retrieve the setting for a scene, given that scene's number.
    def get_setting(self, sceneNum):
        try:
            return realize_setting(self.scenes[str(sceneNum)].setting)
        except:
            return ""

    # Find the setting for a scene, and change its property to value.
    def edit_setting(self, sceneNum, property, value):
        try:
            self.scenes[str(sceneNum)].setting[property] = value
        except:
            print "Warning: could not edit setting in scene " + str(sceneNum) + "."

    # Remove the setting from a scene.
    def remove_setting(self,sceneNum):
        # Find the brain assertion for the setting, and remove it.
        ids = self.brain.get_assertion_ids_with({"l":["setting"],"relation":"has_value","scene":str(sceneNum)})

        self.remove_assertion_ids(ids)

    # Helper when we're removing certain ids from a story.
    def remove_assertion_ids(self, ids):
        removed = False
        for id in ids:
            self.brain.remove_assertion_with_id(id)
            removed = True

        # Only update if we've removed an assertion.
        if removed:
            self.update()

    # Add / edit the setting in a scene.
    # - Note that sceneNum should be a string in the assertion.  Otherwise, scene sorting will be confused by the different types (int vs. string).
    def add_setting(self, sceneNum, time, place, general_place):
        # If there is a previous setting for the scene, remove it.
        self.remove_setting(sceneNum)
        # Add the assertion to the Story brain.
        self.brain.add_assertion({"l":["setting"],"relation":"has_value","r":[{"time":time,"place":place,"general_place":general_place}],"scene":str(sceneNum)})
        # Update the Story based on its brain.
        return self.update()

    # Retrieve all scenes in a story.
    def get_scenes(self):
        return [v for k,v in self.scenes.iteritems()]

    # Retrieve a scene by its number.
    def get_scene(self, sceneNum):
        try:
            return self.scenes[str(sceneNum)]
        except:
            return None

    # Retrieve multiple scenes by their numbers.
    def get_scenes_by_nums(self, sceneNums):
        l = []
        for s in sceneNums:
            l.append(self.get_scene(s))
        return l

    # Remove a scene by its number.
    def remove_scene(self, sceneNum):
        # Find all assertions in the brain with the scene sceneNum, and remove them.
        ids = self.brain.get_assertion_ids_with({"scene":str(sceneNum)})
        self.remove_assertion_ids(ids)

    # Remove all scenes from a story.
    # - Optional parameter sceneNums is a list of specific scenes to remove.
    def remove_scenes(self, sceneNums = None):
        if sceneNums == None:
            ids = self.brain.get_assertion_ids_with_attributes(["scene"])
            self.remove_assertion_ids(ids)
        else:
            for s in sceneNums:
                self.remove_scene(s)

    # Retrieve StoryPoints from a given scene.
    def get_storypoints(self, sceneNum):
        try:
            return [v for k,v in self.get_scene(str(sceneNum)).points.iteritems()]
        except:
            return []

    # Retrieve assertions from a given scene and StoryPoint.
    def get_storypoint_assertions(self, sceneNum, pointNum):
        try:
            return self.get_storypoints(1)[pointNum].assertions
        except:
            return []

    # Add an assertion to the Story brain.
    def add_assertion(self, assertion):
        self.brain.add_assertion(assertion)
        self.update()

    # Initialize and organize scenes for a story.
    def init_scenes(self):
        scenes = {}

        # Iterate over all assertions.  Add each assertion to its assigned scene.
        for assertion in self.brain.get_assertions():
            if hasattr(assertion,"scene"):
                # This is the scene number corresponding to the assertion.
                num = assertion.scene
                # If there is no Scene in the scenes list with this scene number, add a new one.
                if num not in scenes:
                    scenes[num] = Scene()
                # If the Scene at the given index does not have the given assertion in its StoryPoints list,
                if not(scenes[num].has_assertion(assertion)):
                    #Add the assertion to that Scene at the correct StoryPoint.
                    scenes[num].add_assertion(assertion)

        # Iterate through all Scenes.
        for k, v in scenes.iteritems():
            # Make a brain out of the current Scene's assertions.
            sceneBrain = make_brain(v.assertions)
            # Get all assertions related to the setting value.
            settingAssertions = sceneBrain.get_assertions_with({"l":["setting"],"relation":"has_value"})
            # If the settingAssertions list isn't empty,
            if settingAssertions:
                # Define the scene setting.
                scenes[k].setting = settingAssertions[0]["r"][0]
            # Get all assertions related to the header value.
            headerAsserts = sceneBrain.get_assertions_with({"l":["header"],"relation":"has_value"})

            # If the header list isn't empty,
            if headerAsserts:
                # Define the scene header.
                scenes[k].header = headerAsserts[0]["r"][0]
                if hasattr(headerAsserts[0],"with_property"):
                    scenes[k].headerStyle=headerAsserts[0].with_property

            # Add StoryPoints to the current Scene.
            scenes[k].points = get_points(sceneBrain, get_max_size(sceneBrain))
        return scenes

    # Returns actor object if the given string matches the keyword or name of an Actor in this Story.
    def get_actor(self, str):
        for actor in self.actors:
            if str==actor.name:
                return actor
            elif str==actor.keyword:
                return actor
        return False

    # Returns all actor objects in the Story.
    def get_actors(self):
        return self.actors

    # Returns the names of all actor objects in the Story.
    def get_actor_names(self):
        l=[]
        for actor in self.actors:
            l.append(str(actor.name))
        return l

    # Removes all mention of an actor from the Story.
    # - Note that removal can have unintended consequences.  If you are removing all instances of an actor, you may end up removing crucial details of a story.
    def remove_actor(self, actorName):
        # Remove all assertions related to the actor in self.brain.
        actor = self.get_actor(actorName)
        if actor:
            keyword = actor.keyword
            name = actor.name

            # Get all assertions that contain the actor's keyword or name.
            keywordIDs = self.brain.get_assertion_ids_related_to(keyword)
            nameIDs = self.brain.get_assertion_ids_related_to(name)
            ids = keywordIDs + nameIDs

            for id in ids:
                # Here, we *could* just self.brain.remove_assertion_with_id(id).
                # However, we ideally only want to remove the id if no one else is featured in the assertion.  Otherwise, remove the actor from that part of the assertion.
                if id in self.brain.assertions:
                    a = self.brain.assertions[id].to_pruned_dict()
                    # Check each property in the assertion.  If actor name is in a value that is a list, or a value inside a list of dictionaries, remove actorName.
                    for k,v in a.iteritems():
                        if name in v or keyword in v:
                            # Edit the assertion so the name/keyword is removed.
                            self.brain.edit_assertion(id,k,[x for x in v if x != name and x != keyword])
                            # If we end up with just an empty list, remove the assertion entirely.
                            if [x for x in v if x != name and x != keyword]==[]:
                                self.brain.remove_assertion_with_id(id)
                                break
                        # If v is a list of dictionaries, search inside them and do the same as above.
                        if isinstance(v,list) and isinstance(v[0],dict):
                            for d in v:
                                for k2,v2 in d.iteritems():
                                    if isinstance(v2,list):
                                        if name in v2 or keyword in v2:
                                            # Edit the assertion so the name/keyword is removed.
                                            self.brain.edit_assertion(id,k2,[x for x in v2 if x != name and x != keyword])
                                            # If we end up with just an empty list, remove the assertion entirely.
                                            if [x for x in v2 if x != name and x != keyword]==[]:
                                                self.brain.remove_assertion_with_id(id)
                                                break

            # Update the Story.
            self.update()
        else:
            print "Warning: no actor named " + actorName + "."

    # Realize the story in natural text.
    def realize(self):
        for scene,v in sorted(self.scenes.iteritems()):
            if v.header:
                print v.header
            if v.setting:
                realize_setting(v.setting)
            realizedAsserts = "  "
            lastWasDiscourse = True
            for p in v.points:
                # (If we realized a in v.points[p].assertions here, we'd see repeated assertions as they continued to be true.  For the sake of interesting storytelling, we're only going to realize assertions that are new.)
                for a in v.points[p].added:
                    if is_discourse_assertion(a):
                        if lastWasDiscourse:
                            realizedAsserts += realize_brain_assertion(self.brain, a, False) + "\n  "
                        else:
                            realizedAsserts += "\n  " + realize_brain_assertion(self.brain, a, False) + "\n  "
                        lastWasDiscourse = True
                    else:
                        lastWasDiscourse = False
                        realizedAsserts += realize_brain_assertion(self.brain, a, False) + " "
            print realizedAsserts

# Realize a setting assertion.
def realize_setting(setting):
    set = ""
    if setting["general_place"]:
        set += setting["general_place"] + " "
    if setting["place"]:
        set += setting["place"].upper() + " "
    if setting["time"]:
        set += setting["time"].upper()
    print set

'''
A Scene contains:
 - a setting, which is a dict containing values for:
      > time of day
      > location name
      > general location (interior, exterior, or both)
 - a linked list of StoryPoints that occur in that scene.
 '''
class Scene(object):
    def __init__(self):
        self.setting = {}
        self.points = []
        self.assertions = []
        self.header = ""
        self.headerStyle = []

     # Check if this Scene has an assertion.
    def has_assertion(self,assertion):
        return assertion in self.assertions

    # Add an assertion to this Scene.
    def add_assertion(self,assertion):
        self.assertions.append(assertion)

'''
A StoryPoint represents a single time step in a story.

Each StoryPoint has a list of assertions that are true at the same point in time.
'''
class StoryPoint(object):
    def __init__(self):
        self.assertions = []
        self.added = []
        self.removed = []

    def has_assertion(self,assertion):
        return assertion in self.assertions

    def add_assertion(self,assertion):
        self.assertions.append(assertion)

'''
Helper functions for organizing StoryPoints.
'''
def add_assertion_to_points(allPoints, idx, assertion):
    # If there is no StoryPoint at the given index,
    if idx not in allPoints:
        # Add a new empty StoryPoint.
        allPoints[idx] = StoryPoint()
    # If the StoryPoint at the given index does not have the given assertion,
    if not (allPoints[idx].has_assertion(assertion)):
        # Add the assertion to that StoryPoint.
        allPoints[idx].add_assertion(assertion)
    return allPoints

def add_assertion_to_points_for_range(allPoints, begin, end, assertion, maxSize):
    # If end is infinity, adjust to be the last index in the array.
    if (end=="Infinity"):
        end = maxSize

    # Add the given assertion between the begin and end timepoints.
    for i in range(begin, end):
        allPoints = add_assertion_to_points(allPoints, i, assertion)

    return allPoints

def get_points(brain,size):
    allPoints = {}

    # Iterate over all assertions and add to appropriate StoryPoints.
    for assertion in brain.get_assertions():
        if hasattr(assertion,"storypoints"):
            points = assertion.storypoints
            for point in points:
                if "at" in point:
                    allPoints = add_assertion_to_points(allPoints, point["at"], assertion)
                elif "begin" in point and "end" in point:
                    allPoints = add_assertion_to_points_for_range(allPoints, point["begin"], point["end"], assertion, size);
                else:
                    print "RENSA: Error organizing StoryPoints for point " + str(point) + "."

    # Update previous, next, added, and removed attributes.
    for k,v in allPoints.iteritems():
        # If k is zero, list of added assertions = list of all assertions for this StoryPoint.
        if k==0:
            allPoints[k].added = allPoints[k].assertions

        # If there is a StoryPoint at the previous index,
        if (k-1) in allPoints:
            # For all assertions in the current StoryPoint,
            for a in v.assertions:
                # If the previous storypoint doesn't have this assertion, add to list of added.
                if not(a in allPoints[k-1].assertions):
                    allPoints[k].added.append(a)
            # For all assertions in the previous StoryPoint,
            for b in allPoints[k-1].assertions:
                # If the current StoryPoint doesn't have this assertion, add to list of removed.
                if not (b in v.assertions):
                    allPoints[k].removed.append(b)
    return allPoints

'''
Get the max size of a Story brain.
'''
def get_max_size(brain):
    maxSize = 0
    for assertion in brain.get_assertions():
        if hasattr(assertion,"storypoints"):
            for point in assertion.storypoints:
                if "end" in point and point["end"] != "Infinity":
                    try:
                        maxSize = max(maxSize, point["end"]);
                    except:
                        print "RENSA: Error retrieving maxSize of Story when examining point: " + str(point) + "."
                elif "at" in point:
                    try:
                        maxSize = max(maxSize, point["at"]);
                    except:
                        print "RENSA: Error retrieving maxSize of Story when examining point: " + str(point) + "."
    return maxSize
