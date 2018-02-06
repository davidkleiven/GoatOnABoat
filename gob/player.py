import pygame as pg

class Player(object):
    def __init__( self, name="noname", img=None, n_tiles=0 ):
        self.name = name
        if ( img is None ):
            raise ValueError( "No image provided!" )
        self.img = img
        self.points = 0
        self.tile_x = 0
        self.tile_y = 0
        self.n_tiles = n_tiles

    def move( self, direction ):
        """
        Moves the player one tile up,down,left or right
        """
        known_directions = ["left","right","up","down"]
        if ( not direction in known_directions ):
            raise ValueError( "Unknown directoin!" )

        if ( direction == "up" ):
            if ( self.tile_y == 0 ):
                return
            else:
                self.tile_y -= 1
        elif ( direction == "down" ):
            if ( self.tile_y == self.n_tiles-1 ):
                return
            else:
                self.tile_y += 1
        elif ( direction == "left" ):
            if ( self.tile_x == 0 ):
                return
            else:
                self.tile_x -= 1
        elif ( direction == "right" ):
            if ( self.tile_x == self.n_tiles-1 ):
                return
            else:
                self.tile_x += 1
