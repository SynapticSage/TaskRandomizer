# --------------------------------------------------------------------------------------------
#Author:            Ryan Young
#Contents:          LS, Task, TaskStructure Classes and Methods; and Testing
#Date Started       July 21, 2013
#
#
#Description:
#   File contains basic classes and operational procedures for a virtual "Lazy Suzan". I plan to put it to use picking
#   which task to take on when I become less interested with the current task I'm working on, at the suggestion of David Eagleman.
#   It needs to have the flexibility to a store a hierarchy of tasks, and select at random from the
#   tasks a new task. Inherent in the selection of a new task, the lazy suzan must keep track of the current task
#   I'm working on, as well as the priority of tasks. Future capabilities may be added to the class to support different
#   styles of work and productivity as I think of them. For now, this is my attempt to imbue a general framework for
#   the classes.
#
#Planned changes:
#   ???
#
#
# --------------------------------------------------------------------------------------------

#IMPORTS
import random
import time
import Queue

#CLASSES AND GLOBAL VARIABLES
# -------------------------------
#Class name:        Task

#Description:       Contains properties necessary for a task, and any methods for printing or formatting its information
#                   for other objects or python to use.
# -------------------------------
#This is the new file that requires a new form of processing
class Task(object):
    def __init__(self, description, id = 0, hierarchical_level = 0, task_importance = 1, parent = None):

        #MAIN INFORMATION
        self.description = description
        self.super_task = parent                  #ie this is the parent task
        self.sub_tasks = []

        #FURTHER IDENTIFIER INFORMATION
        self.task_info = {}
        self.task_info["id"] = id
        self.task_info["hierarchical_level"] = hierarchical_level
        self.task_info["importance"] = task_importance       #In the future, this number will be used to gauge how likely it
                                                    # is for the selection algorithm to choose this particular task.
        #KEEPING TRACK OF TIME
        self.task_info["total_time"] = 0                #TODO Task class -- need method to often resample time of a task, not simply every time a new task is selected.
        self.task_info["temp_start_time"] = None

    def addSubTask(self, description, id = 0, ast_importance = 1):
        #TODO Task::addSubTask() .. make the method return the task object added? -- for the purpose of the queue method in the LazySuzan object
        self.sub_tasks.append( Task(description, id, self.task_info["hierarchical_level"] + 1, parent=self, task_importance=ast_importance ) )


    def searchSubDescription(task = None, description = ""):
        #TODO Task::searchSubDescription() -- searchSubTask, fix parameter order in parameter list

        found = False
        #Check for an empty list structure
        if(not task == None and len(task.sub_tasks) > 0):
            #return that (1) that no object was found, (2) therefore no level found, (3) therefore task = None


            for subtask in task.sub_tasks:
                if(subtask.description == description):
                    found_task = subtask
                    found = True

            if(not found):
                #return [Found, found_task.task_info["hierarchical_level"], found_task]
                for subtask in task.sub_tasks:
                    branch_search_vec = Task.searchSubDescription(subtask, description)
                    found = branch_search_vec[0]
                    if(found):
                        found_task = branch_search_vec[2]
                        break
        if(not found):
            return [False, None, None]
        else:
            return [found, found_task.task_info["hierarchical_level"], found_task]

    def searchSubID(task = None, id = 0):

        found = False
        #Check for an empty list structure
        if(not (task == None)  and (len(task.sub_tasks) > 0)):
            #return that (1) that no object was found, (2) therefore no level found, (3) therefore task = None
            for sub_task in task.sub_tasks:
                if(sub_task.task_info["id"] == id):
                    found_task = sub_task
                    found = True

            if(not found):
                #return [Found, found_task.task_info["hierarchical_level"], found_task]
                for sub_task in task.sub_tasks:
                    branch_search_vec = Task.searchSubID(sub_task, id)
                    found = branch_search_vec[0]
                    if(found):
                        found_task = branch_search_vec[2]
                        break
        if(not found):
            return [False, None, None]
        else:
            assert (found_task != None)                                             #Making sure there's not a "None" returned
            return [found, found_task.task_info["hierarchical_level"], found_task]

    def subTask_weightArray(self, no_parents = False):
        #METHOD primarily for the purpose of implementing recursive weighted array of the entire TaskStructure class
        #loop that constructs the sub_weight_array.
        return_array = []

        #populate the return array
        if(no_parents == True):
            for elem in self.sub_tasks:
                if (elem.sub_tasks != []):
                    return_array = return_array + elem.subTask_weightArray(True)
                #in which case we arrived at a child node, and populate the array with copies of id# based on
                #importance
                else:
                    for i in range(0,elem.task_info["importance"]):
                        return_array.append(elem.task_info["id"])
        else:
            for elem in self.sub_tasks:
                #add ids into array for parent node
                for i in range(0,elem.task_info["importance"]):
                        return_array.append(elem.task_info["id"])
                #search for children nodes
                if (elem.sub_tasks != []):
                    return_array = return_array + elem.subTask_weightArray(False)

        return return_array
    def __str__(self):
    #TODO Task:__str__() improve string formatting with "-------------"
        # This will have to return a string referencing the description of the object as well as the sub_task
        # list of the object.

        object_string = ""
        tabs_string = self.task_info["hierarchical_level"] * "\t"
        sep_string = "---------------------"
        new_line = "\n"

        object_string = new_line + tabs_string + "TASK=\"" + self.description + "\""
        if(len(self.sub_tasks) > 0):
            object_string = object_string + "\n" + tabs_string + "=>SUBTASKS=[ "

            #have to add all the sub_tasks into the string one by one
            for i in self.sub_tasks:
                object_string = object_string + str(i)
            object_string = object_string + "\n" + (tabs_string +"\t") + "]"

        return object_string

    def __print__(self):
        print(str(self))

    def startTask(self):
        #Method for primarily starting the counter, when a task first begins
        global time
        self.task_info["temp_start_time"] = time.time()

    def timeUpdate(self):
        #method for updating the time property of a task

        #import the global object yielding system time
        global time

        #getting start and stop times
        start_time, stop_time = self.task_info["temp_start_time"], time.time()

        #check if start time had a legit value!! if it does not have this, it
        # is likely and indeed probable that the object was not properly started!
        if (start_time != None):
            raise "start_time does not take on a valid value."
        assert(start_time != None)

        #find the difference
        time_difference = stop_time - start_time

        #update teh total time spent
        self.task_info["temp_start_time"] = self.task_info["temp_start_time"] + time_difference

        #resetting temporary start time for next call of this function
        self.task_info["temp_start_time"] = stop_time

