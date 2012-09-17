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
    """ Graphical Interface for displaying the environment """

    # Constructor
    def __init__( self, size = (11, 11), prey = (0, 0), predator = (5, 5) ):
        Thread.__init__(self)
        pygame.init()

        # Setup the main screen
        self.size = size
        self.offset = 100
        self.refresh = 0.4
        self.resolution = ( self.offset + size[0] * 50, self.offset + size[1] * 50 )
        self.screen = pygame.display.set_mode( self.resolution )
        pygame.display.set_caption( 'Autonomous Agents: Predator vs. Prey' )

        # Setup the background
        self.background = pygame.Surface( self.screen.get_size() )
        self.background = self.background.convert()
        self.background.fill( (255, 255, 255) )
        self.__drawBoard()

        # Predator
        self.predator = pygame.image.load( "images/predator.png" ).convert()
        self.predator_rect = self.predator.get_rect()
        self.predator_rect.left = (self.offset / 2) + (predator[0] * 51) + 1
        self.predator_rect.top  = (self.offset / 2) + (predator[1] * 51) + 1

        # Prey
        self.prey = pygame.image.load( "images/prey.png" ).convert()
        self.prey_rect = self.prey.get_rect()
        self.prey_rect.left = (self.offset / 2) + (prey[0] * 51) + 1
        self.prey_rect.top  = (self.offset / 2) + (prey[1] * 51) + 1

    # Draws the board on the background
    def __drawBoard( self ):
        for i in range( self.size[0] + 1 ):
            pygame.draw.line( self.background, (0, 0, 0), ( self.offset / 2, self.offset / 2 + i * 51), ( self.offset / 2 + self.size[1] * 51, self.offset / 2 + i * 51) )
        for i in range( self.size[1] + 1 ):
            pygame.draw.line( self.background, (0, 0, 0), ( self.offset / 2 + i * 51, self.offset / 2), ( self.offset /2 + i * 51, self.offset / 2 + self.size[0] * 51) )

    # Updates the screen
    def __update( self ):
        # Create new frame
        frame = self.background.copy()
        frame.blit( self.predator, self.predator_rect )
        frame.blit( self.prey, self.prey_rect )

        # Display frame
        self.screen.blit( frame, (0, 0) )
        pygame.display.flip()

    # Sets the location of the predator
    def setPredator( self, location ):
        self.predator_rect.left = (self.offset / 2) + ( (location[0] % self.size[1] ) * 51) + 1
        self.predator_rect.top  = (self.offset / 2) + ( (location[1] % self.size[1] ) * 51) + 1
        time.sleep( self.refresh )

    # Sets the location of the prey
    def setPrey( self, location ):
        self.prey_rect.left = (self.offset / 2) + ( (location[0] % self.size[0]) * 51) + 1
        self.prey_rect.top  = (self.offset / 2) + ( (location[1] % self.size[1]) * 51) + 1
        time.sleep( self.refresh)

    # Thread function checks if screen is quitted and updates screen.
    def run( self ):
        while( 1 ):
            for e in pygame.event.get():
                if ( ( e.type == QUIT ) ):
                    sys.exit()
            self.__update()
            time.sleep( self.refresh / 2 )

# DEMONSTRATION
if( __name__ == '__main__' ):
    GUI = Interface( (11, 11), (0, 0), (5, 5) )
    GUI.start()

    # PATH
    for i in range( 22 ):
        GUI.setPrey( ( (0+i), 0) )
        GUI.setPredator( ( 5, (5+i) ) )

    # Wait for GUI to end
    GUI.join()