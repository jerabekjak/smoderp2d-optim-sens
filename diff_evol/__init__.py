import time
import math

import model.smoderp2d.main_optim_sens as sm
from diff_evol.mod_data_handling import read_mod_file
from diff_evol.mod_data_handling import interpolate
from diff_evol.mod_data_handling import RecModData
from tools.plots import plot_de
from tools.writes import write_de
from tools.plots import plot_de_residuals
from tools.optim_fnc import sum_of_squares
from tools.optim_fnc import nash_sutcliffe as ns

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
        self._obs_data_h = obs.data_h
        self._obs_data_q = obs.data_q
        self._mod_data_h = None
        self._mod_data_q = None
        # prepare for repeating run
        self._mod_data_h_interp = RecModData(len(self._obs_data_h.time))
        self._mod_data_q_interp = RecModData(len(self._obs_data_q.time))
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
        if  (any(params[0:5]<=0)) :
            self.result.x = params
            self.result.fun = 999
            self.result.message = 'I stopped the optimization...'
            return 999

        t1 = time.time()
        sm.run(self._mod_conf, params, self._obs)
        t2 = time.time()

        self._mod_data_h = self._read_mod_file(self._mod_file,
                col = 'totalWaterLevel[m]')
        self._mod_data_q = self._read_mod_file(self._mod_file,
                col = 'surfaceFlow[m3/s]')
        self._mod_data_q.val = [
                self._mod_data_q.val / 16 for self._mod_data_q.val in self._mod_data_q.val]

        self._mod_data_h_interp = self._interp_mod_data(
                mod=self._mod_data_h, obs=self._obs_data_h)
        self._mod_data_q_interp = self._interp_mod_data(
                mod=self._mod_data_q, obs=self._obs_data_q)

        ssh = sum_of_squares(self._obs_data_h.val, self._mod_data_h_interp.val)
        ssq = sum_of_squares(self._obs_data_q.val,
                self._mod_data_q_interp.val)*100
        nsh = ns(self._obs_data_h.val, self._mod_data_h_interp.val)
        nsq = ns(self._obs_data_q.val, self._mod_data_q_interp.val)
        ss = (ssh*math.log10(ssh) + ssq*math.log10(ssq))/(math.log10(ssh)+math.log10(ssq))
        if (self._mod_data_h_interp.val.sum() == 0) :
            ss = 1e0
        if (self._mod_data_q_interp.val.sum() == 0) :
            ss = 1e0

        self.result.x = params
        self.result.fun = ss
        self.result.message = 'I stopped the optimization...'

        self._model_runs += 1

        #print ('In interation ;{}; model run ;{}; runs ;{:1.2f}; secs with ss = ;{:1.4e};with pars set ;{:1.4e};{:1.4e};{:1.4e};{:1.4e};{:1.4e};{:1.4e}'.format(self.iter_,
        msg =   'In interation ;{}; model run ;{}; runs;{:1.2f} secs;'.format(self.iter_,self._model_runs, t2-t1)
        msg +=  'with ssh = ;{:1.4e};'.format(ssh)
        msg +=  'with ssq = ;{:1.4e};'.format(ssq)
        msg +=  'with ss = ;{:1.4e};'.format(ss)
        msg +=  'with nsh = ;{:1.4e};'.format(nsh)
        msg +=  'with nsq = ;{:1.4e};'.format(nsq)
        msg +=  'with pars set;{:1.4e};{:1.4e};{:1.4e};{:1.4e};{:1.4e};{:1.4e}'.format(params[0], params[1], params[2], params[3], params[4], params[5])
        print (msg)

        return ss

    def make_de(self):

        # bounds for parameters [X,Y,b]
        #bounds = [(1, 20), (0.01, 1.), (1., 2.0),
        #          (1e-8, 1e-6), (1e-8, 1e-1), (-0.005, 0)]
        bounds = [(1, 100), (0.01, 5.), (1., 2.0),
                 (1e-9, 1e-4), (0, 1e-1), (-0.01, 0)]
        x0 = [1e+01, 5e-01, 1.5e+00, 4.4133e-08, 7.9349e-06, -0.001]
        #self.result = self._minimize(self.model, x0, method='Nelder-Mead')
        #self.result = self._minimize(self.model, x0, method='CG')

        self._mod_data_q_interp.val.fill(0.0)
        while self._mod_data_q_interp.val.sum() == 0.0:
            self.iter_ += 1
            if (self._max_iter()):
                break
            self.result = self._de(self.model, bounds, disp=False,
                    # init='random',
                    init='latinhypercube',
                    # mutation=(0.5,1.9),
                    #mutation=1.5,
                    #maxiter=1,
                    popsize=100,
                    #recombination=0.9,
                    # strategy='randtobest1exp'
                    )
                    #popsize=5, maxiter=4)

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

        write_de(self._obs, 
                self._mod_data_h_interp,
                self._mod_data_q_interp,
                self.result, self._out_dir)

