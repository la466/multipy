#!/usr/bin/env python

"""
Author: Liam Abrahams
Desription:
    Example of how to run a simple multiprocess example returning dictionary,
    but results from various processes have the same key. This will make a list
    of all results with the same key. This only works in parralel because if
    run linearly, you simply overwrite the key each time.
"""

import multiprocess

# function
def dictionary_example_same_key(iteration_list, a, b):
    outputs = {}
    for iteration in iteration_list:
        output = [a*iteration, b*iteration*2]
        outputs["test_key1"] = output
        outputs["test_key2"] = output*2
    return outputs


iterations = list(range(10))

# multiprocess
multiprocess_output = multiprocess.run_in_parallel(iterations, [10, 20], dictionary_example_same_key)
print(multiprocess_output)
