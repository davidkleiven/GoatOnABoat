import pygame as pg
from gob.fishing_trick import FishingTrick

class DirtyTricksMenu(object):
    def __init__( self, app ):
        self.available_tricks = [FishingTrick(app)]
        self.app = app

    def dirty_trick_keys(self):
        return [trick.key for trick in self.available_tricks]

    def show( self ):
        color = (255,255,255)
        x0 = self.app.get_start_of_info_screen()
        y0 = 40
        delta = 30
        font = pg.font.SysFont( "Comic Sans MS", 30 )
        screen = self.app._display_surf
        text = "Dirty tricks menu"
        text = font.render( text, False, color )
        screen.blit( text, (x0,y0))
        counter = 1
        for trick in self.available_tricks:
            text = "{}: {}. {}p".format(trick.key, trick.info, trick.cost)
            text = font.render( text, False, color )
            y = y0+counter*delta
            counter += 1
            screen.blit( text, (x0,y) )

        pg.display.flip()
