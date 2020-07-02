import statistics as stat
import numpy as np

def nash_sutcliffe(obs, mod):

    mean_obs = stat.mean(obs)
    r = np.array(obs) - np.array(mod)
    r = r**2.0
    m = [iob - mean_obs for iob in obs]
    m[:] = [im**2.0 for im in m]
    return 1-sum(r)/sum(m)


def sum_of_squares(obs, mod):
    
    r = np.array(obs) - np.array(mod)
    #r[0] = r[0]*50.
    #r[1] = r[1]*5.
    r = r**2.0

    return sum(r)
