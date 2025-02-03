import math
import datetime
import time
import numpy as np


# Default args taken from R Package
MU = 2200.0 # Start rating
SIGMA = 300.0 # Starting Variance
GAMMA = 0.0 # Player one advantange parameter
CVAL = 10.0 # Controls the increase in player deviations across time.
HVAL = 10.0 # Also controls the increase in player deviations across time
# Note that both cval and hval increase player deviations, so if hval is 
# not zero then cval should typically be lower than the corresponding parameter in glicko (Dynamic).
BVAL = 0.0 # Bonus - Bonus to high frequency players
LAMBDA = 2.0 # Starting neighborhood - Shrinks player ratings towards their opponents.
HISTORY = False # Returns history - unneeded
SORT = True # Sort table by rating - unneeded
RDMAX = 350.0 # Max variance

# RP is not in R, however this model of stephenson is not on a week by week basis
RATING_PERIOD = 30.0 # 90.0  # Days # http://www.glicko.net/research/volleyball-FINAL.pdf
Q = math.log(10) / 400

class Stephenson(object):
    def __init__(self, mu=MU, sigma=SIGMA, last_match=None, rp=RATING_PERIOD, gamma=GAMMA, cval=CVAL, hval=HVAL, bval=BVAL, lamb=LAMBDA, history=HISTORY, sort=SORT, rdmax=RDMAX):
        self.mu = mu
        self.sigma = sigma ** 2 # When referencing sqrt
        self.last_match = last_match
        self.rp = rp
        self.gamma = gamma
        self.cval = cval ** 2 # When referencing sqrt
        self.hval = hval ** 2 # When referencing sqrt
        self.bval = bval / 100 # When referencing times by factor
        self.lamb = lamb / 100 # When referencing times by factor
        self.history = history
        self.sort = sort
        self.rdmax = rdmax ** 2

    def printVals(self):
        print(f"Rating: {self.mu} Deviation: {math.sqrt(self.sigma)}")

    def getVar(self):
        return math.sqrt(self.sigma)
    
    def getRating(self):
        return self.mu

    def getTimeFactor(self, current_date=None):
        if self.last_match is not None and current_date is not None:
            time_difference = (current_date - self.last_match).days  # Time passed
            time_factor = (time_difference / self.rp) # Scale to ratio of rating periods passed
        else:
            return None

        return time_factor

    def updateVar(self, current_date=None):
        t = self.getTimeFactor(current_date)
        self.last_match = current_date if current_date is not None else self.last_match
        self.sigma = min(self.sigma + (self.cval * t), self.rdmax) if t is not None else self.sigma

    def getKVal(self, opponent_rating):
        k = (1 / math.sqrt(1 + (3 * Q**2 * opponent_rating.sigma) / np.pi**2))
        return k

    # pone - Player one advantage for chess only (or other games with advantage) Set to 1 for White -1 for Black 0 for unknown
    # If game has no starting advantages ignore (0)
    def getEVal(self, opponent_rating, k, pone):
        e = 1 / (1 + 10 ** (-(k * (self.mu - opponent_rating.mu + self.gamma*pone) / 400)))
        return e

    # Since this is a game by game version we will not use summation
    def getDVal(self, k, e):
        d = (Q ** 2) * (k ** 2) * e * (1 - e)
        return d

    # M is one as their is only one player in each iteration
    def newVarRating(self, opponent_rating, score, pone):
        k = self.getKVal(opponent_rating)
        e = self.getEVal(opponent_rating, k, pone)
        d = self.getDVal(k, e)

        sigma = (1 / (self.sigma + self.hval) + d) ** (-1)
        mu = self.mu + Q * sigma * k * (score - e + self.bval) + self.lamb * (opponent_rating.mu - self.mu)
        self.sigma = min(sigma, self.rdmax)
        self.mu = mu
        # print(f"New Sigma : {math.sqrt(self.sigma)} New Mu: {self.mu}")

    def expectedScore(self, opponent_rating):
        k = (1 / math.sqrt(1 + (3 * Q**2 * (self.sigma + opponent_rating.sigma)) / np.pi**2))
        e = 1 / (1 + 10 ** (-(k * (self.mu - opponent_rating.mu + self.gamma) / 400)))
        return e