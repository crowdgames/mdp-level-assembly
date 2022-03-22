import unittest
from Utility.RewardType import *

class TestRewardType(unittest.TestCase):
    def test_reward_type_to_str(self):
        self.assertEqual('DESIGNER', reward_type_to_str(RewardType.DESIGNER))
        self.assertEqual('PLAYER', reward_type_to_str(RewardType.PLAYER))
        self.assertEqual('BOTH', reward_type_to_str(RewardType.BOTH))

    def test_get_reward(self):
        self.assertEqual(10, get_reward(RewardType.DESIGNER, 10, -4))
        self.assertEqual(-4, get_reward(RewardType.PLAYER, 10, -4))
        self.assertEqual(6, get_reward(RewardType.BOTH, 10, -4))
        self.assertEqual(10, get_reward(RewardType.BOTH, 5, 5))
