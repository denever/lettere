import sys
from emdl_parser import EMDLParser, parse_emdl_file
from rule_parser import RuleParser, parse_rule_file
from epymap import EpyMap

if __name__ == '__main__':
    map = EpyMap()
    map.initialize(32, 32)
    (entities, trans) = parse_rule_file('../data/default.txt')
    oldmap = parse_emdl_file(entities, sys.argv[1])
    parser = EMDLParser(entities)
    print oldmap
    print id(oldmap)

    while(True):
        line = raw_input('command: ')

        if line == 'view':
            print parser.get_map()
            print id(parser.get_map())

        parser.parse(line)

