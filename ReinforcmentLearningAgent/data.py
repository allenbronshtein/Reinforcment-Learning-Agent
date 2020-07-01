# Details : 206228751 Allen Bronshtein
import tools
from inspect import currentframe, getframeinfo

frameinfo = getframeinfo(currentframe())

q_table = {}
states = []
actions = ["move-north0", "move-north1", "move-north2", "move-north3", "move-east0", "move-east1", "move-east2",
           "move-east3", "move-south0", "move-south1", "move-south2", "move-south3", "move-west0", "move-west1",
           "move-west2", "move-west3", "pick-food"]
states_not_handled = []
alpha = 0.5
gama = 0.9
reward_empty = -0.04
reward_food = 1


def is_not_handled(state_name):
    if state_name in states_not_handled:
        return True
    return False


def handled(state_name):
    if state_name in states_not_handled:
        states_not_handled.remove(state_name)


def init_Qtable(state_set):
    global q_table
    qtable_str = tools.read_qtable()
    # QTABLE IS EMPTY
    if qtable_str == "":
        for state in state_set:
            state = state[0]
            states_not_handled.append(state)
            for action in actions:
                q_table[(state, action)] = 0

    else:
        q_table = tools.qtable_str_to_dict(qtable_str)


def get_action_quality((state, action)):
    return q_table.get((state, action))


def set_action_quality((state, action), value):
    key = (state, action)
    del q_table[key]
    q_table[key] = value


def remove_uneeded_actions(state_name, needed_actions):
    global actions
    uneeded_keys = []
    uneeded_actions = tools.copy(actions)
    for action in needed_actions:
        uneeded_actions.remove(action)
    for action in uneeded_actions:
        uneeded_keys.append((state_name, action))
    for key in uneeded_keys:
        if key in q_table:
            del q_table[key]


def get_Qualities(state_name, actions_names):
    qualities_list = []
    for action in actions_names:
        quality = q_table.get((state_name, action))
        qualities_list.append(quality)
    return qualities_list


def init_states(state_set):
    for state in state_set:
        states.append(state[0])
