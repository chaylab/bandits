import numpy as np

class Context:
    def __init__(self, n, arms_mean):
        self.n = n
        self.dists = [[i, 1] for i in arms_mean]
        # 0 mean
        # 1 sd

    def _bound(self, x):
        # [0, 1]
        return max(min(x,1),0)

    def sample(self, n):
        result = [[] for i in range(n)]
        for dist in self.dists:
            X = np.random.normal(dist[0], dist[1], n)
            tmp = [self._bound(x) for x in X]
            for i in range(n):
                result[i].append(tmp[i])
        return result
