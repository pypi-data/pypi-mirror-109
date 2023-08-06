# -*- coding: utf-8 -*-

__all__ = [
    'absorption_probabilities',
    'committor_probabilities',
    'first_passage_probabilities',
    'first_passage_reward',
    'hitting_probabilities',
    'hitting_times',
    'mean_absorption_times',
    'mean_first_passage_times_between',
    'mean_first_passage_times_to',
    'mean_number_visits',
    'mean_recurrence_times',
    'mixing_time',
    'sensitivity'
]


###########
# IMPORTS #
###########

# Full

import numpy as np
import numpy.linalg as npl
import scipy.optimize as spo

# Internal

from .custom_types import *


#############
# FUNCTIONS #
#############

def absorption_probabilities(mc: tmc) -> oarray:

    if len(mc.transient_states) == 0:
        return None

    n = mc.fundamental_matrix

    if mc.is_absorbing:

        absorbing_indices = [mc.states.index(state) for state in mc.absorbing_states]
        transient_indices = [mc.states.index(state) for state in mc.transient_states]
        r = mc.p[np.ix_(transient_indices, absorbing_indices)]

        ap = np.transpose(np.matmul(n, r))

    else:

        recurrent_indices = [[*map(mc.states.index, recurrent_class)] for recurrent_class in mc.recurrent_classes]
        transient_indices = [mc.states.index(state) for state in mc.transient_states]
        r = np.zeros((len(transient_indices), len(recurrent_indices)), dtype=float)

        for i, transient_state in enumerate(transient_indices):
            for j, recurrent_class in enumerate(recurrent_indices):
                r[i, j] = np.sum(mc.p[transient_state, :][:, recurrent_class])

        ap = np.transpose(np.matmul(n, r))

    return ap


def committor_probabilities(mc: tmc, committor_type: str, states1: tlist_int, states2: tlist_int) -> oarray:

    if not mc.is_ergodic:
        return None

    if committor_type == 'backward':
        a = np.transpose(mc.pi[0][:, np.newaxis] * (mc.p - np.eye(mc.size, dtype=float)))
    else:
        a = mc.p - np.eye(mc.size, dtype=float)

    a[states1, :] = 0.0
    a[states1, states1] = 1.0
    a[states2, :] = 0.0
    a[states2, states2] = 1.0

    b = np.zeros(mc.size, dtype=float)

    if committor_type == 'backward':
        b[states1] = 1.0
    else:
        b[states2] = 1.0

    cp = npl.solve(a, b)
    cp[np.isclose(cp, 0.0)] = 0.0

    return cp


def first_passage_probabilities(mc: tmc, steps: int, initial_state: int, first_passage_states: olist_int) -> tarray:

    e = np.ones((mc.size, mc.size), dtype=float) - np.eye(mc.size, dtype=float)
    g = np.copy(mc.p)

    if first_passage_states is None:

        z = np.zeros((steps, mc.size), dtype=float)
        z[0, :] = mc.p[initial_state, :]

        for i in range(1, steps):
            g = np.dot(mc.p, g * e)
            z[i, :] = g[initial_state, :]

    else:

        z = np.zeros(steps, dtype=float)
        z[0] = np.sum(mc.p[initial_state, first_passage_states])

        for i in range(1, steps):
            g = np.dot(mc.p, g * e)
            z[i] = np.sum(g[initial_state, first_passage_states])

    return z


def first_passage_reward(mc: tmc, steps: int, initial_state: int, first_passage_states: tlist_int, rewards: tarray) -> float:

    other_states = sorted(list(set(range(mc.size)) - set(first_passage_states)))

    m = mc.p[np.ix_(other_states, other_states)]
    mt = np.copy(m)
    mr = rewards[other_states]

    k = 1
    offset = 0

    for j in range(mc.size):

        if j not in first_passage_states:

            if j == initial_state:
                offset = k
                break

            k += 1

    i = np.zeros(len(other_states))
    i[offset - 1] = 1.0

    reward = 0.0

    for _ in range(steps):
        reward += np.dot(i, np.dot(mt, mr))
        mt = np.dot(mt, m)

    return reward


def hitting_probabilities(mc: tmc, targets: tlist_int) -> tarray:

    target = np.array(targets)
    non_target = np.setdiff1d(np.arange(mc.size, dtype=int), target)

    hp = np.ones(mc.size, dtype=float)

    if non_target.size > 0:
        a = mc.p[non_target, :][:, non_target] - np.eye(non_target.size, dtype=float)
        b = np.sum(-mc.p[non_target, :][:, target], axis=1)
        x = spo.nnls(a, b)[0]
        hp[non_target] = x

    return hp


def hitting_times(mc: tmc, targets: tlist_int) -> tarray:

    target = np.array(targets)

    hp = hitting_probabilities(mc, targets)
    ht = np.zeros(mc.size, dtype=float)

    infinity = np.flatnonzero(np.isclose(hp, 0.0))
    current_size = infinity.size
    new_size = 0

    while current_size != new_size:
        x = np.flatnonzero(np.sum(mc.p[:, infinity], axis=1))
        infinity = np.setdiff1d(np.union1d(infinity, x), target)
        new_size = current_size
        current_size = infinity.size

    ht[infinity] = np.Inf

    solve = np.setdiff1d(list(range(mc.size)), np.union1d(target, infinity))

    if solve.size > 0:
        a = mc.p[solve, :][:, solve] - np.eye(solve.size, dtype=float)
        b = -np.ones(solve.size, dtype=float)
        x = spo.nnls(a, b)[0]
        ht[solve] = x

    return ht