# -------------------------------
#Class Name:        TaskStructure

#Description:       This contains a structure of tasks, where each task can itself be a list of elements. This means,
#                       that the element needs to keep track
#                       of whether it's a base element, i.e., a Task, a description of a task, or whether it's a list
#                       of elements.
# -------------------------------
class TaskStructure(object):
    def __init__(self):
        #Create the root task
        #The primary piece of the TaskStructure is the root task, which stores references via its sub task to its
        #
        global Task
        self.list_structure = Task("Task List")

        #Variable to keep track of task_information
        self.next_id = 0
        self.number_of_levels = 0

    #METHODS FOR ADDITION AND REMOVAL OF NODES ...

    # -------------------------------
    #Method Name:     addTask
    #
    #Description:     It inputs a new list or base element, somewhere into the task structure. At some point, there needs to be a method for
    #                 converting a base element into a list, if it is called upon by this method. At that point the user is specifying a
    #                 desire to convert that base element into a list of tasks. (Which causes me to realize it's time for the Task object to
    #                 be upgraded.)

    #Inputs:          self object = so that we can look for a requested object in the structure.
    #                 description = the task descrption to add.
    #                 which_object = which object's list to add the new task to.
    #                               this NEEDS to be able to spell-out a location on the list.
    #
    #Return:           It returns nothing - i.e. void.
    # -------------------------------
    def addTask(self, description, to_which_descriptor = None, at_importance = 1):

        if (to_which_descriptor == None):
            self.list_structure.addSubTask(description, self.next_id)
        else:
            task_vec = self.searchTaskStructure(to_which_descriptor)
            if(not task_vec[0]):
                print("WARNING: DESCRIPTOR SOUGHT NOT FOUND!")
                assert(not task_vec[0])
            else:
                task_vec[2].addSubTask(description, self.next_id, ast_importance=at_importance)

                #this is how the method keeps track of the number of levels within the TaskStructure object.
                if(task_vec[1] > self.number_of_levels):
                    self.number_of_levels = task_vec[1]

        #INCREMENT NEXT_ID of the TaskStructure
        self.next_id = self.next_id + 1

    def removeTask(self, description):
        search_vec = self.searchTaskStructure(description)
        found = search_vec[0]
        if not found:
            raise TS_Exception()
        else:
            #We move into the parent task, and remove the found task from the list
            found_task = search_vec[2]

            parent_task = found_task.super_task
            parent_task.sub_tasks.remove(found_task)

    #This method will search out the task structure with a depth-first approach (because that's easiest!)
    #Outputs:       [x, y, z] .. where x = whether a sub_task element was found within the task or not.
    #                           y = the level at which the task was found (is this redundant, because it's contained in z
    #                           TODO TaskStructure::searchTaskStructure() eliminate the second element of search output: it's redundant.
    #                           and z = the task found, which is equal to None if no task found at or
    #                           below the specified level
    #Inputs:        Task   .. it's default value is self, and it specifies the
    def searchTaskStructure(self, which_description= None):
        return Task.searchSubDescription(self.list_structure, which_description)

    def searchTaskStructureID(self, which_id= None):
        return Task.searchSubID(self.list_structure, which_id)

    #Method:        weightArray
    #Use:           Provides an array of task ids, with multiple copies of each id based upon importance. Basically, it
    #               forms a population to sample a new task from when we care about the importance of the various tasks.
    #Return:        array [] of integers representing ids in the tree that can represent a potential new task for the
    #               LS object to select, and embark upon.
    def normalWeightArray(self):
        #TODO -- TaskStructure::weightArray implement the method!
        #This method will provide the vanilla weight array for selectin of future tasks.
        return self.list_structure.subTask_weightArray(True)

    #OUTPUT METHODS
    def __str__(self):
        #We need a better way to stringify this structure!!! This is passable, but certainly not ideal.
        str_string = str(self.list_structure)
        return str_string
    def __print__(self):
        print(str(self))

