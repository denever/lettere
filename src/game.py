'''
Created on 17/gen/2010

@author: anonymous
'''

import pygame, sys,os
from pygame.locals import *
from gsl_parser import parse_gsl_file
# from emdl_parser import parse_emdl_file
# from rule_parser import parse_rule_file
from level import Level
from config import Config
from game_console import GameConsole
from patterns import Singleton

class Game(Singleton):
    def __init__(self):
        Singleton.__init__(self)
        self.init()
        
    def init(self):
        self.window = pygame.display.set_mode((640, 480))
        pygame.display.set_caption('Gnosis - Epiphany generator')
        self.screen = pygame.display.get_surface()
        pygame.font.init()
        pygame.mixer.init()
        self.debugfont = pygame.font.SysFont("Courier New", 9)
        self.show_states = False
        self.console = GameConsole(self.screen, self)

    def input(self, events):
        
        for event in events:
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYUP:
                if event.key == 275:
                    pass
                if event.key == 276:
                    pass
                if event.key == 273:
                    pass
                if event.key == 274:
                    pass
                if event.key == 282:
                    #F1
                    self.console.set_active()

    def trans_neighbours(self, neigh, trans_rules):
        new_neigh = dict()
        for trans_rule in trans_rules:
            if self.match_neighbours(neigh, trans_rule[0]):
                for (key, value) in trans_rule[1].items():
                    new_neigh[key]= value
                break
        return new_neigh
    
    def match_neighbours(self, neigh1, neigh2):
        set1 = set(neigh1.items())
        set2 = set(neigh2.items())
        return set2.issubset(set1)

    def start(self):
        level = Level()
        level.init()
        (entities, trans) = parse_gsl_file(Config.data_path+'/testfile.gsl')
        
        
#        parse_emdl_file(entities, Config.data_path+'/map/level10.map', level)
        
        
        while True:
            self.console.process_input()
            self.input(pygame.event.get())
            self.screen.fill((0, 0, 0))
            pygame.time.wait(100)
            level.update_on_events()
            level.update()
            
            level.draw(self.screen)
            
            if self.show_states == True:
                level.draw_debug(self.screen)
                
            self.console.draw()    


            #self.screen.blit(surface, (0, 0))
            pygame.display.flip()

    def toggle_states(self):
        self.show_states = not self.show_states

if __name__ == '__main__':
#    try:
        g = Game()
        g.start()
#    except Exception, e:
#        print e
#        sys.exit(0)
