#!/usr/bin/env python

"""
Author: Liam Abrahams
Credit: Rosina Savisaar
Desription:
    Functions needed to run funcion in parallel
"""


import os
import multiprocessing
import collections


def run_in_parallel(iteration_list, sim_args, function_to_run, kwargs_dict = None, parallel = True, workers = None):
    """
    Wrapper to run simulation function

    Args:
        iteration_list (list): list to iteration function over
        sim_args (list): list of arguments to pass to the function
        function_to_run (func): function to run
        kawrgs_dict (dict): dictionary of keyword argument to pass to the function
        parallel (bool): if true, run in parallel, else run linearly
        workers (int): if set, use user defined number of processes

    Returns:
        outputs: returned output
    """

    # run the simulations
    if parallel:
        # add foo to argument list for parallelisation
        sim_args.insert(0, "foo")
        # get the number of workers to use
        if not workers:
            # minus 2 to allow some spare cpus
            workers = os.cpu_count() - 2
        # run the function
        processes = parallelise_function(iteration_list, sim_args, function_to_run, kwargs_dict = kwargs_dict, workers = workers)
        # now process the results
        # first get the results
        results = []
        for process in processes:
            results.append(process.get())
        # now merge into one
        # if you return a list from the function, combine the lists
        if isinstance(results[0], list):
            flattened_outputs = []
            [flattened_outputs.extend(i) for i in results]
            outputs = flattened_outputs
        # if you return a dictionary
        elif isinstance(results[0], dict):
            # get the keys
            keys = list(results[0].keys())
            # if keys exist
            if len(keys):
                # if the results have repeated keys, append each keys result to a list to merge all results
                # for one key to the same list
                if isinstance(results[0][keys[0]], list):
                    flattened_outputs = collections.defaultdict(lambda: [])
                    for result in results:
                        for key in result:
                            flattened_outputs[key].extend(result[key])
                    #unpickle
                    outputs = {i: flattened_outputs[i] for i in flattened_outputs}
                # otherwise, just add to one dictionary
                else:
                    flattened_outputs = {}
                    [flattened_outputs.update(i) for i in results]
                    outputs = flattened_outputs
            else:
                outputs = None
        else:
            outputs = None
    else:
        if kwargs_dict:
            # use keyword args
            outputs = function_to_run(simulations, *sim_args, **kwargs_dict)
        else:
            # no keyword args
            outputs = function_to_run(simulations, *sim_args)
    # return the outputs
    return outputs


def parallelise_function(input_list, args, func, kwargs_dict = None, workers = None, onebyone = False):
    """
    Take an input list, divide into chunks and then apply a function to each of the chunks in parallel.

    Args:
        input_list: a list of the stuff you want to parallelize over (for example, a list of gene names)
        args: a list of arguments to the function. Put in "foo" in place of the argument you are parallelizing over.
        func: the function to run
        kwargs_dict: a dictionary of any keyword arguments the function might take
        workers: number of parallel processes to launch
        onebyone: if True, allocate one element from input_list to each process
    """
    if not workers:
        #divide by two to get the number of physical cores
        #subtract one to leave one core free
        workers = int(os.cpu_count()/2 - 1)
    elif workers == "all":
        workers = os.cpu_count()
    #in the list of arguments, I put in "foo" for the argument that corresponds to whatever is in the input_list because I couldn't be bothered to do something less stupid
    arg_to_parallelize = args.index("foo")
    if not onebyone:
        #divide input_list into as many chunks as you're going to have processes
        chunk_list = [input_list[i::workers] for i in range(workers)]
    else:
        #each element in the input list will constitute a chunk of its own.
        chunk_list = input_list
    pool = multiprocessing.Pool(workers)
    results = []
    #go over the chunks you made and laucnh a process for each
    for elem in chunk_list:
        current_args = args.copy()
        current_args[arg_to_parallelize] = elem
        if kwargs_dict:
            process = pool.apply_async(func, tuple(current_args), kwargs_dict)
        else:
            process = pool.apply_async(func, tuple(current_args))
        results.append(process)
    pool.close()
    pool.join()
    return(results)