# -------------------------------
#Class Name:        LazySuzan
#Description:       This is an abstract class specifying the basic features of a LazySuzan.
# -------------------------------
class LS(object):
    #TODO LS class ought to have a copy constructor parameter... and note that it can be combined within the actual constructor
    def __init__(self):
        global TaskStructure
        self.current_task = ""
        self.task_structure = TaskStructure()

        self.task_history = Queue.Queue(100) #list to keep tabs on the previous 100 tasks -- a queue object if possible
                                #   this will be both for future methods, and to implement a reduced priority when
                                #   spinning the LazySuzan for selection of past tasks, according to some selection
                                #   function. This will likely be a priori in early versions of this code, but later
                                #   versions will include a mechanism for inputting new functions for selection.


    def __str__(self):
        string_ret = "Current Task = \t" + str(self.current_task) + "\nTask Structure = \t" + str(self.task_structure);
        return string_ret
    def __print__(self):
        print(str(self))

    #Needs a way to take a random number, and pick a task in the list. This might be a good time to add a task
    #   count to list structure, and add a task identifier number to each task element.
    #This method will need a way to swtich between the normal selection method, and the importance weighted selection methods.
    def selectTask(self, use_importance = True):
        #TODO !!! separate the act of taking task time from the selectTask method + incoporate the new method
        global random, time

        #generate a random number that will symbolize one of the ids in the self.task_structure
        # next_id = self.task_structure.next_id
        # rand_id = random.randrange(0, next_id)

        # #generate importance-weighted array of possible ids!
        i_weighted_array = self.task_structure.normalWeightArray()
        rand_element_index = random.randrange(0,len(i_weighted_array))
        #
        #
        # #stil have to implement the ID search method!
        #
        # #obtain the initial id we will try
        id_to_get = i_weighted_array[rand_element_index]

        #obtain element associated with the id
        # new_current_task_vec = self.task_structure.searchTaskStructureID(id_to_get)
        new_current_task_vec = self.task_structure.searchTaskStructureID(id_to_get)
        found = new_current_task_vec[0]
        found_task = new_current_task_vec[2]

        #check to see if it's a valid element, and if not, pick another
        #validity is defined by the task element having no children tasks --l PERHAPS THIS CAN BE BUILT INTO THE weightArray() mechanism?
        while( not found or (len(found_task.sub_tasks) > 0)   ):

            #generate a random number that will symbolize one of the ids in the self.task_structure
            rand_id = random.randrange(0, next_id)
            print ("loop!" + "random id # = " + str(rand_id))

            #stil have to implement the ID search method!
            new_current_task_vec = self.task_structure.searchTaskStructureID(rand_id)
            found = new_current_task_vec[0]
            found_task = new_current_task_vec[2]

        #LET'S FINISH OFF THE TIME CALCULATIONS
        #update the total time for the current task
        #find the task of the current description
        if (self.current_task != ""):                                                                                                           #For some reason ... this is not a safegaurd!
            current_task_vec = self.task_structure.searchTaskStructure(self.current_task)
            if(current_task_vec[2] != None and current_task_vec[2].task_info["temp_start_time"] != None):                                       #Re-implement to not require first term!
                time_elapsed = (current_task_stop_time - current_task_vec[2].task_info["temp_start_time"])
                current_task_vec[2].task_info["total_time"] = current_task_vec[2].task_info["total_time"] + \
                                                              time_elapsed
                if(time_elapsed > 1):
                    print("...time elapsed on previous task... " + str(time_elapsed) + " seconds.")
        #update new task start time
        new_current_task_vec[2].task_info["temp_start_time"] = time.time()

        #UPDATE TASK DESCRIPTION
        self.current_task = new_current_task_vec[2].description


    def displayTask(self):
        pass


    def selectDisplayTask(self):
        #Because the two methods, selectTask and displayTask, are often used in
        #   conjunction, I wrote a combined method that calls each respectively, in
        #   sequence.
        self.selectTask()
        self.displayTask()

    #MODIFICATION METHODS FOR THE TASK STRUCTURE!
    def addTask(self, description, to_where = None, importance = 1):
        self.task_structure.addTask(description, to_where, at_importance=importance)

        #MOVE THE TASK ADDED INTO THE QUEUE
        self.historyEnqueue(description)

    def removeTask(self, description):
        self.task_structure.removeTask(description)

        #NOTICE: just because we remove a task from the data structure does NOT mean it ought be dequeued from the task_history.

    #METHODS FOR DEALING WITH THE HISTORY OF TASKS SELECTED OVER THE LIFETIME OF THE LAZY SUZAN
    def historyEnqueue(self, task):
        self.task_history.put_nowait(task)
    def historyDequeue(self):                                                                       #takse no more args on account that we
        return self.task_history.get_nowait()
    #Method:    historyDisplay
    #Does:      generates a visual of the task history
    #Type:      virtual method -- GUI and Console LZs will need to implement their own versions of
    #               this method.

    def historyDisplay(self):
        #No idea if this method works .. not sure if Queue object can be iterated across.
        count = 1
        #iterates over a list version of a copy of the Queue object!
        for element in list(self.task_history.queue):
            print("---------------------")
            print("ITEM N = " + str(count))
            print(str(element))
            count = count + 1
        print("---------------------")
    def historyReturn(self):
        pass
    #Method:    historyPosition
    #Does:      provides the position of a task in the history queue
    def historyPosition(self, task):
        count = 1
        for element in list(self.task_history.queue):
            if(element == task):
                print "history position = " + str(count)
            count = count + 1


