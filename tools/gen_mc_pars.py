import random
import numpy as np
from os import walk
bounds = [(10, 100), (0.5, 0.5), (5/3, 5/3),
          (2.7778e-08, 1.6667e-5), (1e-8, 1e-2),
          (-0.005, 0)]


# folder path
dir_path = 'pareto_pars'
# list to store files name
res = []
for (dir_path, dir_names, file_names) in walk(dir_path):
    res.extend(file_names)


def genpars(n=100):
    X = []
    Y = []
    b = []
    K = []
    S = []
    r = []
    for i in range(n):
        X.append(random.uniform(bounds[0][0],bounds[0][1]))
        Y.append(0.5)
        b.append(5/3)
        K.append(random.uniform(bounds[3][0],bounds[3][1]))
        S.append(random.uniform(bounds[4][0],bounds[4][1]))
        r.append(random.uniform(bounds[5][0],bounds[5][1]))

    return(np.array([X,Y,b,K,S,r]))

for idir  in res: 
    path = 'mc_pars/{}'.format(idir)
    np.savetxt(path,np.transpose(genpars()),fmt='%.5e')






