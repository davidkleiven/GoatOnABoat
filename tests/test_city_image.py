import unittest
from gob.city_image_question import CityImageQuestion

class TestCityImage(unittest.TestCase):
    def test_no_throw(self):
        no_throw = True
        try:
            cityQ = CityImageQuestion()
        except Exception as exc:
            print (str(exc))
            no_throw = False
        self.assertTrue( no_throw )

    def test_get_image(self):
        cityQ = CityImageQuestion()
        cityQ.get_image("London")

if __name__ == "__main__":
    unittest.main()
