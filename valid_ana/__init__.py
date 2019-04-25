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
from tools.writes import write_va
from tools.plots import plot_va


loc_textures = {}
loc_textures["trebsin"] = ["silty loam"]  
loc_textures["neustupov"] = ["sandy loam"]  
loc_textures["klapy"] = ["silty clay loam"]  
loc_textures["trebesice"] = ["sandy loam"]  
loc_textures["nucice"] = ["silty loam"]  
loc_textures["vsetaty"] = ["loam"]  
loc_textures["nove_straseci"] = ["loam"]  
loc_textures["risuty"] = ["loam"]  

# params for given texture
texture_pars = {}
texture_pars["silty loam"] = [10.1, 0.561, 1.74]
texture_pars["sandy loam"] = [9.2, 0.462, 1.79 ]
texture_pars["silty clay loam"] = [10.7, 0.603, 1.7]
texture_pars["loam"] = [10.1, 0.561, 1.74]


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

        self._plot = True
        self._total_time = time.time()
        
        self._nparams = 6
        
        # name of location
        self._loc_name = self._get_location_name(self._cfgs._best_fit_dir)
        
        self._texture_pars = self._get_params_for_textures(self._loc_name)


    def _model(self, params, mc=False):
        """ Run the model

        :param mc: allows to record good results during monte carlo runs
        """
        sm.run(self._mod_conf, params, self._cfgs)

        mod_data = self._read_mod_file(self._mod_file)
        self._mod_data_interp = self._interp_mod_data(
            mod=mod_data, obs=self._data)
        
        self._ss_val = sum_of_squares(self._data.val, self._mod_data_interp.val)
        self._ns_val = nash_sutcliffe(self._data.val, self._mod_data_interp.val)
        self._ss_opt = sum_of_squares(self._data.val, self._data.fit_vals)
        self._ns_opt = nash_sutcliffe(self._data.val, self._data.fit_vals)
        
    def do_va(self):
        
        params = self._get_param_set()

        self._model(params)
        
    
    def _get_params_for_textures(self, loc):
        texture = loc_textures[loc]
        return (texture_pars[texture[0]])
    
    def _get_location_name(self,path):
        """ get location name from path to bf records """
        
        loc_name = path.split('/')
        loc_name = loc_name[len(loc_name)-1]
        loc_name = loc_name.replace('out-','')
        
        i = loc_name.find('_')
        
        loc_name = (loc_name[0:i])
        
        return loc_name
        

    def _get_param_set_orig(self):
        """ returns parameters of best fit """

        params = np.zeros([self._nparams], float)
        params[0] = self._texture_pars[0]
        params[1] = self._texture_pars[1]
        params[2] = self._texture_pars[2]
        params[3] = self._cfgs.bfKs
        params[4] = self._cfgs.bfS
        params[5] = self._cfgs.bfret
        
        self._params = params

        return (params)
    

    def _get_param_set_manning(self):
        """ returns parameters of best fit """

        params = np.zeros([self._nparams], float)
        params[0] = self._cfgs.bfX
        params[1] = 0.5
        params[2] = 1.5
        params[3] = self._cfgs.bfKs
        params[4] = self._cfgs.bfS
        params[5] = self._cfgs.bfret
        
        self._params = params

        return (params)
    
    def _store_pars(self):
        """ store optim and valid parameters for write """
        
        tmp = np.zeros([2,8], float)
        tmp[0][0:6] = self._params
        tmp[0][6] = self._ss_val
        tmp[0][7] = self._ns_val
        
        tmp[1][0] = self._cfgs.bfX
        tmp[1][1] = self._cfgs.bfY
        tmp[1][2] = self._cfgs.bfb
        tmp[1][3] = self._cfgs.bfKs
        tmp[1][4] = self._cfgs.bfS
        tmp[1][5] = self._cfgs.bfret
        tmp[1][6] = self._ss_opt
        tmp[1][7] = self._ns_opt
        
        
        return (tmp)
        
        
        
    def __del__(self):
        if self._plot:
            plot_va(self._data, self._mod_data_interp, self._out_dir)
            
        res = self._store_pars()

        write_va(res, self._data, self._mod_data_interp, self._out_dir)
        
        
        
        
        
        
