import os
import numpy as np
import math
from random import uniform
import time
import sys

from diff_evol.mod_data_handling import read_mod_file
from diff_evol.mod_data_handling import interpolate
from diff_evol.mod_data_handling import RecModData
import model.smoderp2d.main as sm
from tools.writes import write_sa
from tools.optim_fnc import sum_of_squares
from tools.optim_fnc import nash_sutcliffe


class SensAna(object):

    def __init__(self, pars, cfgs):
        """ init SensAnal

        :param pars: parser namespace
        """
        self._bf_data = cfgs.data
        self._mod_data = None
        self._mod_data_interp = None
        self._cfgs = cfgs
        self._mod_conf = pars.mod_conf
        self._mod_file = self._cfgs.model_file
        self._mcruns = cfgs.mcruns

        self._out_dir = pars.out_dir

        self._read_mod_file = read_mod_file
        self._interp_mod_data = interpolate

        self._nparams = 6
        # how much is the parameter changed
        self._proc_mv = 0.1

        # stores results from the +- proc sensitivity
        # self._nparams+1 means + ss
        self._plus_minus_res = np.zeros(
            [2*self._nparams, self._nparams+2], float)

        # stores results from the monte carlo sensitivity
        # self._nparams+1 means + ss
        self._monte_carlo_res = np.zeros(
            [self._mcruns, self._nparams+2], float)

        self._plot = False
        self._total_time = time.time()

        # folders to store good run
        self._good_run_dir_int = 0

    def _get_param_set(self):

        params = np.zeros([self._cfgs.k], float)

        i = randint(0, self._cfgs.p-1)
        params[0] = self._X_levels[i]
        i = randint(0, self._cfgs.p-1)
        params[1] = self._Y_levels[i]
        i = randint(0, self._cfgs.p-1)
        params[2] = self._b_levels[i]
        i = randint(0, self._cfgs.p-1)
        params[3] = self._Ks_levels[i]
        i = randint(0, self._cfgs.p-1)
        params[4] = self._S_levels[i]
        i = randint(0, self._cfgs.p-1)
        params[5] = self._ret_levels[i]

        return (params)

    def _gen_plus_minus_param_set(self, i, proc_mv):
        """ generates parameter where one parameter is proc_mv
        from the best fit

        :param i: which parameter changes
        :param proc_mv: how much (sigh gives direction)
        """

        params = np.zeros([self._nparams], float)
        params[0] = self._cfgs.bfX
        params[1] = self._cfgs.bfY
        params[2] = self._cfgs.bfb
        params[3] = self._cfgs.bfKs
        params[4] = self._cfgs.bfS
        params[5] = self._cfgs.bfret

        params[i] += params[i]*proc_mv

        return (params)

    def _gen_monte_carlo_param_set(self):

        params = np.zeros([self._nparams], float)
        params[0] = uniform(self._cfgs.X[0], self._cfgs.X[1])
        params[1] = uniform(self._cfgs.Y[0], self._cfgs.Y[1])
        params[2] = uniform(self._cfgs.b[0], self._cfgs.b[1])
        params[3] = uniform(self._cfgs.Ks[0], self._cfgs.Ks[1])
        params[4] = uniform(self._cfgs.S[0], self._cfgs.S[1])
        params[5] = uniform(self._cfgs.ret[0], self._cfgs.ret[1])

        return params

    def _model(self, params, mc=False):
        """ Run the model

        :param mc: allows to record good results during monte carlo runs
        """

        sm.run(self._mod_conf, params, self._cfgs)

        mod_data = self._read_mod_file(self._mod_file)
        self._mod_data_interp = self._interp_mod_data(
            mod=mod_data, obs=self._bf_data)

        ss = sum_of_squares(self._bf_data.val, self._mod_data_interp.val)
        ns = nash_sutcliffe(self._bf_data.val, self._mod_data_interp.val)

        return ss, ns

    def _plus_minus_proc(self):

        print ('# plus minus sensitivity...')
        for i in range(self._nparams):

            sys.stdout.write('run {}/{}'.format((i+1)*2, self._nparams*2))
            t1 = time.time()

            params = self._gen_plus_minus_param_set(i, self._proc_mv)
            self._plus_minus_res[2*i][0:self._nparams] = params
            self._plus_minus_res[2 *
                                 i][self._nparams:(self._nparams+2)] = self._model(params)

            params = self._gen_plus_minus_param_set(i, -self._proc_mv)
            self._plus_minus_res[2*i+1][0:self._nparams] = params
            self._plus_minus_res[2*i +
                                 1][self._nparams:(self._nparams+2)] = self._model(params)

            t2 = time.time()
            print (' done in {:1.2f} secs'.format(t2-t1))

    def _monte_carlo(self):

        print ('# monte carlo sensitivity...')
        for i in range(self._mcruns):
            sys.stdout.write('run {}/{}'.format((i+1), self._mcruns))
            t1 = time.time()

            # generates parameter set
            params = self._gen_monte_carlo_param_set()

            # store parameter set
            results = np.zeros(self._nparams+2)
            results[0:self._nparams] = params
            results[self._nparams:(self._nparams+2)
                    ] = self._model(params, mc=True)

            # recond results
            self._monte_carlo_res[i][:] = results

            ns = results[self._nparams+2-1]
            if (ns > 0):
                self._store_good_run(results)

            t2 = time.time()
            print (' done in {:1.2f} secs'.format(t2-t1))

    def do_sa(self):

        # self._plus_minus_proc()

        self._monte_carlo()

    def _store_good_run(self, results):

        int_ = self._good_run_dir_int
        dir_ = '{0}{sep}{1}'.format(
            self._out_dir, str(int_).zfill(5), sep=os.sep)
        if not os.path.exists(dir_):
            os.makedirs(dir_)

        path_run = '{0}{sep}{1}'.format(dir_, 'params.dat', sep=os.sep)
        with open(path_run, 'w') as pf:
            pf.write('X;Y;b;Ks;S;ret;SofSq;NashSutcliffe\n')
            for ix in results[0:(self._nparams+1)]:
                pf.write('{:1.3e};'.format(ix))
            pf.write('{:1.3e}'.format(results[self._nparams+2-1]))

        n = len(self._bf_data.time)

        path_run = '{0}{sep}{1}'.format(dir_, 'mod_obs.dat', sep=os.sep)

        print_arr = np.zeros([3, n], float)
        print_arr[0] = self._bf_data.time
        print_arr[1] = self._bf_data.val
        print_arr[2] = self._mod_data_interp.val
        print_arr = np.transpose(print_arr)

        np.savetxt(path_run, print_arr, fmt='%1.4e',
                   header='time;obs;mod', delimiter=';')

        # updata dir name
        self._good_run_dir_int += 1

    def __del__(self):

        write_sa(self._plus_minus_res, "plus_minus_sa.dat", self._out_dir)
        write_sa(self._monte_carlo_res, "monte_carlo_sa.dat", self._out_dir)
        print ('done in {:1.1e} secs'.format(time.time()-self._total_time))
