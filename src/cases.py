import random
from itertools import combinations
from .config import SEED

def numbers(n,run,seed=SEED):
    rng=random.Random(seed+n*101+run*1000003)
    return tuple(rng.randrange(-n,10*n) for _ in range(n))

def activities(n,run,seed=SEED):
    rng=random.Random(seed+n*103+run*1000003)
    return [(s:=rng.randrange(-n,10*n),s+rng.randrange(1,101),i) for i in range(n)]

def feasible(result):
    return len({a[2] for a in result})==len(result) and all(a[1]<=b[0] for a,b in zip(result,result[1:]))

def optimum(items):
    return max((len(c) for k in range(len(items)+1) for c in combinations(items,k) if feasible(sorted(c,key=lambda a:a[1]))),default=0)
