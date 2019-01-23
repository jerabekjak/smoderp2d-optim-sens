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
    plt.figure(1, figsize=(9, 7))
    plt.plot(obs.time/60, obs.val*1000*60*60, 'ro', label='observed data')
    plt.plot(mod.time/60, mod.val*1000*60*60, 'bo', label='modeled data')
    plt.title("final parameters: X={:1.2f}, Y={:1.2f}, b={:1.2f}, ks={:.2e}, s={:0.2e}, ret={:0.2e}\nsum of squares = {:.2E}".format(
        de_results.x[0], de_results.x[1], de_results.x[2], de_results.x[3], de_results.x[4], de_results.x[5], de_results.fun*(1000*60*60)**2.0), fontsize=10, loc='left')
    plt.xlabel('time [mins]')
    plt.ylabel('runoff [mm/hour]')
    plt.legend()
    plt.savefig(path, dpi=200)


def plot_sa(out_dir, mu, sigma, cfgs):

    path = '{0}{sep}{1}{sep}{2}{sep}{3}'.format(os.path.dirname(
        os.path.realpath(__file__)), '..', out_dir, 'mu_sigma_space.png', sep=os.sep)

    labels = ['X','Y','b','Ks','S','ret']
    plt.figure(cfgs.R+1, figsize=(9, 7))
    
    for i in range(cfgs.k):
        plt.plot(mu[i],sigma[i], 'o')
    
    
    for i in range(cfgs.k):
        plt.annotate(
            labels[i],
            xy=(mu[i], sigma[i]), xytext=(-20, 20),
            textcoords='offset points', ha='right', va='bottom',
            bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
            arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))
    
    
    plt.title('Morris 1991 screening sensitivity analyses with R = {} and p = {}'.format(cfgs.R,cfgs.p))
    plt.xlabel('mu')
    plt.ylabel('sigma')
    plt.savefig(path)
    plt.close(cfgs.R+1)
    
    
def plot_rep(out_dir,rep,obs,mod):

    path = '{0}{sep}{1}{sep}{2}{sep}{3}{4}{5}'.format(os.path.dirname(
        os.path.realpath(__file__)), '..', out_dir, 'repetition_',rep+1,'.png', sep=os.sep)
    
    plt.figure(rep-1, figsize=(9, 7))
    
    plt.plot(obs.time/60, obs.val*1000*60*60, 'ro', label='observed data')
    
    for i in range(1,len(mod)):
        plt.plot(mod[i].time/60, mod[i].val*1000*60*60, 'go', label='delta model')
    
    plt.plot(mod[0].time/60, mod[0].val*1000*60*60, 'bo', label='base model')
    
    plt.xlabel('time [mins]')
    plt.ylabel('runoff [mm/hour]')
    plt.title('Repetition {}'.format(rep+1))
    plt.legend()
    plt.savefig(path)
    plt.close(rep-1)



def plot_de_residuals(obs, mod, out_dir):
    path = '{0}{sep}obs_mod_residuals.png'.format(out_dir, sep=os.sep)

    residuals = obs.val - mod.val

    plt.figure(2, figsize=(9, 7))

    n = len(obs.time)
    i = 0
    plt.plot([obs.time[i]/60, obs.time[i]/60],
             [0, residuals[i]*1000*60*60], label='obs - mod')
    for i in range(0, n):
        plt.plot([obs.time[i]/60, obs.time[i]/60],
                 [0, residuals[i]*1000*60*60])

    plt.title("Resuduals of the model ")
    plt.xlabel('time [mins]')
    plt.ylabel('residuals [mm/hour]')
    plt.legend()
    plt.savefig(path, dpi=200)
