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
from threading import Thread
from pygame.locals import * 

class Interface( Thread ):
    ''' Graphical Interface for displaying the environment '''

    # Constructor
    def __init__( self, size = (11, 11), s = (0, 0, 5, 5) ):
        ''' Constructor for setting up the GUI '''
        Thread.__init__(self)
        pygame.init()

        # Setup the main screen
        self.size = size
        self.offset = 100
        self.refresh = 0.2
        self.quit = False
        self.again = False
        self.resolution = ( self.offset + size[0] * 50, self.offset + size[1] * 50 )
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
        self.predator_rect.left = (self.offset / 2) + (s[0] * 51) + 1
        self.predator_rect.top  = (self.offset / 2) + (s[1] * 51) + 1

        # Prey sprite
        self.prey = pygame.image.load( "images/prey.png" ).convert()
        self.prey_rect = self.prey.get_rect()
        self.prey_rect.left = (self.offset / 2) + (s[2] * 51) + 1
        self.prey_rect.top  = (self.offset / 2) + (s[3] * 51) + 1

    def __drawBoard( self ):
        ''' Draws the board '''
        for i in range( self.size[0] + 1 ):
            pygame.draw.line( self.background, (0, 0, 0), ( self.offset / 2, self.offset / 2 + i * 51), ( self.offset / 2 + self.size[1] * 51, self.offset / 2 + i * 51) )
        for i in range( self.size[1] + 1 ):
            pygame.draw.line( self.background, (0, 0, 0), ( self.offset / 2 + i * 51, self.offset / 2), ( self.offset /2 + i * 51, self.offset / 2 + self.size[0] * 51) )

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
        self.predator_rect.left = (self.offset / 2) + ( (location[0] % self.size[0] ) * 51) + 1
        self.predator_rect.top  = (self.offset / 2) + ( (location[1] % self.size[1] ) * 51) + 1
        time.sleep( self.refresh )

    def setPrey( self, location ):
        ''' Sets the prey location on the screen '''
        self.prey_rect.left = (self.offset / 2) + ( (location[0] % self.size[0]) * 51) + 1
        self.prey_rect.top  = (self.offset / 2) + ( (location[1] % self.size[1]) * 51) + 1
        time.sleep( self.refresh )

    def getStatus( self ):
        ''' Returns the state of the GUI, if quitted it returns True '''
        return self.quit

    def getReload( self ):
        again = self.again
        self.again = False
        return again

    def run( self ):
        ''' Updates the screen and checks for quit events '''
        while( 1 ):
            for e in pygame.event.get():
                if ( ( e.type == QUIT ) ):
                    self.quit = True
                    sys.exit()
                elif ( ( e.type == KEYDOWN ) and ( e.key == K_r ) ):
                    self.again = True

            self.__update()
            time.sleep( self.refresh / 2 )
