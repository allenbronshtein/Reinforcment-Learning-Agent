# Details : 206228751 Allen Bronshtein
import data
import tools
from inspect import currentframe, getframeinfo

frameinfo = getframeinfo(currentframe())
alpha = data.alpha
gama = data.gama
q_table = data.q_table
reward = data.reward_empty


# Input : List of numbers
# Output : max number
def getMax(my_list):
    max_var = None
    size = len(my_list)
    if size == 1:
        max_var = my_list[0]
        return max_var
    elif size != 0:
        max_var = my_list[0]
        for i in range(1, size):
            if my_list[i] > max_var:
                max_var = my_list[i]
    return max_var


# Q(s,a)+= a[r + gama*max{Q(s_next,a)} - Q(s,a)]
def bellmanCalc(state_name, actions_names):
    global reward
    if tools.load_service()[1] == "pick-food":
        reward = data.reward_food
    key = tools.load_service()
    prev_state_quality = data.q_table.get(key)
    current_state_qualities = data.get_Qualities(state_name, actions_names)
    max_val = getMax(current_state_qualities)
    new_state_quality = prev_state_quality
    new_state_quality += alpha * (reward + gama * max_val - prev_state_quality)
    reward = data.reward_empty
    return new_state_quality
