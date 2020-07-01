import agent
import data
import tools
import math_class

goal = None
states = []
north_neighbor = {}
south_neighbor = {}
west_neighbor = {}
east_neighbor = {}
map_dict = {}
init_state = {}


# b is north of a
def is_north_of(a, b):
    if a in north_neighbor:
        if b == north_neighbor.get(a):
            return True
    return False


# b is south of a
def is_south_of(a, b):
    if a in south_neighbor:
        if b == south_neighbor.get(a):
            return True
    return False


# b is east of a
def is_east_of(a, b):
    if a in east_neighbor:
        if b == east_neighbor.get(a):
            return True
    return False


# b is west of a
def is_west_of(a, b):
    if a in west_neighbor:
        if b == west_neighbor.get(a):
            return True
    return False


def priority_insert(queue, item):
    queue.append(item)
    queue = sorted(queue, key=lambda tup: tup[0])
    queue.reverse()


def get_neighbors(state):
    neighbors = []
    if state in north_neighbor:
        neighbors.append(north_neighbor.get(state))
    if state in south_neighbor:
        neighbors.append(south_neighbor.get(state))
    if state in east_neighbor:
        neighbors.append(east_neighbor.get(state))
    if state in west_neighbor:
        neighbors.append(west_neighbor.get(state))
    return neighbors


def in_closed_q(item, closed):
    for entry in closed:
        if entry[1] == item:
            return True
    return False


def in_open_q(item, open_q):
    for entry in open_q:
        if entry[1] == item:
            return True
    return False


def init():
    global goal, states, init_state
    init_state = agent.init_state
    goal = agent.food_location
    states = tools.copy(data.states)
    init_north_south()
    init_east_west()
    init_map()


def find(start_state):
    update_prices()
    open_q = []
    closed_q = []
    solution = []
    null_state = (0, start_state, None)
    open_q.append(null_state)
    while len(open_q) is not 0:
        node = (open_q[0][0], open_q[0][1], open_q[0][2])
        open_q.pop(0)
        closed_q.append(node)
        if node[1] == goal:
            solution.append(node[1])
            parent = node[2]
            while parent is not null_state[2]:
                if parent == closed_q[0][1]:
                    solution.append(closed_q[0][1])
                    parent = closed_q[0][2]
                    closed_q.pop(0)
                else:
                    closed_q.append(closed_q[0])
                    closed_q.pop(0)
        else:
            neighbors = get_neighbors(node[1])
            for neighbor in neighbors:
                if in_closed_q(neighbor, closed_q):
                    continue
                top_quality_for_action = get_top_quality_for_action(node[1], neighbor)
                if not in_open_q(neighbor, open_q):
                    neighbor_state = (node[0] + top_quality_for_action, neighbor, node[1])
                    priority_insert(open_q, neighbor_state)
                else:
                    neighbor_state = (node[0] + top_quality_for_action, neighbor, node[1])
                    replace = False
                    for item in open_q:
                        if neighbor == item[1] and neighbor_state[0] > item[0]:
                            open_q.pop(0)
                            replace = True
                    if replace:
                        priority_insert(open_q, neighbor_state)
    solution.reverse()
    return adapt_solution_to_policy(solution)


def adapt_solution_to_policy(solution):
    action = "pick-food"
    if len(solution) > 1:
        current_state = solution[0]
        next_state = solution[1]
        if is_north_of(current_state, next_state):
            action = "move-north0"
            quality = data.get_action_quality((current_state, "move-north0"))
            for i in range(1, 4):
                temp_action = "move-north" + str(i)
                temp_quality = data.get_action_quality((current_state, temp_action))
                if temp_quality > quality:
                    quality = temp_quality
                    action = temp_action
        elif is_south_of(current_state, next_state):
            action = "move-south0"
            quality = data.get_action_quality((current_state, "move-south0"))
            for i in range(1, 4):
                temp_action = "move-south" + str(i)
                temp_quality = data.get_action_quality((current_state, temp_action))
                if temp_quality > quality:
                    quality = temp_quality
                    action = temp_action
        elif is_east_of(current_state, next_state):
            action = "move-east0"
            quality = data.get_action_quality((current_state, "move-east0"))
            for i in range(1, 4):
                temp_action = "move-east" + str(i)
                temp_quality = data.get_action_quality((current_state, temp_action))
                if temp_quality > quality:
                    quality = temp_quality
                    action = temp_action
        elif is_west_of(current_state, next_state):
            action = "move-west0"
            quality = data.get_action_quality((current_state, "move-west0"))
            for i in range(1, 4):
                temp_action = "move-west" + str(i)
                temp_quality = data.get_action_quality((current_state, temp_action))
                if temp_quality > quality:
                    quality = temp_quality
                    action = temp_action
    return action