#------ CHILDREN/IMPLEMENTATIONS OF LS CLASS -----
class LSconsole(LS):
    def displayTask(self):
        if(self.current_task != ""):
            print("You should be doing " + self.current_task + ".")

            #print out the time for the task
            current_task_vec = self.task_structure.searchTaskStructure(self.current_task)
            time_so_far = current_task_vec[2].task_info["total_time"]
            print("...time thus far... " + str(time_so_far) + " seconds.")
        else:
            print("You should be doing" + " ???")

class LSgui(LS):
    #TODO LSGui Implement graphical user interface version of LazySuzan class
    pass

class TS_Exception(Exception):
    #TODO TS_Exception flesh out the implementation some
    def __init__():
        self.message = "Task structure problem!"

class TestEnvironment:
    import Queue

    #THIS METHOD WILL BE USED TO ORGANIZE TEST OUTPUT INTO COHERENT PATTERNS!
    ################     DATA STRUCTURES UNDERLYING THE CLASS        #######################
    ########################################################################################
    #
    # {(number, ... ,number) -> string} => n-tuple specifies the position on the hierarchy
    #
    #
    #
    # [q | q in [1,0,[...]]] -> hierarchy keeping track of which tuples can be used to
    #                            elicit a string.
    #
    ########################################################################################
    def __init__(self):
        self.availability_tree = []          #This is a giant list structure that keeps
                                                  #track of which parts of the testing tree
                                                  #have strings!

        self.tuple_to_string = {}             #This maps from an n-tuple to a string

        #points to place on the data structure where the last add took place
        self.c_tuple = []                     # [ r | r in list[q | q in postive integers] ]
        self.c_phase = 0

        self.previous_level_data = Queue.Queue()         # Queue object that functions like a stack frame, storing previous [c_tuple, c_phase]
                                                   # states when moving between levels. We push values when incrementing levels, and we
                                                   # pop lists when moving down a level.


        # some endnotes for the methods -- tuple doesn't literally mean an n-tuple python object, (), but rather a list object
        # the purpose for this abstraction is that the python list object has mutable and object agnostic places in
        # its structure.
    #METHODS FOR MOVING AROUND AND ADDING TEST METHODS!
    def add_phase(self, test_string):

        print "got here"

        #mark the new location as taken
        self.setAvailabilityTaken()

        #create a tuple to access the dictionary object, and thence store a string
        location_to_add = self.c_tuple
        location_to_add.append(self.c_phase)

        #link string to tuple in dictionary
        self.tuple_to_string[tuple(location_to_add)] = test_string

        #increment the current phase position
        self.c_phase = self.c_phase + 1
    def setAvailabilityTaken(self):

        print "got here too!"
        #helper function that builds and runs code
        code_string = "self.availability_tree"
        if (self.c_tuple != ()):
          for i in self.c_tuple:
              code_string = code_string + "[" + str(i) + "]"
        code_string = code_string + "[" + str(self.c_phase) + "]" + " = 1"
        exec(code_string)

    def increment_level(self):
      self.previous_level_data.put_nowait([self.c_tuple,self.c_phase])

      #create a tuple to access the dictionary object, and thence store a string
      next_tuple = self.c_tuple
      next_tuple.append(self.c_phase)
      self.c_tuple = tuple(next_tuple)

      #reset phase
      self.c_phase = 0

    def decrement_level(self):
        previous_data = self.previous_level_data.get_nowait()

        self.c_tuple = previous_data[0]
        self.c_phase = previous_data[1]

    # PRINT METHODS, and helper methods
    def __print__(self):
        loc_list = self.getListLocations()
        #TEMPORARY CODE
        print loc_list
    def getListLocations(self,   = ()):
        list_loc = []
        location_temp = list(curr_loc)
        for i,v in enumerate(self.avaibility_tree):
            if (v == 1):
                list_loc.append(list(location_temp).append(i))
            elif (v == 0):
                pass
            elif (not v.empty()):
                list_loc = list_loc + self.getListLocations( tuple(list(location_temp).append(i)) )

        return list_loc
    def preambleString(location, mode = "default"):
        if(mode == "default"):
            preamble = "\t"*len(location) + location[len(location)-1] + ". "

