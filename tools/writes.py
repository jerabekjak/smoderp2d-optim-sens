import os


def write_de(obs, mod, result, out_dir):

    path_params = '{0}{sep}params.dat'.format(out_dir, sep=os.sep)
    path_val = '{0}{sep}obs_mod.dat'.format(out_dir, sep=os.sep)

    with open(path_params, 'w') as pf:
        pf.write('X;Y;b;Ks;S\n')
        for ix in result.x:
            pf.write('{:1.3e};'.format(ix))

    with open(path_params, 'a') as pf:
        pf.write('{:1.3e}'.format(result.fun))

    n = len(obs.time)
    with open(path_val, 'w') as vf:
        vf.write('time_sec;obs_m_s_1;mod_m_s_1\n')
        for i in range(n):
            vf.write('{:1.3e};{:1.5e};{:1.5e}\n'.format(
                obs.time[i], obs.val[i], mod.val[i]))
