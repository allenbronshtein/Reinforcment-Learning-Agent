# Details : 206228751 Allen Bronshtein
import data
import tools
import math_class
import random
from inspect import currentframe, getframeinfo

frameinfo = getframeinfo(currentframe())
FirstAction = True
food_location = None
init_state = {}
choose_randomly = True


# Input : PDDL action
# Output : action name
def actionName(action):
    return action.split(" ")[0][1:]


# Input : PDDL state
# Output : state name (where i currently am)
def stateName(state):
    return list(state.get("at"))[0][1]


# Input : an action name, with list of actions (PDDL)
# Output : The action with same name , in PDDL
def actionName_to_pddlAction(action_name, actions):
    for action in actions:
        if action_name == actionName(action):
            return action
    return None


# Input : PDDL state and PDDL actions
# Output : Returns PDDL action with greatest quality
def choose_action(current_state, actions):
    global choose_randomly
    if len(actions) == 0:
        return None
    elif len(actions) == 1:
        return actions[0]
    if choose_randomly:
        choose_randomly = False
        return random.choice(actions)
    else:
        choose_randomly = True
        state = stateName(current_state)
        size = len(actions)
        action = actions[0]
        action_quality = data.get_action_quality((state, actionName(action)))
        for i in range(1, size):
            action_name = actionName(actions[i])
            quality = data.get_action_quality((state, action_name))
            if quality > action_quality:
                action = actions[i]
                action_quality = quality
        return action


class MazeLearner(object):
    def __init__(self):
        self.successor = None

    def initialize(self, services):
        global init_state
        self.services = services
        init_state = self.services.perception.get_state()
        data.init_Qtable(init_state.get("empty"))
        data.init_states(init_state.get("empty"))

    def next_action(self):
        # ---------------------- Runtime init ----------------------------------- #
        global FirstAction
        required_actions = []
        current_state = self.services.perception.get_state()
        state_name = stateName(current_state)
        actions = self.services.valid_actions.get()
        actions_names = []
        for action in actions:
            actions_names.append(actionName(action))
        # In runtime delete actions that cannot be executed
        for action in actions_names:
            required_actions.append(action)
        data.remove_uneeded_actions(state_name, required_actions)
        # ----------------------------------------------------------------------- #

        # Food picked up
        if self.services.goal_tracking.reached_all_goals():
            global food_location
            food_location = list(current_state.get("at"))[0][1]
            return None

        action = choose_action(current_state, actions)
        if FirstAction:
            tools.save_service((state_name, actionName(action)))
            FirstAction = False
        else:
            state_and_action = tools.load_service()
            value = math_class.bellmanCalc(state_name, actions_names)
            data.set_action_quality(state_and_action, value)
            tools.save_service((state_name, actionName(action)))
        return action


class MazeExecuter(object):
    def __init__(self):
        self.successor = None

    def initialize(self, services):
        global food_location, init_state
        self.services = services
        init_state = self.services.perception.get_state()
        data.init_states(init_state.get("empty"))

    def next_action(self):
        policy = tools.policy_str_to_dict(tools.read_policy())
        state = self.services.perception.get_state()
        state_name = stateName(state)
        if self.services.goal_tracking.reached_all_goals():
            return None
        actions = self.services.valid_actions.get()
        action = policy[state_name].strip("\'")
        action = actionName_to_pddlAction(action, actions)
        return action