####CODE TESTING!########


# T = TaskStructure()
# T.addTask("Finish IACUC Proceedures!")
# print("\n ---PHASE 1 of TESTING---")
# L = LSconsole()
# T.addTask("DO YOUR HOMEWORK.")
# T.addTask("Eat!")
# print(T.list_structure)
# print("T.next_id = " + str(T.next_id))
#
# vec = T.searchTaskStructure("Finish IACUC Proceedures!")
# for i in vec:
#     print(str(i))
#
# vec = T.searchTaskStructureID(2)
# for i in vec:
#     print(str(i))
#
# print(" ---End of PHASE 1---\n")
#
# print("Testing the new add method for the LazySuzan object...\n")
# L.addTask("Acquire beans.", importance=2)
# L.addTask("Purchase pantaloons.")
# L.addTask("Chase squirrels.")
# L.addTask("Find Bill Murray costume.")
#
# print("Testing str method of the LazySuzan object...\n")
# print(str(L))
#
# print("Selecting new task...\n")
# L.selectTask()
# print("Did LazySuzan object correctly select an available task at \"random\"? ...")
# print(str(L))
#
# print(" ---End of PHASE 2 ---\n")
#
# print(" ---Begin PHASE 3---\n")
# print("Adding subtasks to tasks in LazySuzan's TaskStructure object...")
# #To "Acquire beans." task
#
# print L.task_structure.normalWeightArray()
#
# print("------------------\nPrinting resulting task structure...")
# print( str(L) )
# print("--------------------------")
#
# for i in range(0,20):
#     print("----------------------\n---- L.selectDisplayTask() ----")
#     L.selectDisplayTask()
#     print("-----------------------")
#
# #TESTING OUT THE HISTORY FUNCTIONS
# L.historyDisplay()
# print("\n")
# print(str(L.historyPosition("Chase squirrels.")))
# print("\n")
#
# print ( "Normal weight array = " + str( L.task_structure.normalWeightArray() ) )
#
# print("END OF TEST CODE REACHED!")
# L.addTask("Go to HEB.","Acquire beans.")
# L.addTask("Find beans isle.","Acquire beans.",importance=2)
# L.addTask("Purchase beans.","Acquire beans.")
# L.addTask("Take beans home.","Acquire beans.", importance=3)

T = TestEnvironment()
T.add_phase("HelloWorld"); T.add_phase("Ask Jeeves!")
print T

