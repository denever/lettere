from game import Game

try:
    g = Game()
    g.start()
except Exception, e:
    print e

