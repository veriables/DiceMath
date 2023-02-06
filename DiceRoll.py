from CustomEncoder import CustomEncoder
from DiceRollOutcome import DiceRollOutcome
import json

class DiceRoll:
    def __init__(self):
        # Outcomes from Dice Rolls
        self.outcomes = []
        # Counts
        self.total_rolls = 0
        self.d1_wins = 0
        self.d2_wins = 0
        self.ties = 0
        self.both_3 = 0
        self.either_3 = 0
        self.xor_3 = 0
        self.neither_3 = 0

        # Percentages
        self.percent_d1_wins = 0
        self.percent_d2_wins = 0
        self.percent_ties = 0
        self.percent_both_3 = 0
        self.percent_either_3 = 0
        self.percent_xor_3 = 0
        self.percent_neither_3 = 0

    def __str__(self):
        output = json.dumps(self, indent=4, cls=CustomEncoder)
        return output

    def rollDice(self, num_rolls):
        self.reset()
        for i in range(num_rolls):
            outcome = DiceRollOutcome()
            outcome.rollDice()
            self.outcomes.append(outcome)
        self.setCounts()
        self.setPercentages()

    def reset(self):
        self.outcomes = []
        self.total_rolls = 0
        self.d1_wins = 0
        self.d2_wins = 0
        self.ties = 0
        self.both_3 = 0
        self.either_3 = 0
        self.xor_3 = 0
        self.neither_3 = 0
        self.d1_was_3 = 0
        self.d2_was_3 = 0
        self.percent_d1_wins = 0
        self.percent_d2_wins = 0
        self.percent_ties = 0
        self.percent_both_3 = 0
        self.percent_either_3 = 0
        self.percent_d1_was_3 = 0
        self.percent_d2_was_3 = 0
        

    def setCounts(self):
        for dro in self.outcomes:
            self.total_rolls += 1
            if dro.winner == 1:
                self.d1_wins += 1
            if dro.winner == 2:
                self.d2_wins += 1
            if dro.winner == 0:
                self.ties += 1
            if dro.bothThree:
                self.both_3 += 1
            if dro.eitherThree:
                self.either_3 += 1
            if dro.xorThree:
                self.xor_3 += 1
            if dro.neitherThree:
                self.neither_3 += 1
            if dro.d1_was_three:
                self.d1_was_3 += 1
            if dro.d2_was_three:
                self.d2_was_3 += 1
    
    def setPercentages(self):
        if self.total_rolls > 0:
            self.percent_d1_wins   = self.d1_wins / self.total_rolls
            self.percent_d2_wins   = self.d2_wins / self.total_rolls
            self.percent_ties      = self.ties / self.total_rolls
            self.percent_both_3    = self.both_3 / self.total_rolls
            self.percent_either_3  = self.either_3 / self.total_rolls
            self.percent_xor_3     = self.xor_3 / self.total_rolls
            self.percent_neither_3 = self.neither_3 / self.total_rolls
            self.percent_d1_was_3  = self.d1_was_3 / self.total_rolls
            self.percent_d2_was_3  = self.d2_was_3 / self.total_rolls
            
    def getCountsOfEachOutcome(self):
        outcome_counts = {1:0,2:0,3:0,4:0,5:0,6:0}
        for dro in self.outcomes:
            outcome_counts[dro.d1_result] += 1
            outcome_counts[dro.d2_result] += 1
        return outcome_counts

    def getCountsOfEachOutcomeText(self):
        data = self.getCountsOfEachOutcome()
        counts = data.values()
        str_num_rolls = str(self.total_rolls)
        str_num_outcomes = str(self.total_rolls * 2)
        str_expected = str(round(((self.total_rolls * 2) / 6)))
        str_observed = str(round(sum(counts)/len(counts)))
        message = "<div style='text-align: center'>"
        message += "<b>Notes</b><br>"
        message += "<p>Each outcome is equally likely.  Specifically, 1/6th of the total rolls should show each die face.</p>"
        message += "<p>Thus, we expect each outcome to occur the same number of times. Simply divide the number of rolls by the number of possible outcomes to see how many rolls should come up on any of the six sides.</p>"
        message += "<p>With " + str_num_rolls + " rolls of 2 dice (that's " + str_num_outcomes + " individual die outcomes) we should expect to see each outcome " + str_expected + " times.</p>"
        message += "<b style='color: red'>EXPECTED: " + str_expected + " </b><br>"
        message += "<b style='color: green'>OBSERVED: " + str_observed + " </b><br>"
        message += "</div>"
        return message

    def getCountsForWins(self):
        # 0 = Tie, 1 = Dice 1 won, 2 = Dice 2 won
        outcome_counts = {0:0,1:0,2:0}
        for dro in self.outcomes:
            outcome_counts[dro.winner] += 1
        return outcome_counts
    
    def getPercentForWins(self):
        counts = self.getCountsForWins()
        outcome_counts = {
            'D1 Wins': {'percent': round(self.percent_d1_wins, 1), 'count': counts[1]},
            'Tie': {'percent': round(self.percent_ties, 1), 'count': counts[0]},
            'D2 Wins':  {'percent': round((self.percent_d2_wins), 1), 'count': counts[2]}
        }
        return outcome_counts

    def getCountsForWinsText(self):
            data = self.getCountsForWins()
            num_ties = round((self.total_rolls * (1/6)), 2)
            str_num_rolls = str(self.total_rolls)
            str_num_ties = str(round((self.total_rolls) * (1/6)))
            str_rolls_minus_ties = str((self.total_rolls - num_ties))
            str_expected = str(round(((self.total_rolls - num_ties) / 2)))
            str_observed = str(round(((data[1] + data[2]) / 2)))
            message = "<div style='text-align: center'>"
            message += "<b>Notes</b><br>"
            message += "<p>Each die has an equal chance of winning. It's 50/50 odds. Either die 1 or die 2 "
            message += "wins, right? Well, almost. We need to subtract the tied outcomes.</p>"
            message += "<p>That leaves us with " + str_num_rolls + " - " + str_num_ties + " "
            message += " ties = " + str_rolls_minus_ties + ".</p>" 
            message += "<p>Now because each player has an equal chance of winning, we can simply split the "
            message += str_rolls_minus_ties + " in half to see the number of wins each player should have.</p>"
            message += "<p>" + str_rolls_minus_ties + " / 2 = " + str_expected + "</p>"
            message += "<b style='color: red'>EXPECTED: " + str_expected + " </b><br>"
            message += "<b style='color: green'>OBSERVED: " + str_observed
            message += "</div>"
            return message

    def getCountsForTie(self):
        outcome_counts = {
            'Draw': self.ties, 
            'Total': len(self.outcomes)
        }
        return outcome_counts

    def getPercentForTie(self):
        outcome_counts = {
            'Draw': round(self.percent_ties, 1), 
            'Not Draw':  round(((self.percent_d1_wins + self.percent_d2_wins)), 1)
        }
        return outcome_counts

    def getCountsForTieText(self):
        data = self.getCountsForTie()
        str_num_rolls = str(self.total_rolls)
        str_expected = str(round((self.total_rolls * (1/6)), 2))
        str_observed = str(round(data['Draw']))
        message  = "<div style='text-align: center'>"
        message += "<b>Notes</b><br>"
        message += "<p>There is a chance of a tie. For this to happen, both die need "
        message += "to roll the same number.  What are the odds of a tie? "
        message += "That's where we use the:</p>"
        message += "<p>Multiplication Rule for "
        message += "Probabilities<p>"
        message += "<p>We take the odds of die 1's outcome (die 1 has a 1/1 chance of landing on a number) "
        message += "and multiply it by the odd's of die 2's outcome being the same (which is a 1/6 chance).</p>"  
        message += "<p>So (1) * (1/6) = 1/6</p>"
        message += "<p>In " + str_num_rolls + " roles, we should "
        message += "see about " + str_num_rolls + " * (1/6) = " + str_expected + " ties.</p>"
        message += "<b style='color: red'>EXPECTED: " + str_expected + " </b><br>"
        message += "<b style='color: green'>OBSERVED: " + str_observed
        message += "</div>"
        return message

    def getBothThreeVsTotal(self):
        outcome_counts = {
            'Both 3': self.both_3, 
            'Total': len(self.outcomes)
        }
        return outcome_counts

    def getPercentBothThree(self):
        outcome_counts = {
            'Both 3': round(self.percent_both_3, 1), 
            'Not Both 3':  round(round(self.percent_xor_3, 3) + round(self.percent_neither_3, 3), 1)
        }
        return outcome_counts

    def getBothThreeVsTotalText(self):
            data = self.getBothThreeVsTotal()
            str_num_rolls = str(self.total_rolls)
            str_expected = str(round(((self.total_rolls) * (1/36)), 2))
            str_observed = str(data['Both 3'])
            message  = "<div style='text-align: center'>"
            message += "<b>Notes</b><br>"
            message += "<p>Each die has a 1/6 chance of coming up as a 3. To figure "
            message += "the chance of them both being 3, we use the</p>"
            message += "<p>Multiplication Rule for Probability:</p>"
            message += "<p>1/6 * 1/6 = 1/36</p>"
            message += "<p>That's a 1 in 6 chance of die 1 rolling a 3 "
            message += "and a 1 in 6 chance of die 2 landing on 3 (to match die 1).</p>"
            message += "<p>With " + str_num_rolls + " rolls, we'd expect "
            message += "to see " + str_num_rolls + " * (1/36) = " + str_expected + " "
            message += "of the outcomes being Double Threes.</p>"
            message += "<b style='color: red'>EXPECTED: " + str_expected + " </b><br>"
            message += "<b style='color: green'>OBSERVED: " + str_observed
            message += "</div>"
            return message

    def getEitherThreeVsTotal(self):
        outcome_counts = {
            'Either 3': self.either_3, 
            'Total': len(self.outcomes)
        }
        return outcome_counts

    def getPercentEitherThree(self):
        outcome_counts = {
            'Either 3': round(self.percent_either_3, 3), 
            'Not Either 3':  round(self.percent_neither_3, 3), 
        }
        return outcome_counts

    def getEitherThreeVsTotalText(self):
        data = self.getEitherThreeVsTotal()
        str_num_rolls = str(self.total_rolls)
        str_expected = str(round(self.total_rolls * (11/36)))
        str_observed = str(data['Either 3'])
        message  = "<div style='text-align: center'>"
        message += "<b>Notes</b><br>"
        message += "<p>The odds of either or both of the dice showing "
        message += "a 3 is the sum of three things:</p>"
        message += "<p>The odds of D1 == 3 and D2 != 3<br>"
        message += "(1/6) * (5/6) = (5/36)</p>"
        message += "<p>The odds of D1 != 3 and D2 == 3:<br>"
        message += "(5/6) * (1/6) = (5/36)</p>"
        message += "<p>The odds of D1 == 3 and D2 == 3:<br>"
        message += "(1/6) * (1/6) = (1/36)</p>"
        message += "<p>Sum them up with:<br>"
        message += "(5/36) + (5/36) + (1/36) = (11/36)</p>"
        message += "<p>With our " + str_num_rolls + " rolls, "
        message += "we should have " + str_num_rolls + " "
        message += "* (11/36) = " + str_expected + " "
        message += "cases of either die or both showing a 3.</p>"
        message += "<b style='color: red'>EXPECTED: " + str_expected + " </b><br>"
        message += "<b style='color: green'>OBSERVED: " + str_observed
        message += "</div>"
        return message

    def getXorThreeVsTotal(self):
        outcome_counts = {
            'XOR 3': self.xor_3, 
            'Total': len(self.outcomes)
        }
        return outcome_counts

    def getPercentXorThree(self):
        outcome_counts = {
            'Xor 3': round(self.percent_xor_3, 3), 
            'Not Xor 3':  round(self.percent_neither_3, 3) + round(self.percent_both_3, 3)
        }
        return outcome_counts

    def getXorThreeVsTotalText(self):
        data = self.getXorThreeVsTotal()
        str_num_rolls = str(self.total_rolls)
        str_expected = str(round(self.total_rolls * (5/18)))
        str_observed = str(data['XOR 3'])
        message  = "<div style='text-align: center'>"
        message += "<b>Notes</b><br>"
        message += "<p>The odds of either (but not both) of the dice showing "
        message += "a 3 is the sum of two things:</p>"
        message += "<p>The odds of D1 == 3 and D2 != 3<br>"
        message += "(1/6) * (5/6) = (5/36)</p>"
        message += "<p>The odds of D1 != 3 and D2 == 3:<br>"
        message += "(5/6) * (1/6) = (5/36)</p>"
        message += "<p>Sum them up with:<br>"
        message += "(5/36) + (5/36) = 10/36 = 5/18</p>"
        message += "<p>With our " + str_num_rolls + " rolls, "
        message += "we should have " + str_num_rolls + " "
        message += "* (5/18) = " + str_expected + " "
        message += "cases of either die (but not both) showing a 3.</p>"
        message += "<b style='color: red'>EXPECTED: " + str_expected + " </b><br>"
        message += "<b style='color: green'>OBSERVED: " + str_observed
        message += "</div>"
        return message

    def getNeitherThreeVsTotal(self):
        outcome_counts = {
            'Neither 3': self.neither_3, 
            'Total': len(self.outcomes)
        }
        return outcome_counts
    
    def getNeitherThreeVsTotalText(self):
        data = self.getNeitherThreeVsTotal()
        str_num_rolls = str(self.total_rolls)
        str_expected = str(round(self.total_rolls * (25/36)))
        str_observed = str(data['Neither 3'])
        message  = "<div style='text-align: center'>"
        message += "<b>Notes</b><br>"
        message += "<p>The odds of neither of the dice showing "
        message += "a 3 is the product of two things:</p>"
        message += "<p>The odds of D1 != 3<br>"
        message += "(5/6)</p>"
        message += "<p>The odds of D2 != 3:<br>"
        message += "(5/6)</p>"
        message += "<p>Because they both have to happen, we multiply those odds:<br>"
        message += "(5/6) + (5/6) = 25/36</p>"
        message += "<p>With our " + str_num_rolls + " rolls, "
        message += "we should have " + str_num_rolls + " "
        message += "* (25/36) = " + str_expected + " "
        message += "cases of neither die is showing a 3.</p>"
        message += "<b style='color: red'>EXPECTED: " + str_expected + " </b><br>"
        message += "<b style='color: green'>OBSERVED: " + str_observed
        message += "</div>"
        return message

    def getPercentNeitherThree(self):
        outcome_counts = {
            'Neither 3': round(self.percent_neither_3, 3), 
            'Not Neither 3':  round(self.percent_either_3, 3), 
        }
        return outcome_counts

    

    
        

