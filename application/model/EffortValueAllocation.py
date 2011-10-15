
class EffortValuesAllocation:
    
    def __init__(self):
        self.e_vals = {'hp': 0, 'b': 0, 'd': 0}
        self.defences = {'b': 1000.0, 'd': 1000.0}
        self.damages = {'b': 1000, 'd': 1000}
        self.params = {'hp': 0, 'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0}
    
    def setAllocation(self, e_vals, defences, damages):
        """
        pre::
            0 <= e_vals['hp'] <= 255
            0 <= e_vals['b']  <= 255
            0 <= e_vals['d']  <= 255
        """
        #assert 0 <= e_vals['hp'] <= 255
        #assert 0 <= e_vals['b'] <= 255
        #assert 0 <= e_vals['d'] <= 255
        
        self.e_vals = e_vals
        self.defences = defences
        self.damages = damages
    
    def isHarder(self, defences, damages, which):
        if(which == 'both'):
            arg_defence = defences['b'] + defences['d']
            arg_damage = damages['b'] + damages['d']
            cur_defence = self.defences['b'] + self.defences['d']
            cur_damage = self.damages['b'] + self.damages['d']
        else:
            arg_defence = defences[which]
            arg_damage = damages[which]
            cur_defence = self.defences[which]
            cur_damage = self.damages[which]
        
        if(cur_defence > arg_defence):
            return True
        elif(cur_defence == arg_defence):
            if(cur_damage > arg_damage):
                return True
            else:
                return False
        else:
            return False

    def setParam(self, key, param):
        self.params[key] == param
        return
    
    def setParams(self, params):
        for key in params.keys():
            self.params[key] = params[key]
        return

