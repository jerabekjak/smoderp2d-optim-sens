from exceptions import IncorrectDataInObsFile


class RecObsData(object):
    """ RecObsData contains data of one observed record """

    def __init__(self, time, val):

        self.time = time
        self.val = val


class ObsData(object):
    """ ObsData handle obs data reading 

    public list self.data of RecObsData instances
    """

    def __init__(self, obs_path):

        ob_f = open(obs_path, 'r')

        ob_ls = ob_f.readlines()

        n_read = False

        self.data = []

        for line in ob_ls:
            if ('#' in line[0:4]):
                continue
            else:
                if (not(n_read)):
                    self.n = self.read_line_n(line)
                    n_read = True
                else:
                    time = (self.read_line_vals(line)[0])
                    val = (self.read_line_vals(line)[1])
                    self.data.append(RecObsData(time, val))

        for i in range(3, (3+self.n)):
            l = ob_ls[i]

        ob_f.close()

    def read_line_n(self, _line):
        try:
            val = int(_line)
        except ValueError:
            raise IncorrectDataInObsFile(_line)
        return val

    def read_line_vals(self, _line):

        _line = _line.replace('\n', '').split('\t')
        if not(len(_line) == 2):
            raise IncorrectDataInObsFile(_line)

        try:
            val = list(_line)
        except ValueError:
            raise IncorrectDataInObsFile(_line)

        try:
            time = float(val[0])
        except ValueError:
            raise IncorrectDataInObsFile(val[0])

        try:
            obs = float(val[1])
        except ValueError:
            raise IncorrectDataInObsFile(val[1])
        return time, obs
