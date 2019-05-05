
from random_mode import *
from trace_mode import *
filename='num_tests.txt'
with open(filename) as f:
    num_tests_content=f.readlines()
    # print(num_tests_content)
num_tests=int(num_tests_content[0])

for test_index in range(1,num_tests+1):
    #open mode
    modename="mode_"+str(test_index)+".txt"
    with open(modename) as f:
        mode_content=f.readlines()
    mode_content = [x.strip() for x in mode_content]
    while '' in mode_content:
        mode_content.remove('')
    mode=mode_content[0]
    # print(mode)
    if mode=="trace":
        simulation_trace(test_index)
    if mode=="random":
        simulation_random(test_index)
