# Assignment:   Single Agent Planning
# Course:       Autonomous Agents 2012-2013
# Education:    Master Artificial Intelligence
# By:           Steven Laan
#               Auke Wiggers
#               Camiel Verschoor
#
# File:         interface.py
# Description:  This class is a Graphical Interface for visualizing the grid.
import pygame, sys, time
from pygame.locals import * 
from EnvironmentReduced import EnvironmentReduced

class Interface():
    ''' Graphical Interface for displaying the environment '''

    # Constructor
    def __init__( self, size = (11, 11), s = (0, 0, 5, 5) ):
        ''' Constructor for setting up the GUI '''
        pygame.init()
        
        # Clock init
        self.clock = pygame.time.Clock()

        # Environment
        self.E = EnvironmentReduced()

        # Setup the main screen
        self.size = size
        self.offset = 100
        self.half_offset = 50
        self.quit = False
        self.again = False
        self.resolution = ( self.offset + size[0] * 50, \
                           self.offset + size[1] * 50 )
        self.screen = pygame.display.set_mode( self.resolution )
        pygame.display.set_caption( 'Autonomous Agents: Predator vs. Prey' )

        # Setup the background
        self.background = pygame.Surface( self.screen.get_size() )
        self.background = self.background.convert()
        self.background.fill( (255, 255, 255) )
        self.__drawBoard()

        # Predator sprite
        self.predator = pygame.image.load( "images/predator.png" ).convert()
        self.predator_rect = self.predator.get_rect()
        self.predator_rect.left = (self.half_offset) + (s[0] * 51) + 1
        self.predator_rect.top  = (self.half_offset) + (s[1] * 51) + 1

        # Prey sprite
        self.prey = pygame.image.load( "images/prey.png" ).convert()
        self.prey_rect = self.prey.get_rect()
        self.prey_rect.left = (self.half_offset) + (s[2] * 51) + 1
        self.prey_rect.top  = (self.half_offset) + (s[3] * 51) + 1

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
        frame.blit( self.predator, self.predator_rect )
        frame.blit( self.prey, self.prey_rect )

        # Display frame
        self.screen.blit( frame, (0, 0) )
        pygame.display.flip()

    def setPredator( self, location ):
        ''' Sets the predator location on the screen '''
        self.predator_rect.left = (self.half_offset) + ( (location[0] % self.size[0] ) * 51) + 1
        self.predator_rect.top  = (self.half_offset) + ( (location[1] % self.size[1] ) * 51) + 1

    def setPrey( self, location ):
        ''' Sets the prey location on the screen '''
        self.prey_rect.left = (self.half_offset) + ( (location[0] % self.size[0]) * 51) + 1
        self.prey_rect.top  = (self.half_offset) + ( (location[1] % self.size[1]) * 51) + 1

    def run( self ):
        ''' Updates the screen and checks for quit events '''
        self.E.valueIteration()
        done = False
        running = True
 
        print "Start simulation"
        while not(done):
            # Run a step
            if running:
                self.E.run()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    break
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.E.reset()
                    running = True

            self.setPredator( self.E.predator.location )
            self.setPrey( self.E.prey.location )
            self.__update()
            self.clock.tick(10)
            if self.E.predator.location == self.E.prey.location:
                running = False
