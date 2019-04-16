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
texture_pars["silty clay sloam"] = [10.7, 0.603, 1.7]
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
        
        ss = sum_of_squares(self._data.val, self._mod_data_interp.val)
        ns = nash_sutcliffe(self._data.val, self._mod_data_interp.val)
        
        return ss, ns
    
    def do_va(self):
        
        params = self._get_param_set()

        ss, ns = self._model(params)
        
        print (ss, ns)
        
        
    
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
        
    def _get_param_set(self):
        """ returns parameters of best fit """

        params = np.zeros([self._nparams], float)
        params[0] = self._texture_pars[0]
        params[1] = self._texture_pars[1]
        params[2] = self._texture_pars[2]
        params[3] = self._cfgs.bfKs
        params[4] = self._cfgs.bfS
        params[5] = self._cfgs.bfret

        return (params)
    
    
    def __del__(self):
        if self._plot:
            plot_va(self._data, self._mod_data_interp, self._out_dir)

        
        
        
        
        
        
