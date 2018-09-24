import numpy as np

class Context:
    def __init__(self, n, prop):
        self.n = n
        self.dists = []
        for i in range(n):
            self.dists.append({m:0, sd:0})
        for i in range(n):
            self.dists[i].m = prop[i][0]
            self.dists[i].sd = prop[i][1]

    def sample(self, n):
        result = []
        for dist in dists:
            result.append(np.random.normal(dist.m, dist.sd, n))
        return result
