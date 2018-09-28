import numpy as np
import math

class UCB:
    def __init__(self, n, alpha):
        self.arms = []
        self.N = n
        for i in range(n):
            self.arms.append([0,1])
        self.alpha = alpha
        self.T = 0
        self.reward_sum = 0
        
    def observe(self, x):
        self.arms[self.pevArm][0] += x
        self.arms[self.pevArm][1] += 1
        self.reward_sum += x

    def pick(self):
        tmp = []
        for i,arm in enumerate(self.arms):
            x = arm[0]/arm[1]+np.sqrt(self.alpha*math.log(max(1,self.T))/(2*max(1,arm[1])))
            tmp.append((x, i))
        self.T += 1
        self.pevArm = max(tmp)[1]
        return self.pevArm

    def getSum(self):
        return self.reward_sum

class CUCB:
    def __init__(self, c, n, alpha):
        self.ucbs = [UBC(n, alpha) for i in range(c)]
        self.C = c
        self.T = 0
        self.reward_sum = 0

    def observe(self, x):
        self.ucbs[self.pev_context].observe(x)
        self.reward_sum += x

    def pick(self, context):
        self.T += 1
        self.pev_context = context
        return self.ucbs[context].pick()
    
    def getSum(self):
        return self.reward_sum

class DUCB:
    def __init__(self, c, n ,alpha ,d):
        self.ucbs = [UBC(n, alpha) for i in range(c*2-1)]
        self.C = c
        self.T = 0
        self.delta = d
        self.reward_sum = 0

    def _get_path(n):
        path = [0]
        l = 0, h = self.C
        while l<=h:
            m = (l+h)/2
            if n<m:
                h = m-1
                path.append(path[-1]*2+1)
            elif n>m: 
                l = m+1
                path.append(path[-1]*2+2)
            else:
                break
        return path

    def observe(self, x):
        path = self._get_path(self.pev_context)
        for i in path:
            self.ucbs[i].observe(x)
        self.reward_sum += x

    def pick(self, context):
        path = self._get_path(context)
        context = 0
        for i in path: if self.ucbs[i].T >= self.delta: context = i
        self.pev_context = context
        self.T += 1
        return self.ucbs[context].pick()

    def getSum(self):
        return self.reward_sum