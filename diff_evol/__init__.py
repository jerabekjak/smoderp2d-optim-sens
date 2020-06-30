import time

import model.smoderp2d.main_optim_sens as sm
from diff_evol.mod_data_handling import read_mod_file
from diff_evol.mod_data_handling import interpolate
from diff_evol.mod_data_handling import RecModData
from tools.plots import plot_de
from tools.writes import write_de
from tools.plots import plot_de_residuals
from tools.optim_fnc import sum_of_squares

class DiffEvol(object):

    def __init__(self, pars,  obs):
        from scipy.optimize import differential_evolution
        from scipy.optimize import minimize
        from scipy.optimize import OptimizeResult
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
        # prepare for repeating run
        self._mod_data_interp = RecModData(len(self._obs_data.time))
        self._de = differential_evolution
        self._minimize = minimize
        self._mod_conf = pars.mod_conf
        self._out_dir = pars.out_dir
        self._mod_file = obs.model_file
        self._read_mod_file = read_mod_file
        self._interp_mod_data = interpolate
        self._plot = True
        self._plot = False
        self._model_runs = 0
        # count iterations
        self.iter_ = 0
        self.result = OptimizeResult

        # repeat optimalization id best fit is zero vector
        self._maxIter = 5

    def model(self, params):
        """ compute model and comare it with the data

        :param params: smoderp parameters [X,Y,b,ks,s]
        """
        t1 = time.time()
        sm.run(self._mod_conf, params, self._obs)
        t2 = time.time()

        self._mod_data = self._read_mod_file(self._mod_file,
                col = 'totalWaterLevel[m]')

        self._mod_data_interp = self._interp_mod_data(
            mod=self._mod_data, obs=self._obs_data)

        ss = sum_of_squares(self._obs_data.val, self._mod_data_interp.val)
        if (self._mod_data_interp.val.sum() == 0) :
            ss = 1

        self.result.x = params
        self.result.fun = ss
        self.result.message = 'I stopped the optimization...'

        self._model_runs += 1

        print ('In interation ;{}; model run ;{}; runs ;{:1.2f}; secs with ss = ;{:1.4e};with pars set ;{:1.4e};{:1.4e};{:1.4e};{:1.4e};{:1.4e};{:1.4e}'.format(self.iter_,
                                                                                                                                                                self._model_runs, t2-t1, ss, params[0], params[1], params[2], params[3], params[4], params[5]))

        return ss

    def make_de(self):

        # bounds for parameters [X,Y,b]
        bounds = [(1, 20), (0.01, 1.), (1., 2.0),
                  (1e-8, 1e-6), (1e-8, 1e-1), (-0.005, 0)]
        #bounds = [(1, 30), (0.01, 5.), (1., 4.0),
        #         (1e-8, 1e-5), (1e-8, 1e-3), (-0.5, 0)]
        x0 = [1e+01, 5e-01, 1.5e+00, 4.4133e-08, 7.9349e-06, -0.001]
        self.result = self._minimize(self.model, x0, method='Nelder-Mead')
        #self.result = self._minimize(self.model, x0, method='CG')

       # self.result = self._de(self.model, bounds, disp=False,
       #         init='random'
       #         #mutation=(0.1,0.9),
       #         #recombination=0.9,
       #         #strategy='rand2exp'
       #         )
       #         #popsize=5, maxiter=4)
       # print ('vals {}'.format(self._mod_data_interp.val))

        #self._mod_data_interp.val.fill(0.0)
        #while self._mod_data_interp.val.sum() == 0.0:
        #    self.iter_ += 1
        #    if (self._max_iter()):
        #        break
        #    self.result = self._de(self.model, bounds, disp=False,
        #    strategy='best2exp', popsize=4, maxiter=3)
        #    print ('vals {}'.format(self._mod_data_interp.val))

    def _max_iter(self):
        return self.iter_ > self._maxIter

    def __del__(self):

        print ('\n{}'.format(self.result.message))
        print ('{} model runs during optimalization'.format(self._model_runs))
        print ('final parameters: X={:.2E}, Y={:.2E}, b={:.2E}\n\tKs={:.2E}, S={:.2E}, ret={:.2E}'.format(
            self.result.x[0], self.result.x[1], self.result.x[2], self.result.x[3], self.result.x[4], self.result.x[5]))
        print ('sum of squares = {:.2E}'.format(self.result.fun))
        print (self.result)

        if self._plot:
            plot_de(self._obs_data, self._mod_data_interp,
                    self.result, self._out_dir)
            plot_de_residuals(
                self._obs_data, self._mod_data_interp, self._out_dir)

        write_de(self._obs, self._mod_data_interp,
                 self.result, self._out_dir)

