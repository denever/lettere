
class EMDLParser:
    def __init__(self, level, allowed_entities):
        self.entities = allowed_entities
        self.level = level

    def parse(self, line):
        line = line.strip()
        if line.startswith('set name'):
            return self.level.execute_set_map_title(line[10:-2])

        if line.startswith('set author'):
            return self.level.execute_set_map_author(line[12:-2])

        if line.startswith('set maxtime'):
            return self.level.execute_set_maxtime(int(line[12:-1]))

        if line.startswith('set minscore'):
            return self.level.execute_set_minscore(int(line[13:-1]))

        if line.startswith('get name'):
            return self.level.execute_get_map_title()

        if line.startswith('get author'):
            return self.level.execute_get_map_author()

        if line.startswith('get maxtime'):
            return self.level.execute_get_maxtime()

        if line.startswith('get minscore'):
            return self.level.execute_get_minscore()

        if line.startswith('put'):
            cmd, entity, pos = line.split(' ')
            y, x = eval(pos[1:-2])
            return self.level.execute_put(entity, x, y)

        if line.startswith('line'):
            cmd, entity, pos = line.split(' ')
            if not entity in self.entities:
                return "Can't set unknown entity %s" % entity
            pos = pos.replace(')(',',')
            x1, y1, x2, y2 = eval(pos[1:-2])
            return self.level.execute_line(entity, x1, y1, x2, y2)

        if line.startswith('rect'):
            cmd, entity, pos = line.split(' ')
            if not entity in self.entities:
                return "Can't set unknown entity %s" % entity
            pos = pos.replace(')(',',')
            x1, y1, height, width = eval(pos[1:-2])
            return self.level.execute_rect(entity, x1, y1, height, width)

        if line.startswith('play'):
            cmd, space, args = line.partition(' ')
            return self.level.execute_play(args)

        if line.startswith('move'):
            cmd, direction, n_pixels, entity_id = line.split(' ', 3)
            return self.level.execute_move(int(entity_id), direction, int(n_pixels))

        if line.startswith('add_score'):
            cmd, n_scores = line.split(' ', 1)
            return self.level.execute_add_score(int(n_scores))



def parse_emdl_file(defined_entities, filename, level):
    parser = EMDLParser(level, defined_entities)
    emdl_file = open(filename, 'r')
    for line in emdl_file.readlines():
        print parser.parse(line)

