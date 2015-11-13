from Environment import Environment

from unittest import TestCase
from Parser import Parser
from TypeChecker import TypeChecker

class CommonTest(TestCase):

    def testFirstFunctionApplyBug(self):
        (definitions, errors) = Parser().parse("""
            //def bug(x) = get([x], 0)
            def test(x) = [x]
            def test2(x) = test(x)
            def test3(x) = get(test(x), 0)
            """)
        env = Environment()
        type1 = TypeChecker().check(errors, env, definitions[0])
        type2 = TypeChecker().check(errors, env, definitions[1])
        type3 = TypeChecker().check(errors, env, definitions[2])

        self.assertEqual(errors, [])
        self.assertEqual(str(type1), "a -> [a]")
        self.assertEqual(str(type2), "a -> [a]")
        self.assertEqual(str(type3), "a -> a")


