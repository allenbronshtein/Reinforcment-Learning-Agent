# Details : 206228751 Allen Bronshtein
import tools
from pddlsim.local_simulator import LocalSimulator
from agent import MazeExecuter


# Runs the executer
def run():
    print LocalSimulator().run(tools.getDomain(), tools.getProblem(), MazeExecuter())
