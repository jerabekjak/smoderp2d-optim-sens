import os
import numpy as np
from tools.optim_fnc import nash_sutcliffe


def write_de(obs, mod_h, mod_q, result, out_dir):

    path_params = '{0}{sep}params.dat'.format(out_dir, sep=os.sep)
    path_val_h = '{0}{sep}obs_mod_h.dat'.format(out_dir, sep=os.sep)
    path_val_q = '{0}{sep}obs_mod_q.dat'.format(out_dir, sep=os.sep)

    with open(path_params, 'w') as pf:
        pf.write('X;Y;b;Ks;S;ret;slope;rainfall;SofSq;NashSutcliffe_h;NashSutcliffe_q\n')
        for ix in result.x:
            pf.write('{:1.3e};'.format(ix))
        pf.write('{:1.3e};'.format(obs.slope))
        pf.write('{:1.3e};'.format(obs.rainfall))

    with open(path_params, 'a') as pf:
        pf.write('{:1.3e};'.format(result.fun))
        pf.write('{:1.3e};'.format(nash_sutcliffe(obs.data_h.val, mod_h.val)))
        pf.write('{:1.3e}'.format(nash_sutcliffe(obs.data_q.val, mod_q.val)))

    n = len(obs.data_h.time)
    with open(path_val_h, 'w') as vf:
        vf.write('time_sec;obs_m;mod_m\n')
        for i in range(n):
            vf.write('{:1.3e};{:1.5e};{:1.5e}\n'.format(
                obs.data_h.time[i], 
                obs.data_h.val[i], mod_h.val[i]))

    n = len(obs.data_q.time)
    with open(path_val_q, 'w') as vf:
        vf.write('time_sec;obs_m;mod_m\n')
        for i in range(n):
            vf.write('{:1.3e};{:1.5e};{:1.5e}\n'.format(
                obs.data_q.time[i], 
                obs.data_q.val[i], mod_q.val[i]))

def write_sa(res, file_ ,out_dir):

    path_params = '{0}{sep}{1}'.format(out_dir, file_, sep=os.sep)

    np.savetxt(path_params, res, fmt='%1.4e',comments='',
               header='X;Y;b;Ks;S;ret;SofSq;NashSutcliffe', delimiter=';')
    
def write_va(res, obs, mod_orig, mod_manning, out_dir):

    path_params = '{0}{sep}params.dat'.format(out_dir, sep=os.sep)

    np.savetxt(path_params, res, fmt='%1.4e',comments='',
               header='X;Y;b;Ks;S;ret;SofSq;NashSutcliffe', delimiter=';')

    path_val = '{0}{sep}obs_mod_val.dat'.format(out_dir, sep=os.sep)
    n = len(obs.time)
    with open(path_val, 'w') as vf:
        vf.write('time_sec;obs_m_s_1;opt_m_s_1;val_m_s_1;manning_m_s_1\n')
        for i in range(n):
            vf.write('{:1.3e};{:1.5e};{:1.5e};{:1.5e};{:1.5e}\n'.format(
                obs.time[i], obs.val[i], obs.fit_vals[i], mod_orig.val[i], mod_manning.val[i]))
