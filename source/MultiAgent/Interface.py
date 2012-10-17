# Assignment:   Multi Agent Planning and Learning
# Course:       Autonomous Agents 2012-2013
# Education:    Master Artificial Intelligence
# By:           Steven Laan
#               Auke Wiggers
#               Camiel Verschoor
#
# File:         interface.py
# Description:  This class is a Graphical Interface for visualizing the grid.
import pygame
from pygame.locals import *
from Environment import Environment

class Interface():
    ''' Graphical Interface for displaying the environment '''

    # Constructor
    def __init__( self, size = (11, 11), predators = 2 ):
        ''' Constructor for setting up the GUI '''
        pygame.init()
        
        # Clock init
        self.clock = pygame.time.Clock()

        # Environment
        self.E = Environment( numberOfPredators=predators )
        self.E.qLearning( 10000 )
        self.E.resetAgents()

        # Setup the main screen
        self.size = size
        self.offset = 100
        self.half_offset = 50
        self.resolution = ( self.offset + size[0] * 50, \
                            self.offset + size[1] * 50 )
        self.screen = pygame.display.set_mode( self.resolution )
        pygame.display.set_caption( 'Autonomous Agents: Predators vs. Prey' )

        # Setup the background
        self.background = pygame.Surface( self.screen.get_size() )
        self.background = self.background.convert()
        self.background.fill( (255, 255, 255) )
        self.__drawBoard()

        # Prey sprite
        self.Prey = pygame.image.load( "../images/prey.png" ).convert()
        self.Prey_rect = self.Prey.get_rect()
        x, y = self.E.Prey.location
        self.Prey_rect.left = (self.half_offset) + (x * 51) + 1
        self.Prey_rect.top  = (self.half_offset) + (y * 51) + 1
        
        self.Predators      = list()
        self.Predators_rect = list()

        # Predator sprite
        for i in range(self.E.numberOfPredators):
            self.Predators.append( pygame.image.load( "../images/predator.png" ).convert() )
            x, y = self.E.Predators[i].location
            self.Predators_rect.append( self.Predators[i].get_rect() )
            self.Predators_rect[i].left = (self.half_offset) + (x * 51) + 1
            self.Predators_rect[i].top  = (self.half_offset) + (y * 51) + 1

        # Setup music
        pygame.mixer.music.load( "../music/BennyHillShow.mp3" )


    def __del__( self ):
        pygame.quit()

    def __drawBoard( self ):
        ''' Draws the board '''
        for i in range( self.size[0] + 1 ):
            pygame.draw.line( self.background, (0, 0, 0), ( self.half_offset, self.half_offset + i * 51), ( self.half_offset + self.size[1] * 51, self.half_offset + i * 51) )
        for i in range( self.size[1] + 1 ):
            pygame.draw.line( self.background, (0, 0, 0), ( self.half_offset + i * 51, self.half_offset), ( self.offset /2 + i * 51, self.half_offset + self.size[0] * 51) )

    def __update( self ):
        ''' Updates the location of the predator and the prey on the screen '''
        # Create new frame
        frame = self.background.copy()
        frame.blit( self.Prey, self.Prey_rect )
        for i in range( self.E.numberOfPredators ):
            frame.blit( self.Predators[i], self.Predators_rect[i] )
        
        # Display frame
        self.screen.blit( frame, (0, 0) )
        pygame.display.flip()

    def setPredator( self, i, location ):
        ''' Sets the predator location on the screen '''
        self.Predators_rect[i].left = (self.half_offset) + ( (location[0] % self.size[0] ) * 51) + 1
        self.Predators_rect[i].top  = (self.half_offset) + ( (location[1] % self.size[1] ) * 51) + 1

    def setPrey( self, location ):
        ''' Sets the prey location on the screen '''
        self.Prey_rect.left = (self.half_offset) + ( (location[0] % self.size[0]) * 51) + 1
        self.Prey_rect.top  = (self.half_offset) + ( (location[1] % self.size[1]) * 51) + 1

    def run( self ):
        ''' Updates the screen and checks for quit events '''
        done = False
        running = True
        start = True
        pygame.mixer.music.play(-1)
        frame = 0
 
        print "Start simulation"
        while not(done):
            pygame.image.save( self.screen, "frame{0}.jpg".format( frame ) )
            frame += 1

            # Run a step
            if running:
                self.E.simulateEnvironment()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    break
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.E.resetAgents()
                    running = True

            for i in range( self.E.numberOfPredators ):
                self.setPredator( i, self.E.Predators[i].location )
            self.setPrey( self.E.Prey.location )
            self.__update()
            self.clock.tick(10)

            for i in range( self.E.numberOfPredators ):
                if self.E.Predators[i].location == self.E.Prey.location:
                    running = False

if __name__ == '__main__':
    GUI = Interface()
    GUI.run()
