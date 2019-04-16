import os
import numpy as np
import math
#from random import uniform
import time
import sys

from diff_evol.mod_data_handling import read_mod_file
from diff_evol.mod_data_handling import interpolate
#from diff_evol.mod_data_handling import RecModData
import model.smoderp2d.main as sm
from tools.optim_fnc import sum_of_squares
from tools.optim_fnc import nash_sutcliffe


class ValidAna(object):

    def __init__(self, pars, cfgs):
        
        # data contains observed data and fitted data
        self._data = cfgs.data
        self._mod_data = None
        self._mod_data_interp = None
        self._cfgs = cfgs
        self._mod_conf = pars.mod_conf
        self._mod_file = self._cfgs.model_file

        self._out_dir = pars.out_dir

        self._read_mod_file = read_mod_file
        self._interp_mod_data = interpolate

        self._plot = False
        self._total_time = time.time()
        
        print (self._cfgs._best_fit_dir)

    
    def do_va(self):
        pass
