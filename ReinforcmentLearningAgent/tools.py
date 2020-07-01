# Details : 206228751 Allen Bronshtein
import sys
from inspect import currentframe, getframeinfo
import os

frameinfo = getframeinfo(currentframe())

policy_file = ""
problem_name = ""
domain_name = ""
f = None
general_data_var = None


def init():
    global policy_file, problem_name, domain_name
    domain_name = sys.argv[2]
    problem_name = sys.argv[3]
    policy_file = sys.argv[4]


def print_error(line, fname, lnum):
    sys.stderr.write('\x1b[1;31m' + line + "\n" + '\x1b[0m')
    sys.stderr.write('\x1b[1;31m' + "File name: " + fname + "\n" + '\x1b[0m')
    sys.stderr.write('\x1b[1;31m' + "Line number: " + str(lnum) + "\n" + '\x1b[0m')
    close()
    exit(0)


def write_policy(line):
    global f
    if "\n" in line:
        line = line.strip("\n")
    f = open(policy_file, "w")
    f.write(line)
    f.close()


def read_policy():
    global f
    try:
        f = open(policy_file, "r")
    except:
        print_error("Error opening " + policy_file, frameinfo.filename, getframeinfo(currentframe()).lineno)
    buff = f.readline()
    if buff == "":
        print_error("No policy , please run learning first", frameinfo.filename,
                    getframeinfo(currentframe()).lineno)
    f.close()
    return buff


def getDomain():
    return domain_name


def getProblem():
    return problem_name


def close():
    if os.path.exists("tmp_problem_generation"):
        os.remove("tmp_problem_generation")


def save_service(entry):
    global general_data_var
    clear()
    general_data_var = entry


def load_service():
    return general_data_var


def clear():
    global general_data_var
    general_data_var = None


def copy(old_list):
    new_list = []
    for item in old_list:
        new_list.append(item)
    return new_list


def policy_str_to_dict(policy_str):
    policy = {}
    policy_list = policy_str.strip("{").strip("}").split(",")
    for entry in policy_list:
        entry_list = entry.split(":")
        key = entry_list[0].strip().strip("'")
        value = entry_list[1].strip()
        policy[key] = value
    return policy


def qtable_str_to_dict(qtable_str):
    first = True
    qtable = {}
    qtable_list = qtable_str.strip("{").strip("}").split(", (")
    for entry in qtable_list:
        entry_list = entry.split(":")
        key = entry_list[0]
        if not first:
            key = "(" + str(key)
        key = key.strip("(").strip(")").split(",")
        state = key[0].strip("'")
        action = key[1][2:-1]
        key = (state, action)
        value = float(entry_list[1].strip())
        qtable[key] = value
        first = False
    return qtable


def read_qtable():
    global f
    try:
        f = open("QTABLE", "r")
    except:
        print_error("Error opening QTABLE", frameinfo.filename, getframeinfo(currentframe()).lineno)
    buff = f.readline()
    f.close()
    return buff


def write_qtable(line):
    global f
    if "\n" in line:
        line = line.strip("\n")
    f = open("QTABLE", "w")
    f.write(line)
    f.close()
