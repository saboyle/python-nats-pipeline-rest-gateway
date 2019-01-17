import unittest
import numpy as np

import basic.model
from basic.model import football_poisson

class TestCSGrid(unittest.TestCase):

    def test1(self):
        grid = football_poisson._correct_score_grid(2, 2)

        # It's v close to 1, close enough [normalize to 1 in production].
        self.assertTrue((1 - np.sum(grid)) < 0.00001)

        # The grid returned is a square
        self.assertTrue(np.shape(grid)[0] == np.shape(grid)[1])

        # The dimensions are correct
        self.assertTrue(np.shape(grid)[0] == basic.model.football_poisson.MAX_GOALS)


class TestCSMarkets(unittest.TestCase):

    def testEqualExpectancy(self):
        grid = football_poisson.correct_score_grid(2, 2)
        markets = football_poisson._calc_mw(grid)
        print(markets)
        self.assertEqual(round(markets['home'], 5), round(markets['away'],5)) # With equal expected goals the markets should be equal
        self.assertTrue(markets['draw'] > 0) # There should some probability of a draw

    def testHomeDominance(self):
        grid = football_poisson._correct_score_grid(5, 2)
        markets = football_poisson._calc_mw(grid)
        print(markets)
        self.assertTrue(round(markets['home'], 5) > round(markets['away'],5)) # Home should be higher
        self.assertTrue(markets['draw'] > 0) # There should some probability of a draw

    def testAwayDominance(self):
        grid = football_poisson._correct_score_grid(2, 5)
        markets = football_poisson._calc_mw(grid)
        print(markets)
        self.assertTrue(round(markets['home'], 5) < round(markets['away'], 5)) # Home should be higher
        self.assertTrue(markets['draw'] > 0) # There should some probability of a draw
