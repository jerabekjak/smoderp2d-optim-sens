import matplotlib.pyplot as plt
import numpy as np
import os


def plot_philip(fnc, ks, s, out_dir, obs_data):

    path = '{0}{sep}{1}{sep}{2}{sep}{3}'.format(os.path.dirname(
        os.path.realpath(__file__)), '..', out_dir, 'philip_fit.png', sep=os.sep)

    plt.figure(0)
    t = np.linspace(min(obs_data.time), max(obs_data.time), 100)
    plt.plot(obs_data.time, obs_data.infilt, 'ro', label='observed data')
    lab = 'fitted data: Ks={:.2E}, S={:.2E}'.format(ks, s)
    plt.plot(t, fnc(ks, s, t), label=lab)
    plt.xlabel('time [sec]')
    plt.ylabel('infiltration [L/t]')
    plt.title("Fitted Philip's infiltration")
    plt.legend()
    plt.savefig(path)


def plot_de(obs, mod, de_results, out_dir):

    path = '{0}{sep}{1}{sep}{2}{sep}{3}'.format(os.path.dirname(
        os.path.realpath(__file__)), '..', out_dir, 'de_optim.png', sep=os.sep)
    plt.figure(1)
    plt.plot(obs.time, obs.val, 'ro', label='observed data')
    plt.plot(mod.time, mod.val, 'bo', label='modeled data')
    plt.suptitle("Result of de optimization")
    plt.title("final parameters: X={:.2E}, Y={:.2E}, b={:.2E}\nwith sum of squares = {:.2E}".format(
        de_results.x[0], de_results.x[1], de_results.x[2], de_results.fun),fontsize=9)
    plt.xlabel('time [sec]')
    plt.ylabel('runoff water level [L]')
    plt.legend()
    plt.savefig(path)
