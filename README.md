Optimalization usage:

```
usage: optim.py [-h] [-o OUT_DIR] [-m MOD_CONF] [-O OPT_CONF]

Optimize smoderp2d with differential evolution.
-----------------------------------------------

optional arguments:
  -h, --help            show this help message and exit
  -o OUT_DIR, --out_dir OUT_DIR
                        directory to store the optimaze results [default: out-
                        test]
  -m MOD_CONF, --mod_conf MOD_CONF
                        location of model config file [default:
                        model/test.ini]
  -O OPT_CONF, --opt_conf OPT_CONF
                        location of optimization config file [default:
                        optim.cfg]
```



Sensitivity analysis usage:

```
usage: sens.py [-h] [-O SENS_CONF] [-m MOD_CONF] [-o OUT_DIR]

Sensitivity analysis of smoderp2d based on Morris 1991
------------------------------------------------------

optional arguments:
  -h, --help            show this help message and exit
  -O SENS_CONF, --sens_conf SENS_CONF
                        location of sens. analysis config file [default:
                        sens.cfg]
  -m MOD_CONF, --mod_conf MOD_CONF
                        location of model ini file [default: model/test.ini]
  -o OUT_DIR, --out_dir OUT_DIR
                        directory to store the results [default: out-test-
                        sens]
```
