'''
Created on 02/feb/2010

@author: anonymous
'''

from lib.pyconsole import Console
import sys
from level import Level


class GameConsole(Console):
    '''
    classdocs
    '''
    lastcmd = ""
    rect = ((0,0),(640,200))


    def __init__(self, screen, game):
        level = Level()
        functions={
          "put":level.execute_put,
          "move":level.execute_move,
          "play":level.execute_play,
          "add_score":level.execute_add_score,
          "set_map_author":level.execute_set_map_author,
          "get_map_author":level.execute_get_map_author,
          "set_map_title":level.execute_set_map_title,
          "get_map_title":level.execute_get_map_title,
          "set_minscore":level.execute_set_minscore,
          "get_minscore":level.execute_get_minscore,
          "set_maxtime":level.execute_set_maxtime,
          "get_maxtime":level.execute_get_maxtime,
          "destroy":level.execute_destroy,
          "check":level.execute_check_entity_on_map,
          "line":level.execute_line,
          "rect":level.execute_rect,
          "collide":level.check_collision,
          "entity":level.execute_entity,
          "state":level.execute_state,
          "change_state":level.execute_change_state,
          "on_event":level.execute_on_event,
          "toggle_states":game.toggle_states,
          "launch_event":level.launch_event,
        }
        key_calls={"d":sys.exit}
        vars={}
        syntax={}
        Console.__init__(self, screen, self.rect, functions, key_calls, vars, syntax)
        self.set_active(False)
