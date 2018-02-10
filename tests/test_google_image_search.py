import unittest
from gob.google_image_search import GoogleImageSearch

class TestGoogleImageSearch( unittest.TestCase ):
    def test_img_search_no_throw(self):
        no_throw = True
        try:
            searcher = GoogleImageSearch()
            searcher.search( "svane" )
            searcher.get_first_image( "stokkand" )
        except Exception as exc:
            print (str(exc))
            no_throw = False
        self.assertTrue( no_throw )

if __name__ == "__main__":
    unittest.main()
