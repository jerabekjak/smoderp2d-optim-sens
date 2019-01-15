import matplotlib.pyplot as plt
import numpy as np
import os


def plot_philip(fnc, ks, s, out_dir, obs_data):

    path = '{0}{sep}{1}{sep}{2}{sep}{3}'.format(os.path.dirname(
        os.path.realpath(__file__)), '..', out_dir, 'philip_fit.png', sep=os.sep)

    t = np.linspace(min(obs_data.time), max(obs_data.time), 100)
    plt.plot(obs_data.time, obs_data.infilt, 'ro', label='observed data')
    lab = 'fitted data: Ks={:.5E}, S={:.2E}'.format(ks, s)
    plt.plot(t, fnc(ks, s, t), label=lab)
    plt.xlabel('time [sec]')
    plt.ylabel('infiltration [L/t]')
    plt.title("Fitted Philip's infiltration")
    plt.legend()
    plt.savefig(path)
