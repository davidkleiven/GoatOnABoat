import pygame as pg
from settings import GameMode
from dirtyTrick import DirtyTrick
import numpy as np
import time

possible = [pg.K_1,pg.K_2,pg.K_3,pg.K_4,pg.K_5,pg.K_6,pg.K_7,pg.K_8,pg.K_9]

class FishingTrick( DirtyTrick ):
    """
    A user can throw a fishing crook to one of the other players boats
    and pull. The two players end up at their center of mass
    """
    def __init__( self, app ):
        DirtyTrick.__init__( self, key="F", info="Kast kroken etter motstander", cost=2 )
        self.app = app
        self.selected_player = 0
        self.neutral_color = (254,217,166)
        self.selected_color = (255,127,0)
        self.players = []
        for i,player in enumerate(self.app.players):
            if ( i == self.app.active_player ):
                continue
            self.players.append(player)

    def update_game_mode(self):
        self.app.mode = GameMode.WAIT_FOR_FISHING_RESPONS

    def draw_player_list( self ):
        """
        Draw the list of players
        """
        length_of_list = len(self.players)
        font = pg.font.SysFont( "Comic Sans MS", 30 )
        x0 = self.app.get_start_of_info_screen()
        y0 = 20
        delta = (self.app.height-y0)/length_of_list
        colors = [self.neutral_color for _ in range(length_of_list)]
        colors[self.selected_player] = self.selected_color
        screen = self.app._display_surf
        width = self.app.width-x0
        for indx,player in enumerate( self.players ):
            y = int(y0+indx*delta)
            pg.draw.rect( screen, colors[indx], [x0,y,width,20] )
            text = font.render( "{}: {}".format(indx+1,player.name), False, (0,0,0) )
            screen.blit( text, (x0+4,y) )

    def highlight_tile_of_selected_player(self):
        """
        Highlight the tile of the selected player
        """
        tile_x = self.players[self.selected_player].tile_x
        tile_y = self.players[self.selected_player].tile_y
        tile = (tile_x,tile_y)
        self.app.color_tile(tile,self.selected_color)
        self.app.draw_players()

    def get_accepted_selection_events(self):
        return [possible[i] for i in range(len(self.players))]

    def set_selected( self, pg_key ):
        found_selected_player = False
        for i in range( len(possible) ):
            if ( pg_key == possible[i] ):
                self.selected_player = i
                found_selected_player = True
                break
        if ( not found_selected_player ):
            raise RuntimeError( "Did not manage to figure out which player that was selected!" )

    def get_disabled_tiles( self ):
        """
        Returns a list with disabled tiles
        """
        disabled_tiles = [tile for tile in self.app.disabled_tiles]
        disabled_tiles += [tile for tile in self.app.pickup_tiles]
        disabled_tiles += [tile for tile in self.delivery_tiles]
        players_occupy = self.app.tiles_occupied_by_players()

        active_player = self.app.players[self.app.active_player]
        tile_active = self.app.tile_id( (active_player.tile_x,active_player.tile_y) )
        selected_player = self.players[self.selected_player]
        tile_selected = self.app.tile_id( (selected_player.tile_x,selected_player.tile_y) )
        for uid in players_occupy:
            if ( uid == tile_active or uid == tile_selected ):
                continue
            disabled_tiles += uid
        return disabled_tiles

    def show_options( self ):
        self.draw_player_list()
        self.highlight_tile_of_selected_player()
        pg.display.flip()

    def run_animation(self):
        """
        Run an animation showing the effect of the trick
        """
        # Update the points of a player
        active_player = self.app.players[self.app.active_player]
        if ( active_player.points < self.cost ):
            active_player.points = 0

            # You have to few points to afford this trick.
            # All other players gets points
            for i,player in enumerate(self.app.players):
                if ( i == self.app.active_player ):
                    continue
                player.points += self.cost
        else:
            active_player.points -= self.cost

        v = 30 # px per frame
        dt = 0.1 # Second
        executor = self.app.players[self.app.active_player]
        victim = self.players[self.selected_player]
        x0 = executor.tile_x
        y0 = executor.tile_y
        x1 = victim.tile_x
        y1 = victim.tile_y

        tsize = self.app.tile_size()
        x0,y0 = self.app.tile_to_pixel( (x0,y0) )
        x1,y1 = self.app.tile_to_pixel( (x1,y1) )
        x0 += tsize[0]/2.0
        y0 += tsize[1]/2.0
        x1 += tsize[0]/2.0
        y1 += tsize[1]/2.0

        r = np.sqrt( (x1-x0)**2 + (y1-y0)**2 )
        vx = v*(x1-x0)/r
        vy = v*(y1-y0)/r
        t = 0.0
        tfinal = r/v
        line_start_x = x0
        line_start_y = y0
        screen = self.app._display_surf
        color = (100,100,100)
        lw = 12
        while( t < tfinal ):
            t += dt
            line_end_x = line_start_x+vx*dt
            line_end_y = line_start_y+vy*dt
            pg.draw.line( screen, color, (line_start_x,line_start_y), (line_end_x,line_end_y), lw )
            pg.display.flip()
            time.sleep(dt)
            line_start_x = line_end_x
            line_start_y = line_end_y

        time.sleep(1) # Sleep for 1 second
        # Swap the positions
        active_player = self.app.players[self.app.active_player]
        selected_player = self.players[self.selected_player]

        tile_x = active_player.tile_x
        tile_y = active_player.tile_y
        active_player.tile_x = selected_player.tile_x
        active_player.tile_y = selected_player.tile_y
        selected_player.tile_x = tile_x
        selected_player.tile_y = tile_y
