import pygame as pg
from gob.settings import GameMode

class OnCorrectDrawOptions(object):
    def __init__( self, app ):
        self.app = app

    def can_move( self, new_tile ):
        uid = self.app.tile_id( new_tile )
        return not uid in self.app.disabled_tiles

    def __call__(self):
        """
        Draw letters and change the game mode to wait
        for user response to move boat
        """
        tile_x = self.app.players[self.app.active_player].tile_x
        tile_y = self.app.players[self.app.active_player].tile_y
        self.app.players[self.app.active_player].points += 1
        n_tiles = self.app.n_tiles
        font = pg.font.SysFont( "Comic Sans MS", 30 )
        color = (0,0,0)
        tile_size = self.app.tile_size()
        if ( (tile_y > 0) and self.can_move( (tile_x,tile_y-1)) ):
            pos_x, pos_y = self.app.tile_to_pixel( (tile_x,tile_y-1) )
            pos_x += tile_size[0]/2.0
            pos_y += tile_size[1]/2.0
            text = font.render( "W", False, color )
            self.app._display_surf.blit(text,(pos_x,pos_y))
        if ( (tile_y < self.app.n_tiles-1) and self.can_move( (tile_x,tile_y+1)) ):
            pos_x, pos_y = self.app.tile_to_pixel( (tile_x,tile_y+1) )
            pos_x += tile_size[0]/2.0
            pos_y += tile_size[1]/2.0
            text = font.render( "S", False, color )
            self.app._display_surf.blit(text,(pos_x,pos_y))
        if ( (tile_x > 0) and self.can_move( (tile_x-1,tile_y)) ):
            pos_x, pos_y = self.app.tile_to_pixel( (tile_x-1,tile_y) )
            pos_x += tile_size[0]/2.0
            pos_y += tile_size[1]/2.0
            text = font.render( "A", False, color )
            self.app._display_surf.blit(text,(pos_x,pos_y))
        if ( (tile_x < n_tiles-1) and self.can_move( (tile_x+1,tile_y)) ):
            pos_x, pos_y = self.app.tile_to_pixel( (tile_x+1,tile_y) )
            pos_x += tile_size[0]/2.0
            pos_y += tile_size[1]/2.0
            text = font.render( "D", False, color )
            self.app._display_surf.blit(text,(pos_x,pos_y))
        self.app.mode = GameMode.WAIT_FOR_USER_MOVE_BOAT
        pg.display.flip()

class OnWrongAnswer(object):
    def __init__( self, app ):
        self.app = app

    def __call__(self):
        self.app.next_player()
