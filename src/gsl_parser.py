'''
Created on 18/gen/2010

@author: anonymous
'''

from level import Level

class GSLParserException(Exception):
    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return self.description

    def __str__(self):
        return self.description

class GSLParser(object):
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

        if line.startswith('set name'):
            level.execute_set_map_title(line[10:-2])

        if line.startswith('set author'):
            level.execute_set_map_author(line[12:-2])

        if line.startswith('set maxtime'):
            level.execute_set_maxtime(int(line[12:-1]))

        if line.startswith('set minscore'):
            level.execute_set_minscore(int(line[13:-1]))

        if line.startswith('get name'):
            level.execute_get_map_title()

        if line.startswith('get author'):
            level.execute_get_map_author()

        if line.startswith('get maxtime'):
            level.execute_get_maxtime()

        if line.startswith('get minscore'):
            level.execute_get_minscore()

        if line.startswith('put'):
            cmd, entity, pos = line.split(' ')
            y, x = eval(pos[1:-2])
            level.execute_put(entity, x, y)
        
        if line.startswith('line'):
            cmd, entity, pos = line.split(' ')
            if not entity in self.entities:
                return "Can't set unknown entity %s" % entity
            pos = pos.replace(')(',',')
            x1, y1, x2, y2 = eval(pos[1:-2])
            level.execute_line(entity, x1, y1, x2, y2)

        if line.startswith('rect'):
            cmd, entity, pos = line.split(' ')
            if not entity in self.entities:
                return "Can't set unknown entity %s" % entity
            pos = pos.replace(')(',',')
            x1, y1, height, width = eval(pos[1:-2])
            level.execute_rect(entity, x1, y1, height, width)

        if line.startswith('play'):
            cmd, space, args = line.partition(' ')
            level.execute_play(args)

        if line.startswith('move'):
            cmd, direction, n_pixels, entity_id = line.split(' ', 3)
            level.execute_move(int(entity_id), direction, int(n_pixels))

        if line.startswith('add_score'):
            cmd, n_scores = line.split(' ', 1)
            level.execute_add_score(int(n_scores))

    def parse_mapstatus(self, mapstatus_str):
        place = dict()
        tokens = mapstatus_str.split(' ')
        (entity, slash, state) = tokens.pop(0).partition('/')
        state =  state if state else 'idle'

        if not entity in self.entities:
            raise GSLParserException('Undefined entity %s' % entity)

        if not state in self.states[entity]:
            raise GSLParserException('Undefined state %s for entity %s' % (state, entity))

        place['c'] = (entity, state)
        while tokens:
            direction = tokens.pop(0)
            (entity, slash, state) = tokens.pop(0).partition('/')
            state =  state if state else 'idle'

            if not entity in self.entities:
                raise GSLParserException('Undefined entity %s' % entity)

            if not state in self.states[entity]:
                raise GSLParserException('Undefined state %s for entity %s' % (state, entity))

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

def parse_gsl_file(filename):
    parser = GSLParser()
    rulefile = open(filename, 'r')
    for line in rulefile.readlines():
        parser.parse(line)
    return parser.get_entities(), parser.get_trans()
