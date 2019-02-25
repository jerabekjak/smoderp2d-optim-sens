import statistics as stat


def nash_sutcliffe(obs, mod):

    mean_obs = stat.mean(obs)
    r = obs - mod
    r = r**2.0
    m = [iob - mean_obs for iob in obs]
    m[:] = [im**2.0 for im in m]
    return 1-sum(r)/sum(m)


def sum_of_squares(obs, mod):

    r = obs - mod
    r = r**2.0

    return sum(r)
