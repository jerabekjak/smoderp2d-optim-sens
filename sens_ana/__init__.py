from diff_evol import DiffEvol

from diff_evol.mod_data_handling import read_mod_file
from diff_evol.mod_data_handling import interpolate

class SensAna(DiffEvol):

    def __init__(self, pars,  obs):
        """ init SensAnal
        
        :param pars: parser namespace
        :param obs: list of obs_data_handler.RecObsData instances  
        """
        self._obs = obs
        self._obs_data = obs.data
        self._mod_data = None
        self._mod_data_interp = None
        self._mod_conf = pars.mod_conf
        self._out_dir = pars.out_dir
        self._mod_file = obs.model_file
        self._read_mod_file = read_mod_file
        self._interp_mod_data = interpolate
        self._plot = True
        self._model_runs = 0
        
    def __del__(sefl):
        pass
    
