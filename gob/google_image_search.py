import selenium as sl
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import json

class GoogleImageSearch(object):
    def __init__( self ):
        self.home = "https://www.google.no/imghp?hl=en&tab=wi"
        self.driver = sl.webdriver.Chrome()
        self.image_extensions = ["jpg","png","jpeg"]

    def search( self, query ):
        """
        Performs a google search after the selected image
        """
        self.driver.get( self.home )
        search_field = self.driver.find_element_by_id( "lst-ib" )
        search_field.send_keys( query )
        search_field.send_keys( Keys.ENTER )
        html = self.driver.page_source
        soup = BeautifulSoup(html)
        return soup

    def get_first_image( self, query ):
        soup = self.search( query )
        imgs = soup.findAll( "div", {"class":"rg_meta notranslate"})
        link = json.loads(imgs[0].text)["ou"]
        found_ext = False
        for ext in self.image_extensions:
            pos = link.find(ext)
            if ( pos != -1 ):
                link = link[:pos]+ext
                found_ext = True
                break
        if ( not found_ext ):
            raise RuntimeError( "Did not recognize image!" )
        print (link)
        return link
