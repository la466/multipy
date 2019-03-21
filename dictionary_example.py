#!/usr/bin/env python

"""
Author: Liam Abrahams
Desription:
    Example of how to run a simple multiprocess example returning dictionary.
"""

import multiprocess


# function
def dictionary_example(iteration_list, a, b):
    outputs = {}
    for iteration in iteration_list:
        output = [a*iteration, b*iteration*2]
        outputs[iteration] = output
    return outputs


iterations = list(range(10))

# linear
linear_output = dictionary_example(iterations, 10, 20)
print(linear_output)

# multiprocess
multiprocess_output = multiprocess.run_in_parallel(iterations, [10, 20], dictionary_example)
print(multiprocess_output)
