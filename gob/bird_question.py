from question import QuestionWithImage
import settings
import random
from bs4 import BeautifulSoup
import wget
import json
import requests
from google_image_search import GoogleImageSearch

class BirdQuestion( QuestionWithImage ):
    def __init__( self ):
        QuestionWithImage.__init__(self)
        self.birds = []
        with open( settings.bird_file, 'r' ) as infile:
            self.birds = [line.rstrip().decode("utf8").lower() for line in infile.readlines()]
        self.max_attempts = 40
        self.current_attempts = 0
        self.google_img = GoogleImageSearch()

    def get_url( self, bird_name ):
        url = "https://snl.no/"+bird_name
        return url

    def get( self ):
        try:
            random.shuffle( self.birds )
            res = requests.get( self.get_url(self.birds[0]) )
            soup = BeautifulSoup( res.text )
            question = "Hvilken fugl?"

            """
            # Get all images
            imgs = soup.findAll( "figure", {"class":"image landscape non-expandable published"} )
            imgs += soup.findAll( "figure", {"class":"image portrait non-expandable published"})
            link = imgs[0].img["src"]
            #link = json.loads( imgs[0].text )["ou"]
            fname = link.split("/")[-1]
            """
            link = self.google_img.get_first_image( self.birds[0] )
            fname = link.split("/")[-1]

            # Remove all percentages
            fname.replace("%","")
            self.image_name = "tmp/"+fname
            wget.download( link, out=self.image_name )

            alternatives = self.birds[:4]
            self.current_attempts = 0
            return question, alternatives
        except Exception as exc:
            print ("Bird question: "+str(exc) )
            self.current_attempts += 1
            if ( self.current_attempts < self.max_attempts ):
                self.get()
            else:
                raise RuntimeError( "Could not create bird question!" )
                self.current_attempts = 0
