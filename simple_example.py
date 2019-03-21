#!/usr/bin/env python

"""
Author: Liam Abrahams
Desription:
    Example of how to run a simple multiprocess example.
"""

import multiprocess


# function
def simple_function1(iteration_list, a, b):
    outputs = []
    for iteration in iteration_list:
        output = (a*iteration) + (b*iteration*2)
        outputs.append(output)
    return outputs


iterations = list(range(10))

# linerar
linear_output = simple_function1(iterations, 10, 20)
print(linear_output)
# multiprocess

multiprocess_output = multiprocess.run_in_parallel(iterations, [10, 20], simple_function1)
print(multiprocess_output)
