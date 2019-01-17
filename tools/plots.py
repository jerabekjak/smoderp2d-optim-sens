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
    plt.plot
    plt.plot(obs.time/60, obs.val*1000*60*60, 'ro', label='observed data')
    plt.plot(mod.time/60, mod.val*1000*60*60, 'bo', label='modeled data')
    plt.title("final parameters: X={:1.2f}, Y={:1.2f}, b={:1.2f}, ks={:.2e}, s={:0.2e}\nsum of squares = {:.2E}".format(
        de_results.x[0], de_results.x[1], de_results.x[2], de_results.x[3], de_results.x[4], de_results.fun),fontsize=10, loc='left')
    plt.xlabel('time [mins]')
    plt.ylabel('runoff water [mm/hour]')
    plt.legend()
    plt.savefig(path)



def plot_sa(out_dir,p1,p2,ss):

    path = '{0}{sep}{1}{sep}{2}{sep}{3}'.format(os.path.dirname(
        os.path.realpath(__file__)), '..', out_dir, 'sa_surface.png', sep=os.sep)
    
    plt.figure(1)
    x=np.array(p1)
    y=np.array(p2)
    z=np.array(ss)

    x=np.unique(x)
    y=np.unique(y)
    X,Y = np.meshgrid(x,y)

    Z=z.reshape(len(y),len(x))

    plt.pcolormesh(X,Y,Z)

    plt.savefig(path)


