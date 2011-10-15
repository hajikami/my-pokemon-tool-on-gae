from gaeo.controller import BaseController
import math
import logging
from model import Pokemon
from model import EffortValueAllocation
from model import TestEffortValueAllocation

class WelcomeController(BaseController):
    """The default Controller

    You could change the default route in main.py
    """
    def index(self):
        """The default method

        related to templates/welcome/index.html
        """
        pass
    
    def defence(self):
        s_vals = {
            'hp': int(self.params['s_vals_hp'] if len(self.params['s_vals_hp']) > 0 else 0),
            'b': int(self.params['s_vals_b'] if len(self.params['s_vals_b']) > 0 else 0),
            'd': int(self.params['s_vals_d'] if len(self.params['s_vals_d']) > 0 else 0),
        }
        p_vals = {
            'hp': int(self.params['p_vals_hp'] if len(self.params['p_vals_hp']) > 0 else 0),
            'b': int(self.params['p_vals_b'] if len(self.params['p_vals_b']) > 0 else 0),
            'd': int(self.params['p_vals_d'] if len(self.params['p_vals_d']) > 0 else 0),
        }
        adjustments = {
            'b': float(self.params['adjustments_b'] if len(self.params['adjustments_b']) > 0 else 0),
            'd': float(self.params['adjustments_d'] if len(self.params['adjustments_d']) > 0 else 0),
        }
        e_val = int(self.params['e_val'] if len(self.params['e_val']) > 0 else 0)
        self.best_base_pts = allocate_effort_value(s_vals, p_vals, adjustments, e_val)
        pass
    
    def damage_in(self):
        self.hp = int(self.params['hp'])
        self.b = int(self.params['b'])
        self.d = int(self.params['d'])
        
        pass
    
    def damage(self):
        atk = self.params['atk']
        dfc = 'b' if self.params['atk'] == 'a' else 'd'
        
        self.s_vals_a = int(self.params['s_vals_a']) if len(self.params['s_vals_a']) > 0 else 0
        self.s_vals_c = int(self.params['s_vals_c']) if len(self.params['s_vals_c']) > 0 else 0
        self.p_vals_a = int(self.params['p_vals_a']) if len(self.params['p_vals_a']) > 0 else 0
        self.p_vals_c = int(self.params['p_vals_c']) if len(self.params['p_vals_c']) > 0 else 0
        self.e_vals_a = int(self.params['e_vals_a']) if len(self.params['e_vals_a']) > 0 else 0
        self.e_vals_c = int(self.params['e_vals_c']) if len(self.params['e_vals_c']) > 0 else 0
        self.adjustments_a = float(self.params['adjustments_a'])
        self.adjustments_c = float(self.params['adjustments_c'])
        self.atk_params = {
            'a': common_parameter(self.s_vals_a, self.p_vals_a, self.e_vals_a, 50, self.adjustments_a),
            'c': common_parameter(self.s_vals_c, self.p_vals_c, self.e_vals_c, 50, self.adjustments_c),
        }
        self.dfc_params = {
            'hp': int(self.params['hp']),
            'b': int(self.params['b']),
            'd': int(self.params['d']),
        }
        
        type = float(self.params['type']) if 'type' in self.params else 1.0
        chemistry = float(self.params['chemistry'])
        hardrock = float(self.params['hardrock']) if chemistry > 1.0 else 1.0
        pow = int(self.params['pow']) if len(self.params['pow']) > 0 else 0
        
        self.max_damage = max_damage(50, pow, self.atk_params[atk], self.dfc_params[dfc])
        self.max_damage = int(self.max_damage * type)
        self.max_damage = int(self.max_damage * chemistry)
        self.max_damage = int(self.max_damage * hardrock)
        self.min_damage = min_damage(50, pow, self.atk_params[atk], self.dfc_params[dfc])
        self.min_damage = int(self.min_damage * type)
        self.min_damage = int(self.min_damage * chemistry)
        self.min_damage = int(self.min_damage * hardrock)
        
        self.max_dph = damage_per_hp(self.max_damage, self.dfc_params['hp'])
        self.min_dph = damage_per_hp(self.min_damage, self.dfc_params['hp'])
        
        # Pass for template that current values
        self.atk = self.params['atk']
        self.pow = pow
        self.type = type
        self.chemistry = float(self.params['chemistry'])
        self.hardrock = float(self.params['hardrock'])
        
        pass
    
    def speed(self):
        my = {
            's': int(self.params['my_s'] if len(self.params['my_s']) > 0 else 0),
            'p': int(self.params['my_p'] if len(self.params['my_p']) > 0 else 0),
            'e': 0,
            'lv': 50,
            'adj': float(self.params['my_adj']),
            'item': float(self.params['my_item']),
        }
        ur = {
            's': int(self.params['ur_s'] if len(self.params['ur_s']) > 0 else 0),
            'p': int(self.params['ur_p'] if len(self.params['ur_p']) > 0 else 0),
            'e': int(self.params['ur_e'] if len(self.params['ur_e']) > 0 else 0),
            'lv': 50,
            'adj': float(self.params['ur_adj']),
            'item': float(self.params['ur_item']),
        }
        self.best_base_pts = faster_than_that_speed(my, ur)
        self.my_speed = int(common_parameter(my['s'], my['p'], self.best_base_pts if self.best_base_pts >= 0 else 255, my['lv'], my['adj']))
        self.my_item_speed = int(self.my_speed * my['item'])
        self.ur_speed = int(common_parameter(ur['s'], ur['p'], ur['e'], ur['lv'], ur['adj']))
        self.ur_item_speed = int(self.ur_speed * ur['item'])
        
        pass
    
    def others(self):
        """ STATIC PAGES"""
        pass


