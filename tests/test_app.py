import unittest
from gob.gui.app import App

class TestApp( unittest.TestCase ):
    def test_consistent_special_tiles(self):
        app = App()

        for tile in app.disabled_tiles:
            self.assertFalse( tile in app.delivery_tiles )
            self.assertFalse( tile in app.pickup_tiles)
