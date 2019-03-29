#import scipy.stats.linregress as lreg
from scipy import stats
import os
from tools.plots import plot_philip


def philip(ks, s, t):
    return 0.5*s*t**(-0.5) + ks


def transform_time(time):
    """ transform time in order to Linearize Philip formula """
    return 0.5*time**(-0.5)


def get_ks_s(data, out_dir, plot=True):
    """ return parameters of philip infiltration and store
    them into file .philip

    :param data: list of obs_data_handler.RecObsData instances  
    """
    
    # remove zeros runoff records from philips fit 
    time = data.time[data.val!=0.0]
    t_time = transform_time(time)
    infilt = data.infilt[data.val!=0.0]

    # slope = s
    # intercept = ks
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        t_time, infilt)

    path = '{0}{sep}{1}'.format(out_dir, '.philip', sep=os.sep)

    with open(path, 'w') as outfile:
        outfile.write('Do not edit!!!\n')
        outfile.write('{:.5E}\n'.format(slope))
        outfile.write('{:.5E}\n'.format(intercept))

    if plot:
        plot_philip(fnc=philip, ks=intercept, s=slope,
                    out_dir=out_dir, obs_data=data)
