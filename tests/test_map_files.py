import unittest
import glob
import json

class TestMapFiles( unittest.TestCase ):
    required_fields = ["img","disabled_tiles","delivery_tiles","pickup_tiles","n_tiles"]

    def test_all_map_files( self ):
        for fname in glob.glob("data/*.map.json" ):
            with open( fname, 'r' ) as infile:
                data = json.load( infile )
                for field in TestMapFiles.required_fields:
                    self.assertTrue( field in data.keys() )
