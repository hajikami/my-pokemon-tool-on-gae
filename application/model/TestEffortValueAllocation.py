import unittest
import EffortValueAllocation

class TestNewEffortValueAllocation(unittest.TestCase):
    
    def setUp(self):
        self.effortValueAllocation = EffortValueAllocation()
    
    def testEVals(self):
        for e_val in self.e_vals:
            assertEqual(e_val, 0)
    
    def testDefences(self):
        for defence in self.defences:
            assertEqual(defence, 1000.0)
    
    def testDamages(self):
        for damage in self.damages:
            assertEqual(damage, 1000)
    
    def testParams(self):
        for param in self.params:
            assertEqual(param, 0)
    
    
        