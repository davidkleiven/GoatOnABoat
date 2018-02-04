from question import Question
import settings

class CityImageQuestion(Question):
    def __init__( self ):
        self.fname = settings.city_file

        with open( self.fname, 'r' ) as infile:
            self.cities = infile.readlines()
        self.cities = [line.rstrip() for line in self.cities-]
