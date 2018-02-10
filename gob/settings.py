from enum import Enum

class GameMode(Enum):
    IDLE = 0
    WAIT_FOR_USER_RESPONS = 1
    WAIT_FOR_USER_MOVE_BOAT = 2

city_file = "data/cities.txt"
city_coordinate_file = "data/city_coordinates.csv"
bird_file = "data/birds.txt"
