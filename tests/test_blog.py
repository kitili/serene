import unittest
from app.models import Posts


class TestModelPitch(unittest.TestCase):

    def SetUp(self):
      self.new_pitch = Posts( 'My new pitch', 'dreezy',  0, 0, 0)

    def test_instance(self):
        self.assertTrue(isinstance(self.new_pitch, Posts))