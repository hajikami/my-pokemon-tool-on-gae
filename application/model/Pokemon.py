class Pokemon:
    speciesPoint = None
    personalPoint = None
    basePoint = None
    parameter = None

class ValidationBase:
    
    def isValidOrNone(self, p):
        return isValid(p) or isNone(p)
    
    def isNone(self, p):
        return p == None
    
    def isValid(self, p):
        return true

class ParameterBase(ValidationBase):
    hp = 0
    a = 0
    b = 0
    c = 0
    d = 0
    s = 0
    
    def __init__(self, hp, a, b, c, d, s):
        self.hp = hp
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
    

class BasePoint(ParameterBase):
    MIN_BASE_POINT = 0
    MAX_BASE_POINT = 255
    
    def __init__(self, hp, a, b, c, d, s):
        assert isValidOrNone(hp)
        assert isValidOrNone(a)
        assert isValidOrNone(b)
        assert isValidOrNone(c)
        assert isValidOrNone(d)
        assert isValidOrNone(e)
        
        ParameterBase(hp, a, b, c, d, s)
    
    """ @override """
    def isValid(self, p):
        return isinstanceof(p, int) and MIN_BASE_POINT <= p <= MAX_BASE_POINT

class SpeciesPoint(ParameterBase):
    def __init__(self, hp, a, b, c, d, s):
        ParameterBase(hp, a, b, c, d, s)

class Parameter(ParameterBase):
    def __init__(self, hp, a, b, c, d, s):
        ParameterBase(hp, a, b, c, d, s)
