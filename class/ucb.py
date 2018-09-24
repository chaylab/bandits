import numpy as np
import math

class UCB:
    def __init__(self, n, alpha):
        self.arms = []
        self.n = n
        for i in range(n):
            self.arms.append({r: 0, n: 0})
        self.alpha = alpha
        self.T = 0
        
    def addR(self, x):
        self.arms[x].r += x
        self.arms[x].n += 1

    def getArm(self):
        tmp = []
        for i,arm in enumerate(self.arms):
            x = arm.r/arm.n+self.alpha*math.log(self.T)/arm.n/(self.T-1)
            tmp.append((x, i))
        self.T += 1
        return max(tmp)[1]