def allocate_effort_value(s_vals, p_vals, adjustments, max_e = 510, lv = 50):
    assert 0 <= max_e <= 510
    assert 0 <= lv <= 100
    
    allocations = {
        'b': EffortValuesAllocation(), 
        'd': EffortValuesAllocation(), 
        'both': EffortValuesAllocation(),
    }
    
    """
    -1(assert), 0, 1, 255, 510, 511(assert)
    """
    def e_all_allocation(max_e):
        return [
            {
                'hp': e_hp,
                'b':  e_b,
                'd':  max_e - (e_hp + e_b),
            }
            for e_hp in range(252, -1, -4)
            for e_b in range(252, -1, -4)
            if 0 <= max_e - (e_hp + e_b) <= 255
        ]
    
    for e_vals in e_all_allocation(max_e):
        
        params = {
            'hp': hp_parameter(s_vals['hp'], p_vals['hp'], e_vals['hp'], lv),
            'b':  common_parameter(s_vals['b'], p_vals['b'], e_vals['b'], lv, adjustments['b']),
            'd':  common_parameter(s_vals['d'], p_vals['d'], e_vals['d'], lv, adjustments['d']),
        }
        threshold = math.floor(params['hp'] / 16)
        
        damages = {
            'b': max_damage(lv, 200, 150, params['b']),
            'd': max_damage(lv, 200, 150, params['d']),
        }
        
        defences = {
            'b': damage_per_hp(damages['b'], params['hp']),
            'd': damage_per_hp(damages['d'], params['hp']),
        }
        
        if(allocations['b'].isHarder(defences, damages, 'b')):
            allocations['b'].setAllocation(e_vals, defences, damages)
            allocations['b'].setParams(params)
        
        if(allocations['d'].isHarder(defences, damages, 'd')):
            allocations['d'].setAllocation(e_vals, defences, damages)
            allocations['d'].setParams(params)
        
        diff = abs(damages['b'] - damages['d'])
        if(diff <= threshold and allocations['both'].isHarder(defences, damages, 'both')):
            allocations['both'].setAllocation(e_vals, defences, damages)
            allocations['both'].setParams(params)
        
    
    return allocations

def faster_than_that_speed(my, ene):
    enemy_speed = math.floor(common_parameter(ene['s'], ene['p'], ene['e'], ene['lv'], ene['adj']) * ene['item'])
    my_speed = lambda e: math.floor(common_parameter(my['s'], my['p'], e, my['lv'], my['adj']) * my['item'])
    
    faster_es = [e for e in range(0, 256, 4) if my_speed(e) > enemy_speed]
    if faster_es == []:
        return -1
    else:
        return min(faster_es)

def common_parameter(species, personal, base, lv, adjustment):
    tmp1 = math.floor(species*2 + personal + math.floor(base / 4))
    tmp2 = math.floor(tmp1 * lv / 100) + 5
    return int(math.floor(tmp2 * adjustment))

def hp_parameter(species, personal, base, lv):
    tmp1 = math.floor(species*2 + personal + math.floor(base / 4))
    return int(math.floor(tmp1 * lv / 100) + 10 + lv)

def max_damage(atk_lv, skill_pow, atk_param, dfc_param):
    tmp1 = math.floor(atk_lv * 2 / 5 + 2)
    return int(math.floor(tmp1 * skill_pow * atk_param / dfc_param / 50 + 2))

def min_damage(atk_lv, skill_pow, atk_param, dfc_param):
    return int(math.floor(max_damage(atk_lv, skill_pow, atk_param, dfc_param) * 0.85))

def damage_per_hp(damage, hp):
    return  math.floor(float(damage) / float(hp) * 1000) / 10.0

