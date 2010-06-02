'''
Created on 18/gen/2010

@author: anonymous
'''

from level import Level

class RuleParserException(Exception):
    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return self.description

    def __str__(self):
        return self.description

class RuleParser(object):
    entities = ['empty', 'border']
    trans = dict()
    states = {'empty':['idle'], 'border':['idle']}

    def __init__(self):
        pass

    def parse(self, line):
        line = line.strip()
        level = Level()
        if line.startswith('entity'):
            cmd, entity = line.split(' ')
            level.execute_entity(entity)
            
        if line.startswith('state'):
            cmd, entity, state = line.split(' ')
            level.execute_state(entity, state)
            
        if line.startswith('on_event'):
            lvalue, rvalue = line.split(':')
            cmd, entity, event = lvalue.split(' ')
            commands = []
            curr_command, separator, rvalue = rvalue.partition(',')
            commands.append(curr_command)
            while separator==",":
                curr_command, separator, rvalue = rvalue.partition(',')
                commands.append(curr_command)
            level.execute_on_event(entity, event, commands)

        if line.startswith('trans'):
            firstpart, secondpart = line[6:].split(',')
            old_mapstatus = self.parse_mapstatus(firstpart.strip())
            new_mapstatus = self.parse_mapstatus(secondpart.strip())
            if old_mapstatus['c'][0] not in self.trans:
                self.trans[old_mapstatus['c'][0]] = list()
            self.trans[old_mapstatus['c'][0]].append((old_mapstatus, new_mapstatus))

    def parse_mapstatus(self, mapstatus_str):
        place = dict()
        tokens = mapstatus_str.split(' ')
        (entity, slash, state) = tokens.pop(0).partition('/')
        state =  state if state else 'idle'

        if not entity in self.entities:
            raise RuleParserException('Undefined entity %s' % entity)

        if not state in self.states[entity]:
            raise RuleParserException('Undefined state %s for entity %s' % (state, entity))

        place['c'] = (entity, state)
        while tokens:
            direction = tokens.pop(0)
            (entity, slash, state) = tokens.pop(0).partition('/')
            state =  state if state else 'idle'

            if not entity in self.entities:
                raise RuleParserException('Undefined entity %s' % entity)

            if not state in self.states[entity]:
                raise RuleParserException('Undefined state %s for entity %s' % (state, entity))

            place[direction] = (entity, state)

        return place

    def expand_mapstatus(self, mapstatus):
        final_entities = [] 
        for (position, entity) in mapstatus.items():
            if entity[0]=='any':
                for ent in self.entities:
                    final_entities.append((position,ent))
              
        
    def get_entities(self):
        return self.entities

    def get_trans(self):
        return self.trans

def parse_rule_file(filename):
    parser = RuleParser()
    rulefile = open(filename, 'r')
    for line in rulefile.readlines():
        parser.parse(line)
    return parser.get_entities(), parser.get_trans()
