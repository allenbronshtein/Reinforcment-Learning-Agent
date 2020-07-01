# Details : 206228751 Allen Bronshtein
from sys import argv
import learner
import executer
import tools
from inspect import currentframe, getframeinfo

frameinfo = getframeinfo(currentframe())

if len(argv) != 5:
    tools.print_error("Bad number of arguments", frameinfo.filename, getframeinfo(currentframe()).lineno)

tools.init()

if argv[1] == "-L":
    learner.run()
elif argv[1] == "-E":
    executer.run()
else:
    tools.print_error("Bad arguments", frameinfo.filename, getframeinfo(currentframe()).lineno)

tools.close()
