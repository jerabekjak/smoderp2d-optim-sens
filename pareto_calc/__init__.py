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

        self._plot = False
        self._total_time = time.time()

        # folders to store good run
        self._run_dir_int = 0


    def _model(self, params, mc=False):
        """ Run the model

        :param mc: allows to record good results during monte carlo runs
        """

        sm.run(self._mod_conf, params, self._cfgs)
        mod_data = self._read_mod_file(self._mod_file)
        mod_data_wl = self._read_mod_file(self._mod_file, col = 'totalWaterLevel[m]')

        # in which times to see the restsul
        times =  (np.arange(60, max(mod_data.time), 60))
        
        mod_data_itnerp = np.interp(times, mod_data.time, mod_data.val)
        mod_data_wl_itnerp = np.interp(times, mod_data_wl.time, mod_data_wl.val)
        
        
        outfile_ = '{}/run.{:05d}'.format(self._out_dir, self._run_dir_int)
        self._run_dir_int += 1
                
        table = np.array([times, mod_data_itnerp, mod_data_wl_itnerp])
        np.savetxt(outfile_, np.transpose(table), fmt= '%.5e')
        #mod_data_wl_interp = self._read_mod_file(self._mod_file, col = 'totalWaterLevel[m]')

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


    def __del__(self):

        #write_sa(self._plus_minus_res, "plus_minus_sa.dat", self._out_dir)
        #barplot_sa(self._out_dir, self._plus_minus_res)
        #write_sa(self._monte_carlo_res, "monte_carlo_sa.dat", self._out_dir)
        print ('done in {:1.1e} secs'.format(time.time()-self._total_time))
