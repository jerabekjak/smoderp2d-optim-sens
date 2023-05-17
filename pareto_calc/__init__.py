import os
import numpy as np
import math
from random import uniform
import time
import sys
import shutil

from diff_evol.mod_data_handling import read_mod_file
from diff_evol.mod_data_handling import interpolate
from diff_evol.mod_data_handling import RecModData
#import model.smoderp2d.main as sm
import model.smoderp2d.main_optim_sens as sm
from tools.writes import write_sa
from tools.plots import barplot_sa
from tools.optim_fnc import sum_of_squares
from tools.optim_fnc import nash_sutcliffe


class ParetoCalc(object):

    def __init__(self, pars, cfgs):
        """ init SensAnal

        :param pars: parser namespace
        """
        #self._bf_data = cfgs.data
        self._mod_data = None
        self._mod_data_interp = None
        self._mod_data_interp_wl = None # wl stands for water level
        self._cfgs = cfgs
        self._mod_conf = pars.mod_conf
        self._mod_file = self._cfgs.model_file
        #self._mcruns = cfgs.mcruns

        self._out_dir = pars.out_dir

        self._read_mod_file = read_mod_file
        self._interp_mod_data = interpolate

        self._nparams = 6
        # how much is the parameter changed
        self._proc_mv = 0.1

        # stores results from the +- proc sensitivity
        # self._nparams+1 means + ss
        self._plus_minus_res = np.zeros(
            [2*self._nparams+1, self._nparams+2], float)

        # stores results from the monte carlo sensitivity
        # self._nparams+1 means + ss
        #self._monte_carlo_res = np.zeros(
        #    [self._mcruns, self._nparams+2], float)

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

    def _get_best_param_set(self):
        """ returns parameters of best fit """

        premodel = \
            '{}'.format((os.path.basename(self._mod_conf).split('.')[0]))
        path_ = '../vysledky.4/02.fieldrs/out-{}/params.dat'.format(premodel)
        with open(path_,'r') as f_:
            lines = f_.readlines()
            X = lines[1].split(';')[0]
            Y = lines[1].split(';')[1]
            b = lines[1].split(';')[2]
            Ks = lines[1].split(';')[3]
            S = lines[1].split(';')[4]
            ret = lines[1].split(';')[5]

        params = [X,Y,b,Ks,S,ret]
        params = [float(i) for i in params]
        print (params)
        return (params)

    def _gen_plus_minus_param_set(self, i, params, plus = True):
        """ generates parameter where one parameter is proc_mv

        from the best fit

        :param i: which parameter changes
        :param proc_mv: how much (sigh gives direction)
        """

        # sub orders of magniture multiplicator
        mult = np.zeros(6, float)
        
        # multiplicator for each parameter
        # X
        mult[0] = 80
        # Y
        mult[1] = 1.3
        # b
        mult[2] = 1.125
        # Ks
        mult[3] = 2.0
        # S
        mult[4] = 2.0
        # ret
        mult[5] = 1.5
        
        for j in range(6) :
            # change sighn
            if not(plus):
                mult[0] = 1./3.5
                # Y
                mult[1] = 1.0/1.6
                # b
                mult[2] = 1.0/1.5
                # Ks
                mult[3] = 1.0/5.0
                # S
                mult[4] = 1.0/5.0
                # ret
                mult[5] = 1.0/5
            
        #newparams = np.zeros([self._nparams], float)

        #for i in range(6) :
        #newparams[i] = params[i]*mult[i]
        newparams = params[:]
        if (plus) :
             newparams[i] += newparams[i]*self._proc_mv
        if not(plus) :
             newparams[i] += -newparams[i]*self._proc_mv

        return (newparams)


    def _model(self, params, mc=False):
        """ Run the model

        :param mc: allows to record good results during monte carlo runs
        """

        sm.run(self._mod_conf, params, self._cfgs)
        print (self._mod_file)
        mod_data = self._read_mod_file(self._mod_file)
        #input('')
        mod_data_wl = self._read_mod_file(self._mod_file, col = 'totalWaterLevel[m]')

        # TODO zapsat_vysledky
        #
        #self._mod_data_interp = self._interp_mod_data(
        #    mod=mod_data, obs=self._bf_data)
        #self._mod_data_interp_wl = self._interp_mod_data(
        #    mod=mod_data_wl, obs=self._bf_data)

        #ss = sum_of_squares(self._bf_data.val, self._mod_data_interp.val)
        #ns = nash_sutcliffe(self._bf_data.val, self._mod_data_interp.val)
        #
        #return ss, ns

    def do_sa(self):

        premodel = \
        '{}'.format((os.path.basename(self._mod_conf).split('.')[0]))
        path_ = 'pareto_pars/{}.paretopars'.format(premodel)
        print (premodel)
        print (path_)


        with open(path_,'r') as f_:
            lines = f_.readlines()
    
        for line in lines:
            params =  [float(x) for x in line.split(' ')]
            self._model(params)
        #self._plus_minus_proc()

        #self._monte_carlo()


    def __del__(self):

        #write_sa(self._plus_minus_res, "plus_minus_sa.dat", self._out_dir)
        #barplot_sa(self._out_dir, self._plus_minus_res)
        #write_sa(self._monte_carlo_res, "monte_carlo_sa.dat", self._out_dir)
        print ('done in {:1.1e} secs'.format(time.time()-self._total_time))
