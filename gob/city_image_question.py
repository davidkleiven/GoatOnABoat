from question import Question
import settings
from bs4 import BeautifulSoup
import requests
import os
import random
import shutil

class CityImageQuestion(Question):
    def __init__( self ):
        self.fname = settings.city_file

        with open( self.fname, 'r' ) as infile:
            self.cities = infile.readlines()
        self.cities = [line.rstrip() for line in self.cities]
        self.url = "www.wikipedia.org"
        self.active_image_name = ""

        # Create tmp directory if it does not ecists
        try:
            os.stat("tmp")
        except:
            os.mkdir("tmp")

    def get_image(self,cityname):
        """
        Return a random image from the wikipedia site on the city
        """
        search = "https://en.wikipedia.org/wiki/%s"%(cityname)
        res = requests.get(search)
        soup = BeautifulSoup(res.text)
        tags = soup.find_all("img")

        # Select a random one
        tag = tags[random.randint(0,len(tags)-1)]
        source = tag.get("src")
        splitted = source.split("/")
        imgname = splitted[-1]

        res = requests.get( "https:"+source,stream=True)

        self.active_image_name = "tmp/%s"%(imgname)
        if ( res.status_code == 200 ):
            with open( self.active_image_name, 'wb' ) as outfile:
                res.raw.decode_content = True
                shutil.copyfileobj( res.raw, outfile )

    def get( self ):
        """
        Returns the question. And alternatives.
        The correct answer is the first alternative
        Overrides the parents implementation
        """
        # Shuffle the citynames
        random.shuffle(self.cities)
        self.get_image( self.cities[0] )
        question = "Which city do you associate with this image?"
        return question,self.cities[:4]
