from question import Question
import settings
import random
import numpy as np

def load_city_file():
    info = []
    with open( settings.city_coordinate_file,'r' ) as infile:
        for line in infile.readlines():
            splitted = line.split(",")
            new_entry = {
                "country":splitted[0].rstrip(),
                "capital":splitted[1].rstrip(),
                "latitude":splitted[2].rstrip(),
                "longitude":splitted[3].rstrip()
            }
            info.append(new_entry)
            print (new_entry)
    return info

class CapitalCountry( Question ):
    def __init__( self ):
        Question.__init__( self )
        self.info = load_city_file()

    def get( self ):
        random.shuffle(self.info)
        text = "Capital of {}?".format( self.info[0]["country"] )
        alternatives = []
        for i in range(4):
            alternatives.append( self.info[i]["capital"] )
        return text,alternatives

class CapitalCoordinates( Question ):
    def __init__( self ):
        Question.__init__(self)
        self.info = load_city_file()

    def get( self ):
        random.shuffle(self.info)
        text = "Location of {}?".format( self.info[0]["capital"] )
        alternatives = []
        for i in range(4):
            alt = "{},{}".format( self.info[i]["latitude"], self.info[i]["longitude"] )
            alternatives.append( alt )
        return text, alternatives

class CapitalDistances( Question ):
    def __init__( self ):
        Question.__init__(self)
        self.info = load_city_file()
        self.earth_radius = 6371 # km

    def coordinate_string_to_list( self, info_entry ):
        lat = int( info_entry["latitude"][:-1] )
        lng = int( info_entry["longitude"][:-1] )
        return lat,lng

    def distance( self, first, second ):
        """
        Distance in kilometers between two points
        https://www.movable-type.co.uk/scripts/latlong.html
        """

        first[0] *= np.pi/180.0
        first[1] *= np.pi/180.0
        second[0] *= np.pi/180.0
        second[1] *= np.pi/180.0

        dphi = second[0]-first[0]
        d_lambda = second[1]-first[0]
        a = np.sin( 0.5*dphi )**2 + np.cos(first[0])*np.cos(second[0])*np.sin( 0.5*d_lambda )**2
        c = np.arctan2( np.sqrt(a), np.sqrt(1.0-a) )
        return self.earth_radius*c

    def get(self):
        random.shuffle( self.info )
        text = "Distance between {} and {}".format( self.info[0]["capital"], self.info[1]["capital"] )

        first_crd = self.coordinate_string_to_list( self.info[0] )
        second_crd = self.coordinate_string_to_list( self.info[1] )
