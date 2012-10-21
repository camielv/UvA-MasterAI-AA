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
from TeamEnvironment import Environment

class Interface():
    ''' Graphical Interface for displaying the environment '''

    # Constructor
    def __init__( self, size = (11, 11), predators = 1, episodes = 1000 ):
        ''' Constructor for setting up the GUI '''
        pygame.init()
        
        # Clock init
        self.clock = pygame.time.Clock()

        # Environment
        print "Initializing the agents and environment, performing training."
        self.E        = Environment( numberOfPredators=predators )
        self.episodes = episodes

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
        self.Prey = pygame.image.load( "../../images/prey.png" ).convert()
        self.Prey_rect = self.Prey.get_rect()
        x, y = self.E.TeamPrey.Prey.location
        self.Prey_rect.left = (self.half_offset) + (x * 51) + 1
        self.Prey_rect.top  = (self.half_offset) + (y * 51) + 1
        
        self.Predator = pygame.image.load( "../../images/predator.png" ).convert()
        self.Predator_rect = self.Predator.get_rect()
        x, y = self.E.TeamPredator.Predator.location
        self.Predator_rect.left = (self.half_offset) + (x * 51) + 1
        self.Predator_rect.top  = (self.half_offset) + (y * 51) + 1
        # Setup music
        pygame.mixer.music.load( "../../music/BennyHillShow.mp3" )

        # Setup music
        pygame.mixer.music.load( "../../music/BennyHillShow.mp3" )

        # Setup screen
        self.__update()


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
        frame.blit( self.Predator, self.Predator_rect )
        
        # Display frame
        self.screen.blit( frame, (0, 0) )
        pygame.display.flip()

    def setPredator( self, location ):
        ''' Sets the predator location on the screen '''
        self.Predator_rect.left = (self.half_offset) + ( (location[0] % self.size[0] ) * 51) + 1
        self.Predator_rect.top  = (self.half_offset) + ( (location[1] % self.size[1] ) * 51) + 1

    def setPrey( self, location ):
        ''' Sets the prey location on the screen '''
        self.Prey_rect.left = (self.half_offset) + ( (location[0] % self.size[0]) * 51) + 1
        self.Prey_rect.top  = (self.half_offset) + ( (location[1] % self.size[1]) * 51) + 1

    def run( self ):
        ''' Updates the screen and checks for quit events '''
        done = False
        running = True
        start = True
        self.E.minimaxQLearning( self.episodes )
        pygame.mixer.music.play(-1)
 
        print "Start simulation"
        while not(done):
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

            self.setPredator( self.E.TeamPredator.Predator.location )
            self.setPrey( self.E.TeamPrey.Prey.location )
            self.__update()
            self.clock.tick(5)

            if self.E.TeamPredator.Predator.location == self.E.TeamPrey.Prey.location:
                running = False

if __name__ == '__main__':
    GUI = Interface()
    GUI.run()
