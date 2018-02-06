import pygame
from gob.city_image_question import CityImageQuestion
import random
from enum import Enum

class GameMode(Enum):
    IDLE = 0
    WAIT_FOR_USER_RESPONS = 1


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

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        pygame.font.init()
        self.draw_world()

    def draw_world(self):
        self._display_surf.blit( self.map, self.map.get_rect() )
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

        if ( self.mode == GameMode.WAIT_FOR_USER_RESPONS ):
            if ( event.type == pygame.KEYDOWN ):
                if ( event.key == pygame.K_a or event.key == pygame.K_b or \
                     event.key == pygame.K_c or event.key == pygame.K_d ):
                     self.active_question.highlight_selected( self._display_surf, event.key)
                     self.user_has_selected_alternative = True
                elif ( event.key == pygame.K_RETURN ):
                    self.active_question.check_answer(self._display_surf)
                    self.mode = GameMode.IDLE

        elif ( event.type == pygame.KEYDOWN ):
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
