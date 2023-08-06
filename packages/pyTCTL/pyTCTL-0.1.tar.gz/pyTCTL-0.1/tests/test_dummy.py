import unittest
import pytctl

class DummyTest(unittest.TestCase):
    
    def test_name(self):
        self.assertEqual(pytctl.name, "pyTCTL")