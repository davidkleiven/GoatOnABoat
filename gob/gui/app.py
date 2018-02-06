import pygame
from gob.city_image_question import CityImageQuestion
import random
from gob.player import Player
import gob.callbacks as cb
from gob.settings import GameMode

class App(object):
    def __init__( self ):
        self._running = True
        self._display_surf = None
        self.width = 640
        self.height = 400
        self.size = self.width,self.height
        self.question_types = [CityImageQuestion()]
        self.mode = GameMode.IDLE
        self.active_question = self.question_types[0]
        self.user_has_selected_alternative = False
        self.map = pygame.image.load( "data/holmen.png" )
        self.map = pygame.transform.scale( self.map, (int(self.width/2.0),self.height) )
        self.n_tiles = 10
        self.grid_color = (99,99,99)
        player_img = pygame.image.load( "data/empty_boat.png" )
        img_width = int(self.width/(2.0*self.n_tiles))
        img_height = int(self.height/self.n_tiles)
        player_img = pygame.transform.scale( player_img, (img_width,img_height) )
        self.players = [Player(name="Test player",img=player_img,n_tiles=self.n_tiles)]
        self.active_player = 0

        # Attach the callback on correct to each question
        for q in self.question_types:
            q.on_correct_cb = cb.OnCorrectDrawOptions(self)
            q.on_wrong_cb = cb.OnWrongAnswer(self)

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF )
        self._running = True
        pygame.font.init()
        self.draw_world()

    def tile_size(self):
        wx = self.width/(2.0*self.n_tiles)
        wy = self.height/self.n_tiles
        return wx,wy

    def draw_world(self):
        self._display_surf.blit( self.map, self.map.get_rect() )
        self.draw_grid()
        self.draw_players()
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

    def draw_players(self):
        for player in self.players:
            x,y = self.tile_to_pixel( (player.tile_x,player.tile_y) )
            rect = player.img.get_rect()
            rect[0] += x
            rect[1] += y
            self._display_surf.blit( player.img, rect )
        pygame.display.flip()

    def ask_question( self ):
        """
        Generates a new question
        """
        self.active_question = self.question_types[random.randint(0,len(self.question_types)-1)]
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
                else:
                    return # Return if the pressed key is not a,w,s,d
                self.draw_world()
                self.next_player()

    def next_player(self):
        self.active_player += 1
        if ( self.active_player >= len(self.players) ):
            self.active_player = 0
        self.mode = GameMode.IDLE

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
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
