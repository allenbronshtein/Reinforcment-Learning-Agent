# Details : 206228751 Allen Bronshtein
import tools
from pddlsim.local_simulator import LocalSimulator
from agent import MazeLearner
import data
import BFS


def update_policy():
    policy = {}
    for state in data.states:
        if state is not BFS.goal:
            policy[state] = BFS.find(state)
    tools.write_policy(str(policy))


def learn():
    LocalSimulator().run(tools.getDomain(), tools.getProblem(), MazeLearner())
    BFS.init()


# Runs the learner
def run():
    learn()
    tools.write_qtable(str(data.q_table))
    update_policy()
