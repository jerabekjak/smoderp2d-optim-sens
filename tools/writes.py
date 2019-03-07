import os
import numpy as np
from tools.optim_fnc import nash_sutcliffe


def write_de(obs, mod, result, out_dir):

    path_params = '{0}{sep}params.dat'.format(out_dir, sep=os.sep)
    path_val = '{0}{sep}obs_mod.dat'.format(out_dir, sep=os.sep)

    with open(path_params, 'w') as pf:
        pf.write('X;Y;b;Ks;S;ret;slope;rainfall;SofSq;NashSutcliffe\n')
        for ix in result.x:
            pf.write('{:1.3e};'.format(ix))
        pf.write('{:1.3e};'.format(obs.slope))
        pf.write('{:1.3e};'.format(obs.rainfall))

    with open(path_params, 'a') as pf:
        pf.write('{:1.3e};'.format(result.fun))
        pf.write('{:1.3e}'.format(nash_sutcliffe(obs.data.val, mod.val)))

    n = len(obs.data.time)
    with open(path_val, 'w') as vf:
        vf.write('time_sec;obs_m_s_1;mod_m_s_1\n')
        for i in range(n):
            vf.write('{:1.3e};{:1.5e};{:1.5e}\n'.format(
                obs.data.time[i], obs.data.val[i], mod.val[i]))


def write_sa(res, file_ ,out_dir):

    path_params = '{0}{sep}{1}'.format(out_dir, file_, sep=os.sep)

    np.savetxt(path_params, res, fmt='%1.4e',comments='',
               header='X;Y;b;Ks;S;ret;SofSq;NashSutcliffe', delimiter=';')