def mean_absorption_times(mc: tmc) -> oarray:

    if not mc.is_absorbing or len(mc.transient_states) == 0:
        mat = None
    else:
        n = mc.fundamental_matrix
        mat = np.transpose(np.dot(n, np.ones(n.shape[0], dtype=float)))

    return mat


def mean_first_passage_times_between(mc: tmc, origins: tlist_int, targets: tlist_int) -> oarray:

    if not mc.is_ergodic:
        return None

    a = np.eye(mc.size, dtype=float) - mc.p
    a[targets, :] = 0.0
    a[targets, targets] = 1.0

    b = np.ones(mc.size, dtype=float)
    b[targets] = 0.0

    mfptt = npl.solve(a, b)

    pi_origin_states = mc.pi[0][origins]
    mu = pi_origin_states / np.sum(pi_origin_states)

    mfptb = np.dot(mu, mfptt[origins])

    return mfptb


def mean_first_passage_times_to(mc: tmc, targets: olist_int) -> oarray:

    if not mc.is_ergodic:
        return None

    if targets is None:

        a = np.tile(mc.pi[0], (mc.size, 1))
        i = np.eye(mc.size, dtype=float)
        z = npl.inv(i - mc.p + a)

        e = np.ones((mc.size, mc.size), dtype=float)
        k = np.dot(e, np.diag(np.diag(z)))

        mfptt = np.dot(i - z + k, np.diag(1.0 / np.diag(a)))
        np.fill_diagonal(mfptt, 0.0)

    else:

        a = np.eye(mc.size, dtype=float) - mc.p
        a[targets, :] = 0.0
        a[targets, targets] = 1.0

        b = np.ones(mc.size, dtype=float)
        b[targets] = 0.0

        mfptt = npl.solve(a, b)

    return mfptt


def mean_number_visits(mc: tmc) -> oarray:

    ccis = [[*map(mc.states.index, communicating_class)] for communicating_class in mc.communicating_classes]
    cm = mc.communication_matrix

    closed_states = [True] * mc.size

    for cci in ccis:

        closed = True

        for i in cci:
            for j in range(mc.size):

                if j in cci:
                    continue

                if mc.p[i, j] > 0.0:
                    closed = False
                    break

        for i in cci:
            closed_states[i] = closed

    hp = np.zeros((mc.size, mc.size), dtype=float)

    for j in range(mc.size):

        a = np.copy(mc.p)
        b = -a[:, j]

        for i in range(mc.size):
            a[i, j] = 0.0
            a[i, i] -= 1.0

        for i in range(mc.size):

            if not closed_states[i]:
                continue

            for k in range(mc.size):
                if k == i:
                    a[i, i] = 1.0
                else:
                    a[i, k] = 0.0

            if cm[i, j] == 1:
                b[i] = 1.0
            else:
                b[i] = 0.0

        hp[:, j] = npl.solve(a, b)

    mnv = np.zeros((mc.size, mc.size), dtype=float)

    for j in range(mc.size):

        ct1 = np.isclose(hp[j, j], 1.0)

        if ct1:
            z = np.nan
        else:
            z = 1.0 / (1.0 - hp[j, j])

        for i in range(mc.size):

            if np.isclose(hp[i, j], 0.0):
                mnv[i, j] = 0.0
            elif ct1:
                mnv[i, j] = np.inf
            else:
                mnv[i, j] = hp[i, j] * z

    return mnv


def mean_recurrence_times(mc: tmc) -> oarray:

    if not mc.is_ergodic:
        mrt = None
    else:
        mrt = np.array([0.0 if np.isclose(v, 0.0) else 1.0 / v for v in mc.pi[0]])

    return mrt


def mixing_time(mc: tmc, initial_distribution: tarray, jump: int, cutoff: float) -> oint:

    if not mc.is_ergodic:
        return None

    p = mc.p
    pi = mc.pi[0]

    d = initial_distribution.dot(p)
    tvd = 1.0

    mt = 0

    while tvd > cutoff:
        tvd = np.sum(np.abs(d - pi))
        mt += jump
        d = d.dot(p)

    return mt


def sensitivity(mc: tmc, state: int) -> oarray:

    if not mc.is_irreducible:
        return None

    lev = np.ones(mc.size, dtype=float)
    rev = mc.pi[0]

    a = np.transpose(mc.p) - np.eye(mc.size, dtype=float)
    a = np.transpose(np.concatenate((a, [lev])))

    b = np.zeros(mc.size, dtype=float)
    b[state] = 1.0

    phi = npl.lstsq(a, b, rcond=-1)
    phi = np.delete(phi[0], -1)

    s = -np.outer(rev, phi) + (np.dot(phi, rev) * np.outer(rev, lev))

    return s
