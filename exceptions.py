class Error(Exception):
    pass



class IncorrectDataInObsFile(Error):

    """Exception raised if the water level goes to negative values.

    """

    def __init__(self,val):
        self.msg = 'Incorrect observation data: '+str(val)

    def __str__(self):
        return repr(self.msg)
