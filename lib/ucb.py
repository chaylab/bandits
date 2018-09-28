import numpy as np
import math

class UCB:
    def __init__(self, n, alpha):
        self.arms = []
        self.n = n
        for i in range(n):
            self.arms.append([0,1])
        self.alpha = alpha
        self.T = 0
        
    def observe(self, x):
        self.arms[self.pevArm][0] += x
        self.arms[self.pevArm][1] += 1

    def pick(self):
        tmp = []
        for i,arm in enumerate(self.arms):
            x = arm[0]/arm[1]+np.sqrt(self.alpha*math.log(max(1,self.T))/(2*max(1,arm[1])))
            tmp.append((x, i))
        self.T += 1
        self.pevArm = max(tmp)[1]
        return self.pevArm

class CUCB:
    def __init__(self, c, n, alpha):
        self.ucbs = [UBC(n, alpha) for i in range(c)]
        self.T = 0

    def observe(self, context, x):
        self.ucbs[self.pev_context].observe(x)

    def pick(self, context):
        self.T += 1
        self.pev_context = context
        return self.ucbs[context].pick()