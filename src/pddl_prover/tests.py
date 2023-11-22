import unittest
from logic import *

class TestLogic(unittest.TestCase):
    def setUp(self):
        self.b0, self.b1, self.b2, self.b3, self.b4 = Constant(0), Constant(1), Constant(2), Constant(3), Constant(4)
        self.x, self.y = Variable('x'), Variable('y')

        self.kb = ({self.b0,self.b1,self.b2},{('ontable', (0,)), ('on',(1,0)), ('on', (2,1)), ('clear',(2,)), 
            ('handempty', tuple())})

        self.handempty = Predicate('handempty', 0)
        self.ontable = Predicate('ontable', 1)
        self.on = Predicate('on', 2)
        self.clear = Predicate('clear', 1)

        self.kb2 = (frozenset((self.b0,self.b1,self.b2,self.b3,self.b4)), frozenset(( ('on', (1,0)), ('on', (2,0)), ('on', (3,0)), ('on', (4,0)) )))

    def test_evaluation(self):
        self.assertEqual(self.handempty().evaluate(self.kb), True)
        self.assertEqual(self.ontable(self.x).evaluate(self.kb, {self.x:self.b0}), True)
        self.assertEqual(self.ontable(self.x).evaluate(self.kb, {self.x:self.b1}), False)
        self.assertEqual((self.x != self.y).evaluate(self.kb, {self.x:self.b1, self.y:self.b0}), True)
        self.assertEqual((self.ontable(self.b0) & self.on(self.b1, self.b0) & self.on(self.x,self.b1)).evaluate(self.kb, {self.x:self.b2}), True)
        self.assertEqual((self.ontable(self.b0) & self.on(self.b1, self.b0) & self.on(self.x,self.b1)).evaluate(self.kb, {self.x:self.b0}), False)
        self.assertEqual((self.ontable(self.b0) & self.on(self.b1, self.b0) | self.on(self.x,self.b1)).evaluate(self.kb, {self.x:self.b0}), True)
        self.assertEqual((~(self.ontable(self.b0) & self.on(self.b1, self.b0) | self.on(self.x,self.b1))).evaluate(self.kb, {self.x:self.b0}), False)

    def test_quantifiers(self):
        self.assertEqual(TE(self.x, self.on(self.x, self.b0)).evaluate(self.kb2), True)
        self.assertEqual(TE(self.x, self.on(self.x, self.b1)).evaluate(self.kb2), False)
        self.assertEqual(TE(self.y,TE(self.x, self.on(self.x, self.y) & (self.x == self.y))).evaluate(self.kb2), False)
        self.assertEqual(TE(self.y,TE(self.x, self.on(self.x, self.y) & (self.x != self.y))).evaluate(self.kb2), True)
        self.assertEqual(TE(self.y,TE(self.x, self.on(self.x, self.y))).evaluate(self.kb2), True)

    def test_count(self):
        self.assertEqual(Count( self.on(self.x,self.b0), self.x).evaluate(self.kb2)[0], 4)
        self.assertEqual(Count( self.on(self.x,self.b1), self.x).evaluate(self.kb2)[0], 0)
        self.assertEqual(Count( self.on(self.x,self.y) & (self.x!=self.y), self.x, self.y).evaluate(self.kb2)[0], 4)
        self.assertEqual(Count( FA(self.x, self.on(self.x,self.y) | (self.x==self.y)), self.y ).evaluate(self.kb2)[0], 1)

      
if __name__ == '__main__':
    unittest.main()