import pygame
import copy
import random

class Question(object):
    """
    Base class for all questions
    """
    def __init__(self):
        self.text_color = (43,140,190)
        self.qbox_color = (251,180,174)
        self.neutral_alternative = (254,217,166)
        self.selected_alternative = (255,127,0)
        self.correct_answer = (77,175,74)
        self.wrong_answer = (228,26,28)
        self.font = None
        self.alternatives = []
        self.correct = ""
        self.current_selected = 0

    def check_answer( self ):
        pass

    def get( self ):
        raise NotImplementedError( "This function has to be implemented in derived classes!" )

    def draw( self ):
        raise NotImplementedError( "This function has to implemented in derived class!" )

class QuestionWithImage(Question):
    def __init__(self):
        Question.__init__(self)
        self.image_name = ""
        self.origin = None
        self.size = None
        self.alt_origin = None

    def draw_alternatives( self, screen, origin, size, alternatives, colors=None ):
        """
        Draw the alternatives
        """
        # Draw alternatives
        y0 = origin[1]
        delta = (size[1]-y0)/4.0
        letters = ["A","B","C","D"]
        if ( colors is None ):
            colors = [self.neutral_alternative for i in range(4)]
        for i in range(len(alternatives)):
            y = int(y0+i*delta)
            pygame.draw.rect( screen, colors[i], [origin[0],y,size[0],20] )
            alt = self.font.render( letters[i]+" "+self.alternatives[i], False, self.text_color )
            screen.blit(alt, (int(origin[0]+4), y))

    def highlight_selected( self, screen, key ):
        colors = [self.neutral_alternative for i in range(4)]
        if ( key == pygame.K_a ):
            colors[0] = self.selected_alternative
            self.current_selected = 0
        elif ( key == pygame.K_b ):
            colors[1] = self.selected_alternative
            self.current_selected = 1
        elif ( key == pygame.K_c ):
            colors[2] = self.selected_alternative
            self.current_selected = 2
        elif ( key == pygame.K_d ):
            colors[3] = self.selected_alternative
            self.current_selected = 3
        self.draw_alternatives( screen, self.alt_origin, self.size, self.alternatives, colors=colors )
        pygame.display.flip()

    def check_answer(self,screen):
        # Find the index of the correct answer
        correct_index = self.alternatives.index(self.correct)
        colors = [self.neutral_alternative for i in range(4)]
        colors[correct_index] = self.correct_answer
        if ( self.current_selected != correct_index ):
            colors[self.current_selected] = self.wrong_answer

        self.draw_alternatives( screen, self.alt_origin, self.size, self.alternatives, colors=colors )
        pygame.display.flip()


    def draw( self, screen, origin, size, text, alternatives, altcolor=None ):
        """
        Puts the question onto the screen
        """
        self.alternatives = alternatives
        self.correct = copy.deepcopy(alternatives[0])
        random.shuffle(self.alternatives) # Shuffle alternatives randomly
        self.size = size
        self.origin = origin

        if ( self.image_name == "" ):
            raise ValueError( "No image given!" )
        img = pygame.image.load(self.image_name)
        self.font = pygame.font.SysFont( "Comic Sans MS", 30 )

        # Draw rectangle behind the question text
        y_text = int(0.1*size[1])
        pygame.draw.rect( screen, self.qbox_color, [origin[0],y_text,size[0],20] )
        q_text = self.font.render(text, False, self.text_color )
        screen.blit( q_text, (int(origin[0]+4), y_text))

        self.alt_origin = [origin[0],int(0.5*size[1])]
        self.draw_alternatives( screen, self.alt_origin, size, alternatives, colors=altcolor )
        # Rescale the image
        ratio_h = 0.3*size[1]/img.get_height()
        new_width = img.get_width()*ratio_h
        img = pygame.transform.scale(img, (int(new_width),int(0.3*size[1]) ))

        img_width = img.get_width()
        x0 = origin[0]+size[0]/2.0-img_width/2.0
        screen.blit( img, (int(x0),int(0.2*size[1]) ) )
        pygame.display.flip()
