import pygame as pg
from gob.settings import GameMode
from gob.gui.dirty_tricks_menu import DirtyTricksMenu
import time

class OnCorrectDrawOptions(object):
    def __init__( self, app ):
        self.app = app
        self.dirty_tricks_menu = DirtyTricksMenu(app)

    def can_move( self, new_tile ):
        uid = self.app.tile_id( new_tile )
        return not uid in (self.app.disabled_tiles+self.app.tiles_occupied_by_players())

    def get_dirty_trick( self, key ):
        """
        Returns the dirty trick corresponding to the selection
        """
        for trick in self.dirty_tricks_menu.available_tricks:
            if ( trick.key == key ):
                trick.update()
                return trick
        raise ValueError( "No dirty trick corresponds to the selection!" )

    def __call__(self):
        """
        Draw letters and change the game mode to wait
        for user response to move boat
        """
        self.app.draw_world()
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
        self.dirty_tricks_menu.show()
        pg.display.flip()

class OnWrongAnswer(object):
    def __init__( self, app ):
        self.app = app

    def __call__(self):
        self.app.next_player()

class OnGoatDelivery(object):
    def __init__( self, app ):
        self.app = app

    def __call__( self ):
        player = self.app.players[self.app.active_player]
        player.points += self.app.points_per_goat
        message = "{} delivered a goat!".format( player.name )
        font = pg.font.SysFont( "Comic Sans MS", 48 )
        text = font.render( message, False, (228,26,28) )
        pos = (3,self.app.height/2.0)
        player.has_goat = False
        self.app._display_surf.blit( text, pos )
        pg.display.flip()
        time.sleep(2)

class OnGoatPickUp(object):
    def __init__( self, app ):
        self.app = app

    def __call__( self ):
        player = self.app.players[self.app.active_player]
        if ( player.has_goat ):
            return
        player.has_goat = True
        message = "{} picked up a new goat! Points: {}".format( player.name, player.points )
        font = pg.font.SysFont( "Comic Sans MS", 48 )
        text = font.render( message, False, (228,26,28) )
        pos = (3,self.app.height/2.0)
        self.app._display_surf.blit( text, pos )
        pg.display.flip()
        time.sleep(2)
