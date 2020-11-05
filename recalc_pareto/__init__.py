from diff_evol import DiffEvol

class RecalcPareto(DiffEvol):
    def __init__(self, pars, obs):
        super(RecalcPareto, self).__init__(pars, obs)
        self.pars_matrix_path = pars.opt_conf.replace('.cfgs', '.pars')
        with open(self.pars_matrix_path, 'r') as f :
            lines = f.readlines()

        self.pars_matrix = []
        for line in lines:
            list_ = (line.replace('\n','').split('\t'))
            list_ = [float(x) for x in list_]
            self.pars_matrix.append(list_)

    def __del__(self):
        print ("\n\n\nENDE\n\n\n--------------------------")
    
