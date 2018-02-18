from enum import Enum
import pygame as pg

class GameMode(Enum):
    IDLE = 0
    WAIT_FOR_USER_RESPONS = 1
    WAIT_FOR_USER_MOVE_BOAT = 2
    WAIT_FOR_FISHING_RESPONS = 3

city_file = "data/cities.txt"
city_coordinate_file = "data/city_coordinates.csv"
bird_file = "data/birds.txt"
famous_norw_file = "data/famous_norwegians.txt"

# List translating keys to pygamge enum values
pg_letters= {
    "A":pg.K_a,
    "B":pg.K_b,
    "C":pg.K_c,
    "D":pg.K_d,
    "E":pg.K_e,
    "F":pg.K_f,
    "G":pg.K_g,
    "H":pg.K_h,
    "J":pg.K_j,
    "K":pg.K_k,
    "L":pg.K_l,
    "M":pg.K_m,
    "N":pg.K_n,
    "O":pg.K_o,
    "P":pg.K_p,
    "Q":pg.K_q,
    "R":pg.K_r,
    "S":pg.K_s,
    "T":pg.K_t,
    "U":pg.K_u,
    "V":pg.K_v,
    "W":pg.K_w,
    "X":pg.K_x,
    "Y":pg.K_y,
    "Z":pg.K_z
}

def str2pg_letters( strlist ):
    pg_list = [pg_letters[letter] for letter in strlist]
    return pg_list

def pgkey2str( pg_key ):
    for key,value in pg_letters.iteritems():
        if ( value == pg_key ):
            return key
    raise ValueError( "No letter corresponds to this pygame Key!" )
