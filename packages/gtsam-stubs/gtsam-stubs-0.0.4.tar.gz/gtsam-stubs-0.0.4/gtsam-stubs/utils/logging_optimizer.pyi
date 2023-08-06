from gtsam import NonlinearOptimizer as NonlinearOptimizer, NonlinearOptimizerParams as NonlinearOptimizerParams, Values
from typing import Any, Callable

""" Given an optimizer and a convergence check, iterate until convergence.
    After each iteration, hook(optimizer, error) is called.
    After the function, use values and errors to get the result.
    Arguments:
        optimizer (T): needs an iterate and an error function.
        check_convergence: T * float * float -> bool
        hook -- hook function to record the error
"""
def optimize(optimizer: NonlinearOptimizer, check_convergence: Callable[[NonlinearOptimizer, float, float], bool], hook: Callable[[NonlinearOptimizer, float], None]) -> None: ...

""" Given an optimizer and params, iterate until convergence.
    After each iteration, hook(optimizer) is called.
    After the function, use values and errors to get the result.
    Arguments:
            optimizer {NonlinearOptimizer} -- Nonlinear optimizer
            params {NonlinearOptimizarParams} -- Nonlinear optimizer parameters
            hook -- hook function to record the error
"""
def gtsam_optimize(optimizer: NonlinearOptimizer, params: NonlinearOptimizerParams, hook: Callable[[NonlinearOptimizer, float], None]) -> Values: ...
