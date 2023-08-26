"""
MAPF utilities for clingo written in C++.
"""

from enum import IntEnum

from clingo._internal import _handle_error
from clingo.control import Control
from clingo.symbolic_atoms import SymbolicAtoms

from ._cmapf import ffi as _ffi
from ._cmapf import lib as _lib

__all__ = ["version", "add_sp_length", "add_reachable"]


class Objective(IntEnum):
    """
    The available MAPF objectives.
    """

    SUM_OF_COSTS = _lib.cmapf_objective_sum_of_costs
    MAKESPAN = _lib.cmapf_objective_makespan


def version():
    """
    The CMAPF version number.
    """
    p_major = _ffi.new("int*")
    p_minor = _ffi.new("int*")
    p_revision = _ffi.new("int*")
    _lib.cmapf_version(p_major, p_minor, p_revision)
    return p_major[0], p_minor[0], p_revision[0]


def compute_min_delta_or_horizon(ctl: Control, objective: Objective):
    """
    Compute the minimal delta or horizon value for which the mapf problem is not trivially unsatisfiable.

    Returns None if the problem is unsatisfiable.
    """
    res = _ffi.new("bool*")
    delta = _ffi.new("int*")
    _handle_error(
        _lib.cmapf_compute_min_delta_or_horizon(
            _ffi.cast("clingo_control_t*", ctl._rep), objective, res, delta
        )
    )
    if res[0]:
        return delta[0]
    return None


def add_sp_length(ctl: Control):
    """
    Add shortest paths.
    """
    res = _ffi.new("bool*")
    _handle_error(
        _lib.cmapf_compute_sp_length(_ffi.cast("clingo_control_t*", ctl._rep), res)
    )
    return res[0]


def add_reachable(ctl: Control, objective: Objective, delta_or_horizon: int):
    """
    Add reachable locations based on shortest paths/horizon.
    """
    res = _ffi.new("bool*")
    _handle_error(
        _lib.cmapf_compute_reachable(
            _ffi.cast("clingo_control_t*", ctl._rep), objective, delta_or_horizon, res
        )
    )
    return res[0]


def count_atoms(syms: SymbolicAtoms, name: str, arity: int):
    """
    Count the number of atoms over the given signature.
    """
    res = _ffi.new("int*")
    _handle_error(
        _lib.cmapf_count_atoms(
            _ffi.cast("clingo_symbolic_atoms_t*", syms._rep), name.encode(), arity, res
        )
    )
    return res[0]


__version__ = ".".join(str(num) for num in version())
