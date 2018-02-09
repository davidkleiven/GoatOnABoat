import pygame as pg

class Player(object):
    def __init__( self, app, name="noname", img=None ):
        self.name = name
        if ( img is None ):
            raise ValueError( "No image provided!" )
        self.img = img
        self.points = 0
        self.tile_x = 0
        self.tile_y = 0
        self.app = app
        self.n_tiles = self.app.n_tiles
        self.has_goat = False

    def allowed_move( self, new_tile ):
        uid = self.app.tile_id( new_tile )
        return not (uid in self.app.disabled_tiles)

    def move( self, direction ):
        """
        Moves the player one tile up,down,left or right
        """
        known_directions = ["left","right","up","down"]
        if ( not direction in known_directions ):
            raise ValueError( "Unknown directoin!" )

        if ( direction == "up" ):
            if ( (self.tile_y == 0) or not self.allowed_move((self.tile_x,self.tile_y-1)) ):
                return
            else:
                self.tile_y -= 1
        elif ( direction == "down" ):
            if ( (self.tile_y == self.n_tiles-1) or not self.allowed_move((self.tile_x,self.tile_y+1)) ):
                return
            else:
                self.tile_y += 1
        elif ( direction == "left" ):
            if ( (self.tile_x == 0) or not self.allowed_move( (self.tile_x-1,self.tile_y)) ):
                return
            else:
                self.tile_x -= 1
        elif ( direction == "right" ):
            if ( (self.tile_x == self.n_tiles-1) or not self.allowed_move( (self.tile_x+1,self.tile_y)) ):
                return
            else:
                self.tile_x += 1
