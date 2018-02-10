from question import QuestionWithImage
import settings
import requests
import random
from bs4 import BeautifulSoup
import wget
import re

class FamousNorwegians( QuestionWithImage ):
    def __init__( self ):
        QuestionWithImage.__init__(self)
        self.names =[]
        with open( settings.famous_norw_file , 'r' ) as infile:
            for line in infile.readlines():
                line = line.decode("utf8")
                line = line.replace(","," ")
                self.names.append( line.rstrip() )

    def get_url( self, name ):
        search = name.replace(" ", "_" )
        url = "https://en.wikipedia.org/wiki/"+search
        return url

    def get( self ):
        random.shuffle( self.names )
        url = self.get_url(self.names[0])
        res = requests.get( url )
        soup = BeautifulSoup( res.text )
        res = soup.findAll( "table", {"class":re.compile("infobox*")})
        if ( len(res) == 0 ):
            raise ValueError( "No infobox on wikipedia page!" )
        #soup = BeautifulSoup( res[0] )
        imgs = res[0].findAll( "a", {"class":"image"} )
        link = imgs[0].img["src"]

        # Find extension in string
        extensions = ["jpg","png"]
        ext_found = False
        for ext in extensions:
            pos = link.find(ext)
            if ( pos != -1 ):
                ext_found = True
                link = link[:pos]+ext
                break
        if ( not ext_found ):
            raise ValueError( "Could not one of the file extensions {}".format(extensions) )

        splitted_link = link.split("/")
        if ( "thumb" in splitted_link ):
            # Remove the thumb
            indx = splitted_link.index("thumb")
            del splitted_link[indx]
        link = ""
        for token in splitted_link:
            link += token+"/"
        link = link[:-1] # Remove the last backslash
        link = "https:"+link
        fname = link.split("/")[-1]
        self.image_name = "tmp/"+fname
        wget.download( link, out=self.image_name )
        text = "Hvilken norsk kjendis?"
        return text, self.names[:4]
