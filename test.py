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
    ducb = DUCB(len(contexts), 2, 3, 3)
    return strg1(contexts, ducb, T)

def testC(contexts, T):
    cucb = CUCB(len(contexts), 2, 3)
    return strg1(contexts, cucb, T)

def avg(contexts, func, T, n):
    mis = 0
    C = len(contexts)
    for i in range(n):
        mis += T-func(contexts, T)
    return mis/n

if __name__=='__main__':
    T = 3000
    cs = range(10,1000,10)
    with open('ducb{}.in'.format(T),'w') as f1:
        with open('cucb{}.in'.format(T),'w') as f2:
            print(T, len(cs), file=f1)
            print(T, len(cs), file=f2)
            for i in cs:
                contexts = create_contexts(i)
                s1 = avg(contexts, testD, T, 20)
                s2 = avg(contexts, testC, T, 20)
                print(i, s1, file=f1)
                print(i, s2, file=f2)
                # print(s1,s2)