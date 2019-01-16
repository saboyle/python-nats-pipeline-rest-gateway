import unittest
import uuid

import schematics

from basic.schema.football import FootballRequest


class TestValidRequests(unittest.TestCase):

    def test_lower_boundary(self):
        """ Tests that validation of (valid) request works for lower boundary (>= 0)"""
        req = FootballRequest({'game_id': str(uuid.uuid4()), 'home_expected': 0, 'away_expected': 0})
        self.assertEqual(req.validate(), None)

    def test_mid(self):
        """ Tests that validation of (valid) request works for mid partition"""
        req = FootballRequest({'game_id': str(uuid.uuid4()), 'home_expected': 7.1, 'away_expected': 8.1})
        self.assertEqual(req.validate(), None)

    def test_higher_boundary(self):
        """ Tests that validation of (valid) request works for upper boundary (<= 0)"""
        req = FootballRequest({'game_id': str(uuid.uuid4()), 'home_expected': 15, 'away_expected': 15})
        self.assertEqual(req.validate(), None)



class TestInValidRequests(unittest.TestCase):

    def test_missing_data1(self):
        """ Tests that missing data results in a DataError"""

        with self.assertRaises(schematics.exceptions.DataError):
            req = FootballRequest({'home_expected': 0, 'away_expected': 0})
            req.validate()

    def test_missing_data2(self):
        """ Tests that missing data results in a DataError"""

        with self.assertRaises(schematics.exceptions.DataError):
            req = FootballRequest({'game_id': str(uuid.uuid4()), 'away_expected': 0})
            req.validate()

    def test_missing_data3(self):
        """ Tests that missing data results in a DataError"""

        with self.assertRaises(schematics.exceptions.DataError):
            req = FootballRequest({'game_id': str(uuid.uuid4()), 'home_expected': 0})
            req.validate()

    def test_incorrect_type1(self):
        """ Tests that incorrect data type results in a DataError"""

        with self.assertRaises(schematics.exceptions.DataError):
            req = FootballRequest({'game_id': str(uuid.uuid4()), 'home_expected': 0, 'away_expected': 'a'})
            req.validate()

    def test_incorrect_type2(self):
        """ Tests thatincorrect data type results in a DataError"""

        with self.assertRaises(schematics.exceptions.DataError):
            req = FootballRequest({'game_id': str(uuid.uuid4()), 'home_expected': 'a', 'away_expected': 0})
            req.validate()

    def test_incorrect_type3(self):
        """ Tests thatincorrect data type results in a DataError"""

        with self.assertRaises(schematics.exceptions.DataError):
            req = FootballRequest({'game_id': 2.6, 'home_expected': 0, 'away_expected': 0})
            req.validate()