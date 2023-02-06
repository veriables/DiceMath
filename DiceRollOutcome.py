import random
import numpy as np
from CustomEncoder import CustomEncoder
import json

class DiceRollOutcome:
    def __init__(self):
        self.d1_result = 0
        self.d2_result = 0
        self.winner = 0
        self.bothThree = False
        self.eitherThree = False
        self.xorThree = False
        self.neitherThree = False
        self.d1_was_three = False
        self.d2_was_three = False

    def __str__(self):
        output = json.dumps(self, indent=4, cls=CustomEncoder)
        return output

    def setDice(self, d1_value, d2_value):
        self.d1_result = d1_value
        self.d2_result = d2_value
        self.whoWon()
        self.setThrees()

    def rollDice(self):
        self.d1_result = np.random.randint(1,7)
        self.d2_result = np.random.randint(1,7)
        #self.d1_result = random.randint(1,6)
        #self.d2_result = random.randint(1,6)
        self.whoWon()
        self.setThrees()

    def whoWon(self):
        if self.d1_result > self.d2_result:
            self.winner = 1
        elif self.d1_result < self.d2_result:
            self.winner = 2

    def setThrees(self):
        self.setBothThrees()
        self.setEitherThree()
        self.setXorThree()
        self.setNeitherThree()
        self.setD1WasThree()
        self.setD2WasThree()

    def setD1WasThree(self):
        if self.d1_result == 3:
            self.d1_was_three = True
    
    def setD2WasThree(self):
        if self.d2_result == 3:
            self.d2_was_three = True
    
    def setBothThrees(self):
        if self.d1_result == 3:
            if self.d2_result == 3:
                self.bothThree = True
    
    def setEitherThree(self):
        if self.d1_result == 3:
            self.eitherThree = True
        if self.d2_result == 3:
            self.eitherThree = True

    def setXorThree(self):
        if self.d1_result == 3:
            if not self.d2_result == 3:
                self.xorThree = True
        if self.d2_result == 3:
            if not self.d1_result == 3:
                self.xorThree = True

    def setNeitherThree(self):
        if not self.d1_result == 3:
            if not self.d2_result == 3:
                self.neitherThree = True
        if not self.d2_result == 3:
            if not self.d1_result == 3:
                self.neitherThree = True
        
            