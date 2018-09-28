from lib.context import Context
from lib.ucb import UCB
import math

def delta_diff(n, mean):
    ret = []
    for i in range(n):
        for j in range(i+1,n):
            tmp = abs(mean[i]-mean[j])
            if tmp > 0: ret.append(tmp)
    return ret

def get_theory_regret(d, T, a):
    return sum([2*a/i for i in d])*math.log(T)+a/(a-2)*sum(d)

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

    X = contexts[0].sample(T)
    # print(X)
    ucb = UCB(arm_n, ucb_alpha)
    sum_rwd = [0] * arm_n
    rwd = 0
    for t in range(T):
        it = ucb.pick()
        for i in range(arm_n):
            sum_rwd[i] += X[t][i]
        ucb.observe(X[t][it])
        rwd += X[t][it]
    r = max(sum_rwd) - rwd

    d = delta_diff(arm_n, arms_mean[0])
    theory = get_theory_regret(d, T, ucb_alpha)

    print('reget: {}, max arm reward: {}, player reward: {}, theory reget: {}'.format(r, max(sum_rwd), rwd, theory))

