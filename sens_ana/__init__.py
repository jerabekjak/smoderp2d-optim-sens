from diff_evol import DiffEvol
from diff_evol import sum_of_squares

from diff_evol.mod_data_handling import read_mod_file
from diff_evol.mod_data_handling import interpolate
from diff_evol.mod_data_handling import RecModData
from tools.writes import write_plus_minus_sa
import model.smoderp2d.main as sm

import os
import numpy as np
import math
from random import uniform
from random import randint


class SensAna(DiffEvol):

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

        self._out_dir = pars.out_dir

        self._read_mod_file = read_mod_file
        self._interp_mod_data = interpolate

        self._nparams = 6
        # how much is the parameter changed
        self._proc_mv = 0.1

        # stores results from the +- proc sensitivity
        # self._nparams+1 means + ss
        self._plus_minus_res = np.zeros(
            [2*self._nparams, self._nparams+1], float)

        self._plot = False

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

    def _model(self, params):

        sm.run(self._mod_conf, params, self._cfgs)

        mod_data = self._read_mod_file(self._mod_file)
        self._mod_data_interp = self._interp_mod_data(
            mod=mod_data, obs=self._bf_data)

        ss = sum_of_squares(self._bf_data.val, self._mod_data_interp.val)

        return(ss)

    def plus_minus_proc(self):

        for i in range(self._nparams):
            params = self._gen_plus_minus_param_set(i, self._proc_mv)
            self._plus_minus_res[2*i][0:self._nparams] = params
            self._plus_minus_res[2*i][self._nparams] = self._model(params)
            params = self._gen_plus_minus_param_set(i, -self._proc_mv)
            self._plus_minus_res[2*i+1][0:self._nparams] = params
            self._plus_minus_res[2*i+1][self._nparams] = self._model(params)

    def do_sa(self):

        self.plus_minus_proc()

        #ss_d = self.model(par_d)

    def __del__(self):

        write_plus_minus_sa(self._plus_minus_res, self._out_dir)
        print ('sens.py done')
