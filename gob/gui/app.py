import pygame
from gob.city_image_question import CityImageQuestion
import random
from gob.player import Player
import gob.callbacks as cb
from gob.settings import GameMode
import time
from gob.capital_question import CapitalCountry, CapitalCoordinates
from gob.bird_question import BirdQuestion
from gob.famous_norwegians import FamousNorwegians
import numpy as np
import json
from gob import settings
import shutil

class App(object):
    def __init__( self, players=None ):
        self._running = True
        self._display_surf = None
        self.width = 1280
        self.height = 800
        self.size = self.width,self.height
        self.question_types = [CityImageQuestion(),CapitalCountry(),CapitalCoordinates(),BirdQuestion(),FamousNorwegians()]
        self.mode = GameMode.IDLE
        self.active_question = self.question_types[0]
        self.user_has_selected_alternative = False

        # Define variables that gets read from the map file
        self.map = None
        self.n_tiles = 1
        self.delivery_tiles = []
        self.pickup_tiles = []
        self.disabled_tiles = []
        self.load_map( "data/holmen_one_end.map.json" )

        # Define some colors
        self.grid_color = (99,99,99)
        self.pick_up_tile_color = (141,211,199)
        self.delivery_tile_color = (251,180,174)
        self.active_player_color = self.pick_up_tile_color

        player_img = pygame.image.load( "data/empty_boat.png" )
        img_width = int(self.width/(2.0*self.n_tiles))
        img_height = int(self.height/self.n_tiles)
        player_img = pygame.transform.scale( player_img, (img_width,img_height) )
        self.players = []
        if ( players is None ):
            self.players = [Player(self,name="Test player",img=player_img)]
        else:
            start_tile = 0
            pl_imgs = ["data/empty_boat.png","data/player2.png","data/player3.png","data/player4.png","data/player5.png"]
            for i,player in enumerate(players):
                player_img = pygame.image.load( pl_imgs[i%len(pl_imgs)] )
                img_width = int(self.width/(2.0*self.n_tiles))
                img_height = int(self.height/self.n_tiles)
                player_img = pygame.transform.scale( player_img, (img_width,img_height) )
                self.players.append( Player(self,name=player, img=player_img) )
                self.players[-1].tile_y = self.n_tiles-1
                self.players[-1].tile_x = start_tile
                start_tile += 1
        self.active_player = 0
        self.show_tile_ids = False
        self.points_per_goat = 10

        # Attach the callback on correct to each question
        for q in self.question_types:
            q.on_correct_cb = cb.OnCorrectDrawOptions(self)
            q.on_wrong_cb = cb.OnWrongAnswer(self)

        self.goat_delivered = cb.OnGoatDelivery(self)
        self.goat_picked_up = cb.OnGoatPickUp(self)
        self.active_dirty_trick = None

    def load_map( self, mapfile ):
        """
        Loads the map files
        """
        if ( not mapfile.endswith(".map.json") ):
            raise ValueError( "You have to provide a map file! (extension .map.json)" )

        with open( mapfile, 'r' ) as infile:
            data = json.load(infile)

        self.n_tiles = data["n_tiles"]
        self.disabled_tiles = data["disabled_tiles"]
        self.pickup_tiles = data["pickup_tiles"]
        self.delivery_tiles = data["delivery_tiles"]
        self.map = pygame.image.load( data["img"] )
        self.map = pygame.transform.scale( self.map, (int(self.width/2.0),self.height) )

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF )
        self._running = True
        pygame.font.init()
        pygame.display.set_caption( "Goat On A Boat" )
        self.draw_world()

    def tile_size(self):
        wx = self.width/(2.0*self.n_tiles)
        wy = self.height/self.n_tiles
        return wx,wy

    def tiles_occupied_by_players( self ):
        """
        Returns a list with the uids of the tils occupied by other players
        """
        uids = []
        for player in self.players:
            uids.append( self.tile_id((player.tile_x,player.tile_y)) )
        return uids

    def draw_world(self):
        self._display_surf.fill((0,0,0))
        self._display_surf.blit( self.map, self.map.get_rect() )
        #self.color_pickup_tiles()
        #self.color_deliver_tiles()
        self.draw_grid()
        self.draw_players()
        self.draw_score()
        if ( self.show_tile_ids ):
            self.draw_tile_ids()
        pygame.display.flip()

    def draw_grid(self):
        delta = self.width/(2.0*self.n_tiles)
        x = 0
        while( x < self.width/2.0 ):
            pygame.draw.line( self._display_surf, self.grid_color, (x,0), (x,self.height) )
            x += delta
        delta = self.height/self.n_tiles
        y = 0
        while ( y < self.height ):
            pygame.draw.line( self._display_surf, self.grid_color, (0,y),(int(self.width/2.0),y))
            y += delta

    def tile_to_pixel( self, tile_pos ):
        pix_per_tile_x = self.width/(2.0*self.n_tiles)
        pix_per_tile_y = self.height/self.n_tiles
        x = tile_pos[0]*pix_per_tile_x
        y = tile_pos[1]*pix_per_tile_y
        return x,y

    def pixel_to_tile( self, pixels ):
        pix_per_tile_x = self.width/(2.0*self.n_tiles)
        pix_per_tile_y = self.height/self.n_tiles
        tile_x = int( pixels[0]/pix_per_tile_x )
        tile_y = int( pixels[1](pix_per_tile_y) )
        return tile_x,tile_y

    def tile_id( self, tile_pos ):
        uid = tile_pos[0]*self.n_tiles + tile_pos[1]
        return uid

    def tile_from_uid( self, uid ):
        ty = uid%self.n_tiles
        tx = int(uid/self.n_tiles)
        return tx,ty

    def draw_tile_ids( self ):
        """
        Writes the UID of each tile on the screen.
        Used for debugging only
        """
        BLACK = (0,0,0)
        font = pygame.font.SysFont( "Comic Sans MS", 30 )
        for i in range(self.n_tiles):
            for j in range(self.n_tiles):
                x,y = self.tile_to_pixel( (i,j) )
                uid = self.tile_id( (i,j) )
                text = font.render( "{}".format(uid), False, BLACK )
                self._display_surf.blit(text,(x,y) )
        pygame.display.flip()

    def draw_players(self):
        # Highlight the tile of the active player
        act_player = self.players[self.active_player]
        tile_x = act_player.tile_x
        tile_y = act_player.tile_y
        self.color_tile( (tile_x,tile_y), self.active_player_color )
        for player in self.players:
            x,y = self.tile_to_pixel( (player.tile_x,player.tile_y) )
            rect = player.img.get_rect()
            rect[0] += x
            rect[1] += y
            self._display_surf.blit( player.img, rect )
        pygame.display.flip()

    def color_tile( self, tile, color ):
        """
        Color one tile
        """
        width,height = self.tile_size()
        x,y = self.tile_to_pixel(tile)
        rect = (x,y,width,height)
        pygame.draw.rect( self._display_surf, color, rect )

    def color_pickup_tiles(self):
        width,height = self.tile_size()
        for uid in self.pickup_tiles:
            tile = self.tile_from_uid(uid)
            x,y = self.tile_to_pixel(tile)
            rect = (x,y,width,height)
            pygame.draw.rect( self._display_surf, self.pick_up_tile_color, rect )

    def color_deliver_tiles(self):
        width,height = self.tile_size()
        for uid in self.delivery_tiles:
            tile = self.tile_from_uid(uid)
            x,y = self.tile_to_pixel(tile)
            rect = (x,y,width,height)
            pygame.draw.rect( self._display_surf, self.delivery_tile_color, rect )

    def ask_question( self ):
        """
        Generates a new question
        """
        qtype = np.random.randint(low=0,high=len(self.question_types))
        self.active_question = self.question_types[qtype]
        text, alternatives = self.active_question.get()
        self.active_question.draw( self._display_surf, (self.width*0.5,0.0), (self.width*0.5,self.height), text, alternatives )
        self.mode = GameMode.WAIT_FOR_USER_RESPONS

    def on_event(self, event):
        if (event.type == pygame.QUIT):
            self._running = False
        if ( self.mode == GameMode.IDLE ):
            if ( event.type == pygame.KEYDOWN ):
                if ( event.key == pygame.K_n ):
                    self._display_surf.fill((0,0,0))
                    self.draw_world()
                    max_tries = 100
                    managed_to_create_question = False
                    for i in range(max_tries):
                        try:
                            self.ask_question()
                            manage_to_create_question = True
                            break
                        except Exception as exc:
                            print (str(exc))
                            self._display_surf.fill((0,0,0))
                            self.draw_world()
                            pass
                    if ( not manage_to_create_question ):
                        raise RuntimeError( "Did not manage to create a new question in %d tries!"%(max_tries) )
                    self.user_has_selected_alternative = False

        if ( self.mode == GameMode.WAIT_FOR_USER_RESPONS ):
            if ( event.type == pygame.KEYDOWN ):
                if ( event.key == pygame.K_a or event.key == pygame.K_b or \
                     event.key == pygame.K_c or event.key == pygame.K_d ):
                     self.active_question.highlight_selected( self._display_surf, event.key)
                     self.user_has_selected_alternative = True
                elif ( event.key == pygame.K_RETURN ):
                    self.active_question.check_answer(self._display_surf)

        if ( self.mode == GameMode.WAIT_FOR_USER_MOVE_BOAT ):
            dirty_tricks_menu = self.active_question.on_correct_cb.dirty_tricks_menu.dirty_trick_keys()
            pg_list_menu = settings.str2pg_letters( dirty_tricks_menu )
            if ( event.type == pygame.KEYDOWN ):
                player = self.players[self.active_player]
                if ( event.key == pygame.K_w ):
                    player.move( "up" )
                elif ( event.key == pygame.K_s ):
                    player.move( "down" )
                elif ( event.key == pygame.K_d ):
                    player.move( "right" )
                elif ( event.key == pygame.K_a ):
                    player.move( "left" )
                elif( event.key in pg_list_menu ):
                    self.active_dirty_trick = self.active_question.on_correct_cb.get_dirty_trick( settings.pgkey2str(event.key) )
                    self.active_dirty_trick.update_game_mode()
                    self._display_surf.fill((0,0,0))
                    self.draw_world()

                    # Active dirty trick should now be an instance of FishingTrick
                    self.active_dirty_trick.show_options()
                    return
                else:
                    return # Return if the pressed key is not a,w,s,d

                self.draw_world()
                # Check if the player reached a goat delivery point
                tile_x = player.tile_x
                tile_y = player.tile_y
                uid = self.tile_id ((tile_x,tile_y) )
                if ( player.has_goat ):
                    if ( uid in self.delivery_tiles ):
                        self.goat_delivered()
                else:
                    if ( uid in self.pickup_tiles ):
                        self.goat_picked_up()
                self.next_player()

        if ( self.mode == GameMode.WAIT_FOR_FISHING_RESPONS ):
            if ( self.active_dirty_trick is None ):
                raise ValueError( "No active dirty trick set!" )
            self._display_surf.fill((0,0,0))
            self.draw_world()

            # Active dirty trick should now be an instance of FishingTrick
            self.active_dirty_trick.show_options()

            if ( event.type == pygame.KEYDOWN ):
                if ( event.key in self.active_dirty_trick.get_accepted_selection_events() ):
                    self.active_dirty_trick.set_selected( event.key )
                elif ( event.key == pygame.K_RETURN ):
                    self.active_dirty_trick.run_animation()
                    self.mode = GameMode.IDLE
                    self.draw_world()
                    self.next_player()
                    return

    def next_player(self):
        self.active_player += 1
        if ( self.active_player >= len(self.players) ):
            self.active_player = 0
        self.mode = GameMode.IDLE

    def draw_score(self):
        font = pygame.font.SysFont( "Comic Sans MS", 22 )
        score =""
        for i,player in enumerate(self.players):
            score += "%s:%d "%(player.name[0],player.points)
        text = font.render( score, False, (255,255,255) )
        x = int(self.width/2.0+4)
        y = 5
        self._display_surf.blit( text, (x,y) )
        y = 20
        active = "Player: {}".format(self.players[self.active_player].name)
        text = font.render( active, False, (255,255,255))
        self._display_surf.blit( text, (x,y) )
        pygame.display.flip()

    def get_start_of_info_screen( self ):
        """
        Returns x-coordinate of the start of the info screen
        """
        return int( self.width/2.0 )

    def on_loop(self):
        pass
    def on_render(self):
        pass
    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while( self._running ):
            time.sleep(0.5)
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def __del__( self ):
        """
        Clean up
        """
        shutil.rmtree("tmp")

if __name__ == "__main__":
    theApp = App()
    #theApp.show_tile_ids = True
    theApp.on_execute()
