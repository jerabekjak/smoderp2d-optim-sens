from scipy.optimize import differential_evolution


class DiffEvol(object):

    def __init__(self, obs, pars):
        """ init diff evol 
        1 tell the model which times to store
        2 prepare the model config
        3 fo the optimizatoin (see https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.differential_evolution.html)

        :param obs: list of obs_data_handler.RecObsData instances  
        """

        self._obs = obs
        self._de = differential_evolution
        self._mod_conf = pars.mod_conf

        pass
