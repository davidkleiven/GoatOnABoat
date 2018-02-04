from question import QuestionWithImage
import settings
from bs4 import BeautifulSoup
import requests
import os
import random
import shutil
import wget

class CityImageQuestion(QuestionWithImage):
    def __init__( self ):
        QuestionWithImage.__init__(self)
        self.fname = settings.city_file

        with open( self.fname, 'r' ) as infile:
            self.cities = infile.readlines()
        self.cities = [line.rstrip() for line in self.cities]
        self.url = "www.wikipedia.org"
        self.ignore = ["wik","padlock","static","flag_of","disambig","red_pog"]

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
        imgs = soup.find_all("div", {"class":"magnify"})
        ok = False
        accepted_extensions = ["jpg","png"]
        max_attempts = 10
        counter = 0
        # Select a random one
        while ( not ok and (counter < max_attempts) ):
            ok = True
            counter += 1
            tag = imgs[random.randint(0,len(imgs)-1)]
            soup = BeautifulSoup(str(tag))
            source = soup.find_all("a", href=True )[0]["href"]
            if ( not source[-3:] in accepted_extensions ):
                ok = False
                continue
            source = "https://en.wikipedia.org"+source

            splitted = source.split("/")
            imgname = splitted[-1].split(":")[-1]
            for phrase in self.ignore:
                if ( phrase in imgname.lower() ):
                    ok = False
                    break
            if ( not ok ):
                continue

            # Get the Wikipedia page where this image is shown in large
            res = requests.get(source)
            soup = BeautifulSoup(res.text)
            fname = source.split("/")[-1]
            images = soup.find_all("img")
            fname = fname.replace(" ","_")
            for image in images:
                alt = image.get("alt")
                alt = alt.replace(" ","_")
                if ( alt == fname ):
                    tag = image
                    break
            url = "https:"+tag.get("src")
            self.image_name = "tmp/%s"%(imgname)
            wget.download( url, out=self.image_name)
            return

        if ( counter >= max_attempts ):
            raise RuntimeError( "Could not find any suited image!" )

    def get( self ):
        """
        Returns the question. And alternatives.
        The correct answer is the first alternative
        Overrides the parents implementation
        """
        # Shuffle the citynames
        random.shuffle(self.cities)
        self.get_image( self.cities[0] )
        question = "Which city?"
        return question,self.cities[:4]
