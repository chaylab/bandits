from lib.context import Context
from lib.ucb import UCB, CUCB, DUCB
import math
import random

import numpy as np

def create_contexts(c):
    contexts = []
    cut = random.randint(1,c-1)
    # print('cut:', cut)
    for i in range(c):
        if i<cut: contexts.append(Context(2,[1,0]))
        else: contexts.append(Context(2,[0,1]))
    return contexts

def strg1(contexts, learner, T):
    C = len(contexts)
    for t in range(T):
        c = t % C
        it = learner.pick(c)
        rewards = contexts[c].tSample(1)
        learner.observe(rewards[0][it])
    return learner.getSum()

def testD(contexts, T):
    C = len(contexts)
    ducb = DUCB(C, 2, 3, int(T/(math.log(C,2)/2)))
    return strg1(contexts, ducb, T)

def testC(contexts, T):
    cucb = CUCB(len(contexts), 2, 3)
    return strg1(contexts, cucb, T)
    
if __name__=='__main__':
    T = 3000
    cs = range(10,1000,50)
    with open('ducb{}.in'.format(T),'w') as f1:
        with open('cucb{}.in'.format(T),'w') as f2:
            print(T, len(cs), file=f1)
            print(T, len(cs), file=f2)
            for i in cs:
                s1,s2 = 0,0
                n = 10
                for j in range(n):
                    contexts = create_contexts(i)
                    s1 += testD(contexts, T)
                    s2 += testC(contexts, T)
                s1/=n
                s2/=n
                print(i, T-s1, file=f1)
                print(i, T-s2, file=f2)
                    # print(s1,s2)