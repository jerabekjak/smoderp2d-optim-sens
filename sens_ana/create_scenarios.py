#!/usr/bin/python3
# stand alone scrip to create scenarios
# run: ./sens_ana/create_scenarios.py

import numpy as np
if __name__ == '__main__':
    X = np.arange(10, 210, 10)
    Y = np.arange(0.1, 1.1, 0.1)
    b = [1.6]
    
    path = 'sens_ana/scenarios.dat'
    
    with open(path, 'w') as sc:
        for ix in X :
            for iy in Y :
                for ib in b :
                    line = '{:.5e}\t{:.5e}\t{:.5e}\n'.format(ix,iy,ib)
                    sc.write(line)
    
