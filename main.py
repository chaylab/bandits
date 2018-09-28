from lib.context import Context
from lib.ucb import UCB, CUCB, DUCB
import math

def deltaDiff(n, mean):
    ret = []
    for i in range(n):
        for j in range(i+1,n):
            tmp = abs(mean[i]-mean[j])
            if tmp > 0: ret.append(tmp)
    return ret

def theoryRegret(d, T, a):
    return sum([2*a/i for i in d])*math.log(T)+a/(a-2)*sum(d)

def getMaxReward(X, T):
    tmp = [0]*len(X[0])
    for i in range(T):
        for j in range(len(X[i])):
            tmp[j] += X[i][j]
    return sum(tmp)

def strg1(X, C, learner, N, T):
    for t in range(T):
        c = t mod C
        it = learner.pick(c)
        learner.observe(X[c][t][it])

    tmp = sum([getMaxReward(X[i], T) for i in range(C)])
    return learner.getSum()


if __name__=='__main__':
    context_n = 10
    arm_n = 2
    ucb_alpha = 3 #alpha > 2
    T = 1000
    arms_mean = [
        [0.6, 0.3],
        [0.3, 0.6]
    ]

    contexts = []
    for i in range(context_n):
        if i<int(context_n/2):
            contexts.append(Context(arm_n,arms_mean[0]))
        else:
            contexts.append(Context(arm_n,arms_mean[1]))

    X = [contexts[i].sample(T) for i in context_n]
    cucb = CUCB(context_n, arm_n, ucb_alpha)
    ducb = DUCB(context_n, arm_n, ucb_alpha, 10)
    # print(X)
    # ucb = UCB(arm_n, ucb_alpha)
    # sum_rwd = [0] * arm_n
    # rwd = 0
    # for t in range(T):
    #     it = ucb.pick()
    #     for i in range(arm_n):
    #         sum_rwd[i] += X[t][i]
    #     ucb.observe(X[t][it])
    #     rwd += X[t][it]
    # r = max(sum_rwd) - rwd

    # d = deltaDiff(arm_n, arms_mean[0])
    # theory = theoryRegret(d, T, ucb_alpha)

    # print('reget: {}, max arm reward: {}, player reward: {}, theory reget: {}'.format(r, max(sum_rwd), rwd, theory))

