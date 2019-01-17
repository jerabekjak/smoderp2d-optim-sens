from scipy.optimize import differential_evolution
import time

import model.smoderp2d.main as sm
from diff_evol.mod_data_handling import read_mod_file
from diff_evol.mod_data_handling import interpolate
from tools.plots import plot_de


# objective function


def sum_of_squares(obs, mod):

    r = obs - mod
    r = r**2.0

    return sum(r)


class DiffEvol(object):

    def __init__(self, pars,  obs):
        """ init diff evol 
        1 tell the model which times to store
        2 prepare the model config
        3 fo the optimizatoin (see https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.differential_evolution.html)

        :param pars: parser namespace
        :param obs: list of obs_data_handler.RecObsData instances  
        """
        self._obs = obs
        self._obs_data = obs.data
        self._mod_data = None
        self._mod_data_interp = None
        self._de = differential_evolution
        self._mod_conf = pars.mod_conf
        self._out_dir = pars.out_dir
        self._mod_file = obs.model_file
        self._read_mod_file = read_mod_file
        self._interp_mod_data = interpolate
        self._plot = True
        self._model_runs = 0

    def model(self, params):
        """ compute model and comare it with the data

        :param params: smoderp parameters [X,Y,b,ks,s]
        """
        t1 = time.time()
        sm.run(self._mod_conf, params, self._obs)
        t2 = time.time()
        
        self._mod_data = self._read_mod_file(self._mod_file)

        self._mod_data_interp = self._interp_mod_data(
            mod=self._mod_data, obs=self._obs_data)

        ss = sum_of_squares(self._obs_data.val, self._mod_data_interp.val)
        
        self._model_runs += 1

        print ('model run {} runs {:1.4e} secs with ss = {:1.4e} ...'.format(self._model_runs, t2-t1, ss))

        return sum_of_squares(self._obs_data.val, self._mod_data_interp.val)

    def make_de(self):

        # bounds for parameters [X,Y,b]
        bounds = [(1, 400), (0.001, 1.), (1.5, 2.0), (1e-8,1e-5), (1e-8,1e-5)]
        self.result = differential_evolution(
            self.model, bounds, disp=True, maxiter=1, tol=1e-10)


    def __del__(self):

        if self._plot:
            plot_de(self._obs_data, self._mod_data_interp,
                    self.result, self._out_dir)
            
        print ('\n{}'.format(self.result.message))
        print ('{} model runs during optimalization'.format(self._model_runs))
        print ('final parameters: X={:.2E}, Y={:.2E}, b={:.2E}'.format(
            self.result.x[0], self.result.x[1], self.result.x[2]))
        print ('sum of squares = {:.2E}'.format(self.result.fun))
        print (self.result)
