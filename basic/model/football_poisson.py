import numpy as np
from scipy.stats.distributions import poisson

MAX_GOALS = 13

def correct_score_grid(exp_home, exp_away, max_goals=MAX_GOALS):
    """ Calculate a probability space of given dimension using joint poisson pmf.
    Note: In prod this would need standardising to 1.
    """
    return np.fromfunction(lambda hgoals, agoals: poisson.pmf(hgoals, exp_home) * poisson.pmf(agoals, exp_away), (max_goals, max_goals))


def calc_mw(grid):
    """ Sum different subsets of the grid to calculate 1x2 probabilities."""
    home = np.sum(np.tril(grid, -1))
    draw = np.sum(np.diag(np.diag(grid)))
    away = np.sum(np.triu(grid, 1))

    return {"home": home, "draw": draw, "away": away}
