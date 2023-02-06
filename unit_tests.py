import unittest
from DiceRollOutcome import DiceRollOutcome
from DiceRoll import DiceRoll

class TestBetterRandom(unittest.TestCase):

    def test_dice_roll_outcome_init(self):
        dro = DiceRollOutcome()
        actual = dro.d1_result
        expected = 0
        self.assertEqual(actual, expected, "DiceRollOutcome was not successfully created")

    def test_dice_roll_outcome_roll_dice(self):
        dro = DiceRollOutcome()
        dro.rollDice()
        actual = dro.d1_result
        expected = 0
        self.assertGreater(actual, expected, "The result of rolling dice 1 was not greater than zero")

    def test_dice_roll_init(self):
        dr = DiceRoll()
        actual = dr.total_rolls
        expected = 0
        self.assertEqual(actual, expected, "DiceRollOutcome was not successfully created")

    def test_dice_roll_reset(self):
        dr = DiceRoll()
        dr.rollDice(1000)
        dr.reset()
        actual = dr.total_rolls
        expected = 0
        self.assertEqual(actual, expected, "DiceRoll was reset (cleared out), but total_rolls still had a value higher than zero")

    def test_dice_roll_roll_dice(self):
        dr = DiceRoll()
        dr.rollDice(100)
        actual = dr.total_rolls
        expected = 100
        self.assertEqual(actual, expected, "DiceRoll rolled 100 times, but did not record 100 total rolls")

    def test_dice_roll_roll_dice_object_count(self):
        dr = DiceRoll()
        dr.rollDice(100)
        actual = len(dr.outcomes)
        expected = 100
        self.assertEqual(actual, expected, "DiceRoll rolled 100 times, but did not get 100 DiceRollOutcome objects")

    def test_dice_roll_win_and_tie_counts(self):
        dr = DiceRoll()
        dr.rollDice(100)
        actual = dr.d1_wins + dr.d2_wins + dr.ties
        expected = dr.total_rolls
        self.assertEqual(actual, expected, "d1_wins + d2_wins + ties does not equal total dice rolls")

    def test_dice_roll_win_and_tie_percents(self):
        dr = DiceRoll()
        dr.rollDice(100)
        actual = dr.percent_d1_wins + dr.percent_d2_wins + dr.percent_ties
        expected = 1
        self.assertEqual(actual, expected, "percent_d1_wins + percent_d2_wins + percent_ties does not equal 100 percent")
    
    def test_get_counts_of_each_outcome(self):
        dr = DiceRoll()
        num_rolls = 100
        num_dice = 2
        dr.rollDice(num_rolls)
        outcomes = dr.getCountsOfEachOutcome()
        actual = sum(outcomes.values())
        expected = num_rolls * num_dice
        self.assertEqual(actual, expected, "sum of count of each result does not match number of rolls")

    def test_get_counts_for_wins(self):
        dr = DiceRoll()
        num_rolls = 100
        num_dice = 2
        dr.rollDice(num_rolls)
        outcomes = dr.getCountsForWins()
        actual = sum(outcomes.values())
        expected = 100
        self.assertEqual(actual, expected, "Sum of wins and ties does not equal the number of rolls")

    def test_get_both_three_vs_total(self):
        dr = DiceRoll()
        num_rolls = 100
        num_dice = 2
        dr.rollDice(num_rolls)
        outcomes = dr.getBothThreeVsTotal()
        actual = outcomes['Both 3']
        expected = outcomes['Total']
        self.assertGreaterEqual(expected, actual, "There were more outcomes where both dice rolled three than total rolls")

    def test_get_either_three_vs_total(self):
        dr = DiceRoll()
        num_rolls = 100
        num_dice = 2
        dr.rollDice(num_rolls)
        outcomes = dr.getEitherThreeVsTotal()
        actual = outcomes['Either 3']
        expected = outcomes['Total']
        self.assertGreaterEqual(expected, actual, "There were more outcomes where either dice rolled three than total rolls")

    def test_setDice(self):
        dro = DiceRollOutcome()
        dro.setDice(6, 5)
        actual = True
        if not dro.d1_result == 6:
            actual = False
        if not dro.d2_result == 5:
            actual = False
        expected = True
        self.assertEqual(actual, expected, "One of the dice had a value different from what was set")

    def test_either_three_true(self):
        dro = DiceRollOutcome()
        dro.setDice(1, 3)
        actual = dro.eitherThree
        expected = True
        self.assertEqual(actual, expected, "One of the dice had a value of 3 yet the eitherThree property was False")

    def test_either_three_false(self):
        dro = DiceRollOutcome()
        dro.setDice(1, 4)
        actual = dro.eitherThree
        expected = False
        self.assertEqual(actual, expected, "Neither of the dice had a value of 3 yet the eitherThree property was True")

    def test_both_three_true(self):
        dro = DiceRollOutcome()
        dro.setDice(3, 3)
        actual = dro.bothThree
        expected = True
        self.assertEqual(actual, expected, "Both of the dice had a value of 3 yet the bothThree property was False")

    def test_both_three_false(self):
        dro = DiceRollOutcome()
        dro.setDice(3, 4)
        actual = dro.bothThree
        expected = False
        self.assertEqual(actual, expected, "One of the dice did not have a value of 3 yet the bothThree property was True")

    def test_both_three_false_again(self):
        dro = DiceRollOutcome()
        dro.setDice(2, 4)
        actual = dro.bothThree
        expected = False
        self.assertEqual(actual, expected, "Neither of the dice had a value of 3 yet the bothThree property was True")

    def test_either_vs_both_three(self):
        dr = DiceRoll()
        num_rolls = 100
        num_dice = 2
        dr.rollDice(num_rolls)
        both_outcomes = dr.getBothThreeVsTotal()
        either_outcomes = dr.getEitherThreeVsTotal()
        both_three_count = sum(both_outcomes.values())
        either_three_count = sum(either_outcomes.values())
        self.assertGreaterEqual(either_three_count, both_three_count, "The number of rolls where either dice came up 3 should be greater than the number of rolls where both dice came up three")

    def test_xor_three_vs_both_three(self):
        dr = DiceRoll()
        num_rolls = 1000
        dr.rollDice(num_rolls)
        actual = True
        for dro in dr.outcomes:
            if dro.bothThree and dro.xorThree:
                actual = False
        expected = True
        self.assertEqual(actual, expected, "Found a record where both the both3 and xor3 properties were marked True")

    def test_sum_vs_either_3(self):
        dr = DiceRoll()
        num_rolls = 1000
        dr.rollDice(num_rolls)
        dr_either_3 = dr.either_3
        dro_either_3_sum = 0
        for dro in dr.outcomes:
            if dro.eitherThree:
                dro_either_3_sum += 1
        actual = (dr_either_3 == dro_either_3_sum)
        expected = True
        self.assertEqual(actual, expected, "Summing the DiceRollOutcomes where either_3 is True leads to a different sum than that recorded in the DiceRoll either_3 property")

    def test_sum_vs_neither_3(self):
        dr = DiceRoll()
        num_rolls = 1000
        dr.rollDice(num_rolls)
        dr_neither_3 = dr.neither_3
        dro_neither_3_sum = 0
        for dro in dr.outcomes:
            if dro.neitherThree:
                dro_neither_3_sum += 1
        actual = (dr_neither_3 == dro_neither_3_sum)
        expected = True
        self.assertEqual(actual, expected, "Summing the DiceRollOutcomes where neither_3 is True leads to a different sum than that recorded in the DiceRoll neither_3 property")

    def test_percent_wins(self):
        dr = DiceRoll()
        num_rolls = 1000
        dr.rollDice(num_rolls)
        data = dr.getPercentForWins()
        percentages = []
        for k,v in data.items():
            percentages.append(v['percent'])
        actual = sum(percentages)
        expected = 1
        self.assertEqual(actual, expected, "The sum of the percentages of d1 wins, d2 wins, and ties does not equal 1")

    def test_percent_ties(self):
        dr = DiceRoll()
        num_rolls = 1000
        dr.rollDice(num_rolls)
        percentages = dr.getPercentForTie()
        actual = sum(percentages.values())
        expected = 1
        self.assertEqual(actual, expected, "The sum of the percentages of ties and not ties does not equal 1")

    def test_percent_both_3(self):
        dr = DiceRoll()
        num_rolls = 1000
        dr.rollDice(num_rolls)
        percentages = dr.getPercentBothThree()
        actual = sum(percentages.values())
        expected = 1
        self.assertEqual(actual, expected, "The sum of the percentages of Both_3 and Not_Both_3 does not equal 1")

    def test_percent_either_3(self):
        dr = DiceRoll()
        num_rolls = 1000
        dr.rollDice(num_rolls)
        percentages = dr.getPercentEitherThree()
        actual = sum(percentages.values())
        expected = 1
        self.assertEqual(actual, expected, "The sum of the percentages of Either_3 and Not_Either_3 does not equal 1")

    def test_percent_xor_3(self):
        dr = DiceRoll()
        num_rolls = 1000
        dr.rollDice(num_rolls)
        percentages = dr.getPercentXorThree()
        actual = sum(percentages.values())
        expected = 1
        self.assertEqual(actual, expected, "The sum of the percentages of Xor_3 and Not_Xor_3 does not equal 1")

    def test_percent_neither_3(self):
        dr = DiceRoll()
        num_rolls = 1000
        dr.rollDice(num_rolls)
        percentages = dr.getPercentNeitherThree()
        actual = sum(percentages.values())
        expected = 1
        self.assertEqual(actual, expected, "The sum of the percentages of Neither_3 and Not_Neither_3 does not equal 1")

unittest.main()
