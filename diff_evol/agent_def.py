class Agent(object) :
    
    def __init__(self,n_dim):
        
        self._pos = [-1.]*n_dim
        
        self._obj_fnc_val_new = 3e99
        self._obj_fnc_val_old = 3e99
        
        
