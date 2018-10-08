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
    
    def observeFix(self, it, x):
        self.arms[it][0] += x
        self.arms[it][1] += 1
        self.reward_sum += x

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
        self.ucbs = [UCB(n, alpha) for i in range(c)]
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
        self.ucbs = [UCB(n, alpha) for i in range(2**int(math.ceil(math.log(c,2))+1))]
        self.CT = 2**int(math.ceil(math.log(c,2)))
        self.C = c
        self.T = 0
        self.delta = d
        self.reward_sum = 0

        self.path = [self._get_path(i) for i in range(c)]

    def _get_path(self, n):
        tmp = [0]*int(math.ceil(math.log(self.C,2)))
        for i,num in enumerate(tmp):
            tmp[i] = n%2
            n = int(n/2)
        path = []
        pev = 0
        for i in tmp[::-1]:
            path.append(pev*2+(1+i))
            pev = path[-1]
        return path

    def observe(self, x):
        path = self.path[self.pev_context]
        for i in path:
            self.ucbs[i].observeFix(self.pev_it, x)
        self.reward_sum += x

    def pick(self, context):
        path = self.path[context]
        # print(context, path)
        context = path[0]
        for i,num in enumerate(path): 
            if self.ucbs[num].T >= self.delta: 
                context = num
        self.pev_context = context
        self.pev_it = self.ucbs[context].pick()
        self.T += 1
        return self.pev_it

    def getSum(self):
        return self.reward_sum