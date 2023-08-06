import unittest
from gym_plannable.env.tic_tac_toe import TicTacToeEnv
from plannable_mixins import PlannableInterfaceTestMixin, PlannableEnvTestMixin

class PlannableInterfaceTestTicTacToe(PlannableInterfaceTestMixin, unittest.TestCase):
    env_constructor = TicTacToeEnv
    max_next = 5

class PlannableEnvTestTicTacToe(PlannableEnvTestMixin, unittest.TestCase):
    env_constructor = TicTacToeEnv
