from scipy.optimize import differential_evolution
from scipy.optimize import minimize
from scipy.optimize import OptimizeResult
import time

import model.smoderp2d.main as sm
from diff_evol.mod_data_handling import read_mod_file
from diff_evol.mod_data_handling import interpolate
from tools.plots import plot_de
from tools.writes import write_de
from tools.plots import plot_de_residuals

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
        self.result = OptimizeResult

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

        self.result.x = params
        self.result.fun = ss
        self.result.message = 'I stopped the optimization...'

        self._model_runs += 1

        print ('model run {} runs {:1.2f} secs with ss = {:1.4e} ...'.format(
            self._model_runs, t2-t1, ss))
        print ('\t with pars set {:1.4e},{:1.4e},{:1.4e},{:1.4e},{:1.4e},{:1.4e} ...'.format(
            params[0], params[1], params[2], params[3], params[4], params[5]))

        return sum_of_squares(self._obs_data.val, self._mod_data_interp.val)

    def make_de(self):

        # bounds for parameters [X,Y,b]
        bounds = [(1, 20), (0.01, 1.), (1., 2.0),
                  (1e-8, 1e-5), (1e-8, 1e-3), (-0.1, 0)]
        #x0 = [3.5822e+02, 7.6509e-01, 1.6578e+00, 4.4133e-06, 7.9349e-06]
        #self.result = minimize(self.model, x0, method='Nelder-Mead')
        self.result = differential_evolution(self.model, bounds, disp=True)

    def __del__(self):

        if self._plot:
            plot_de(self._obs_data, self._mod_data_interp,
                    self.result, self._out_dir)
            plot_de_residuals(self._obs_data, self._mod_data_interp, self._out_dir)

        write_de(self._obs_data, self._mod_data_interp,
                 self.result, self._out_dir)
        

        print ('\n{}'.format(self.result.message))
        print ('{} model runs during optimalization'.format(self._model_runs))
        print ('final parameters: X={:.2E}, Y={:.2E}, b={:.2E}\n\tKs={:.2E}, S={:.2E}, ret={:.2E}'.format(
            self.result.x[0], self.result.x[1], self.result.x[2], self.result.x[3], self.result.x[4], self.result.x[5]))
        print ('sum of squares = {:.2E}'.format(self.result.fun))
        print (self.result)
