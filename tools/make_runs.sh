#!/bin/bash

# DESCRIPTION 
# list optim outputs which are in dir bibly_fit/
# basen that the script make runs in directory runs/
# where single runs are stored in files named 
# after the name of the simulation
# eg bibly_fit/out-trebsin_ii_2008-9 > cat runs/trebsin_ii_2008-9 >> run
# in runs/trebsin_ii_2008-9 should be the executing command e.g.:
#    ./optim.py -o out-trebsin_ii_2008-9 -m model/trebsin_ii_2008-9.ini -O cfgs/trebsin_ii_2008-9.cfg > logs/out-trebsin_ii_2008-9.log

worse=`ls blby_fit`

for i in $worse;
do 
cat runs/"${i:4}" >> runs/runs;
done