def init_north_south():
    global north_neighbor, south_neighbor
    for predicate in list(init_state.get("north")):
        north_neighbor[predicate[0]] = predicate[1]
        south_neighbor[predicate[1]] = predicate[0]


def init_east_west():
    global east_neighbor, west_neighbor
    for predicate in list(init_state.get("east")):
        east_neighbor[predicate[0]] = predicate[1]
        west_neighbor[predicate[1]] = predicate[0]


def init_map():
    global map_dict
    for state in states:
        neighbors_list = []
        # state has north neighbor
        if state in north_neighbor:
            neighbor = north_neighbor.get(state)
            neighbors_list.append(("move-north0", neighbor, state, 0))
            if state in south_neighbor:
                neighbors_list.append(("move-north1", neighbor, south_neighbor[state], 0))
            if state in west_neighbor:
                neighbors_list.append(("move-north2", neighbor, west_neighbor[state], 0))
            if state in east_neighbor:
                neighbors_list.append(("move-north3", neighbor, east_neighbor[state], 0))

        # state has south neighbor
        if state in south_neighbor:
            neighbor = south_neighbor.get(state)
            neighbors_list.append(("move-south0", neighbor, state, 0))
            if state in north_neighbor:
                neighbors_list.append(("move-south1", neighbor, north_neighbor[state], 0))
            if state in west_neighbor:
                neighbors_list.append(("move-south2", neighbor, west_neighbor[state], 0))
            if state in east_neighbor:
                neighbors_list.append(("move-south3", neighbor, east_neighbor[state], 0))

        # state has east neighbor
        if state in east_neighbor:
            neighbor = east_neighbor.get(state)
            neighbors_list.append(("move-east0", neighbor, state, 0))
            if state in north_neighbor:
                neighbors_list.append(("move-east1", neighbor, north_neighbor[state], 0))
                neighbors_list.append(("move-east2", neighbor, north_neighbor[state], 0))
                neighbors_list.append(("move-east3", neighbor, north_neighbor[state], 0))

        # state has west neighbor
        if state in west_neighbor:
            neighbor = west_neighbor.get(state)
            neighbors_list.append(("move-west0", neighbor, state, 0))
            if state in north_neighbor:
                neighbors_list.append(("move-west1", neighbor, north_neighbor[state], 0))
                neighbors_list.append(("move-west2", neighbor, north_neighbor[state], 0))
            if state in east_neighbor:
                neighbors_list.append(("move-west3", neighbor, east_neighbor[state], 0))

        map_dict[state] = neighbors_list


def update_prices():
    global map_dict
    for state in states:
        map_list = list(map_dict.get(state))
        working_map_list = tools.copy(map_list)
        for entry in working_map_list:
            new_price = data.q_table.get((str(state), str(entry[0])))
            map_list.remove(entry)
            entry = (entry[0], entry[1], new_price)
            map_list.append(entry)
        del map_dict[state]
        map_dict[state] = map_list


def get_top_quality_for_action(current_state, next_state):
    value_list = []
    if is_north_of(current_state, next_state):
        for i in range(0, 4):
            action = "move-north" + str(i)
            reward = data.q_table.get((current_state, action))
            value_list.append(reward)
        return math_class.getMax(value_list)
    elif is_south_of(current_state, next_state):
        for i in range(0, 4):
            action = "move-south" + str(i)
            reward = data.q_table.get((current_state, action))
            value_list.append(reward)
        return math_class.getMax(value_list)
    elif is_east_of(current_state, next_state):
        for i in range(0, 4):
            action = "move-east" + str(i)
            reward = data.q_table.get((current_state, action))
            value_list.append(reward)
        return math_class.getMax(value_list)
    # Is west of
    for i in range(0, 4):
        action = "move-west" + str(i)
        reward = data.q_table.get((current_state, action))
        value_list.append(reward)
    return math_class.getMax(value_list)
