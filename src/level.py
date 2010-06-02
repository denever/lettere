'''
Created on 31/gen/2010

@author: anonymous
'''
import pygame, sys,os
from pygame.locals import *
from config import Config
from patterns import Singleton
from emdl_parser import EMDLParser
import copy

class GfxRepository(Singleton):
    gfx = dict()
    sprite_size = 32
    def __init__(self):
        Singleton.__init__(self)

    def init(self, entities=[]):
        for entity in entities:
            if not entity == 'empty':
                self.add(entity)

    def add(self, entity_type):
        self.gfx[entity_type] = pygame.image.load(Config.data_path+'/gfx/'+entity_type+'/idle/000.png')

class EntitySprite(pygame.sprite.Sprite):
    state = "idle"
    type = "empty"
    events = []
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect((0, 0), (32,32))


    def setImage(self, image):
        self.image = image

    def setPosition(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def add_event(self, event):
        self.events.append(event)

    def flush_events(self):
        temp_events = copy.deepcopy(self.events)
        self.events=[]
        return temp_events

class Level(Singleton):
    sprites_group = pygame.sprite.Group()
    minscore = 0
    maxtime = 0
    title = None
    author = None
    last_entity_id = 0
    entities = dict()
    total_score = 0
    states = dict()
    on_event = dict()

    def __init__(self):
        Singleton.__init__(self)

    def init(self):
        self.gfxrepo = GfxRepository()
        self.gfxrepo.init()
        self.execute_entity('border')
        self.debugfont = pygame.font.SysFont("Courier New", 9)
        self.set_level_size(32,32)

    def set_level_size(self, width, height):
        for i in xrange(0, height):
            self.execute_put("border/idle", i,0)
            self.execute_put("border/idle", i, width-1)

        for i in xrange(0, width):
            self.execute_put("border/idle", 0,i)
            self.execute_put("border/idle", height-1, i)

    def update_on_events(self):
        for entity_id in self.entities:
            type = self.entities[entity_id].type
            events = self.entities[entity_id].flush_events()
            if type in self.on_event:
                for event in events:
                    if event in self.on_event[type]:
                        actions = self.on_event[type][event]
                        for action in actions:
                            self.run_action(entity_id, action)

    def update(self):
        self.sprites_group.update()

    def draw(self, screen):
        self.sprites_group.draw(screen)

    def draw_debug(self, screen):
        for entity in self.sprites_group:
            debugtext = self.debugfont.render(entity.type[0:3]+"/"+entity.state[0:3], 0, (255,255,255))
            debugrect = debugtext.get_rect()
            debugrect.x = entity.rect.x
            debugrect.y = entity.rect.y-entity.rect.height/2
            screen.blit(debugtext, debugrect)

    def check_collision(self, entity_id):
        self.sprites_group.remove(self.entities[entity_id])
        collided_sprites = pygame.sprite.spritecollide(self.entities[entity_id], self.sprites_group, False)
        self.sprites_group.add(self.entities[entity_id])
        return bool(len(collided_sprites)>0)

    def execute_entity(self, entity_type):
        if entity_type not in self.gfxrepo.gfx:
            self.gfxrepo.add(entity_type)
            self.execute_state(entity_type, 'idle')
            self.on_event[entity_type] = dict()
            return "Added entity-type %s." % entity_type
        return "Entity-type %s is already added." % entity_type

    def execute_state(self, entity_name, state_name):
        if entity_name not in self.states:
            self.states[entity_name]=[]

        self.states[entity_name].append(state_name)


    def execute_put(self, entity_type, x, y):
        (entity, slash, state) = entity_type.partition('/')
        if slash == "":
            state = "idle";
        if not entity in self.gfxrepo.gfx:
            return "Entity-type %s not initialized." % entity

        if entity != "empty":
            self.last_entity_id +=1
            id = self.last_entity_id
            entity_sprite = EntitySprite()
            entity_sprite.type = entity
            entity_sprite.state = state
            entity_sprite.setImage(self.gfxrepo.gfx[entity])
            entity_sprite.setPosition(x*32, y*32)
            entity_sprite.add(self.sprites_group)
            self.entities[id] = entity_sprite
            return "Added new entity(%s) with id: %s" % (entity, id)

    def execute_line(self, entity, x1, y1, x2, y2):
        if x1 < 0 or x2 < 0 or y1 < 0 or y2 < 0:
            return "Can't start a line of entity out of a map or on borders"


        if x1 > self.size_x or x2 > self.size_x or y1 > self.size_y or y2 > self.size_y:
            return "Can't start a line of entity out of a map or on borders"

        deltax = x2 - x1
        deltay = y2 - y1
        d = 2*deltay - deltax

        if deltax > 1:
            y = y1
            for x in xrange(x1, x2):
                self.execute_put(entity, x, y)
                if d < 0:
                    d += (2*deltay)
                else:
                    d+=2*(deltay-deltax)
                    y+=1
        else:
            if deltay > 1:
                for y in xrange(y1, y2):
                    self.execute_put(entity, x1, y)

    def execute_rect(self, entity, x1, y1, height, width):
        for x in xrange(x1, x1+height):
            for y in xrange(y1, y1+width):
                self.execute_put(entity,x,y)

    def execute_move(self, entity_id, direction, pixels):
        if direction == 'n':
            self.entities[entity_id].rect.y-=pixels
        if direction == 'e':
            self.entities[entity_id].rect.x+=pixels
        if direction == 's':
            self.entities[entity_id].rect.y+=pixels
        if direction == 'w':
            self.entities[entity_id].rect.x-=pixels
        return "Moving %s, direction %s, %d pixels" % (entity_id, direction, pixels)

    def execute_destroy(self, entity_id):
        self.entities[entity_id].kill()
        return "Killed entity with id: %d" %entity_id

    def execute_add_score(self, n_scores):
        self.total_score += n_scores
        return "Added %d to score, total %d" % (n_scores, self.total_score)

    def execute_play(self, file_name):
        file_path = Config.data_path+"/sfx/"+file_name
        sound = pygame.mixer.Sound(file_path)
        sound.play()
        return "Playing %s" % file_path

    def execute_set_minscore(self, value):
        self.minscore = int(value)

    def execute_get_minscore(self):
        return self.minscore

    def execute_set_maxtime(self, value):
        self.maxtime = value

    def execute_get_maxtime(self):
        return self.maxtime

    def execute_set_map_title(self, value):
        if value is None:
            return "Can't set a map title to nothing"

        self.title = value

    def execute_get_map_title(self):
        return self.title

    def execute_set_map_author(self, value):
        if value is None:
            return "Can't set a map author to nothing"

        self.author = value

    def execute_get_map_author(self):
        return self.author

    def execute_check_entity_on_map(self, entity):
        if entity in self.gfxrepo.gfx:
                return True
        return False

    def execute_change_state(self, entity_id, new_state):
        type = self.entities[entity_id].type
        if type in self.states:
            self.entities[entity_id].state = new_state
            return "Entity %s changed state to %s" % (entity_id, new_state)
        return "State %s not defined for entity of type %s" % (new_state, type)

    def execute_on_event(self, entity_type, event, commands):
        self.on_event[entity_type][event] = commands
        return "Registered commands for entity %s on event %s" % (entity_type, event)

    def execute_launch_event(self, entity_id, event):
        return self.launch_event(entity_id, event)

    def run_action(self, entity_id, action):
        emdl_parser = EMDLParser(self, [])
        line = "%s %d" % (action, entity_id)
        print emdl_parser.parse(line)

    def launch_event(self, entity_id, event):
        self.entities[entity_id].add_event(event)
