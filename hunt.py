# GAME CLASS {{{

class Game(object):
    def __init__(self, map): # {{{
        self.x = 0
        self.y = 0
        self.game_over = False
        self.player_life = 5
        # print("running Game.__init__")
        # }}}

    def print_map(self): # {{{
        # print("running Game.print_map")
        print("Bob at [%s: %s]  HP:%s" % (self.x, self.y, self.player_life))
        # }}}

    def read_commands(self): # {{{
        # print("running Game.read_commands")
        self.command = input("now? " )
        # }}}

    def act(self): # {{{
        # print("running Game.act")
        if self.command == 'l':
            self.x -= 1
        if self.command == 'r':
            self.x += 1
        if self.command == 'u':
            self.y += 1
        if self.command == 'd':
            self.y -= 1
        if self.command == 'die':
            self.player_life -=1
        if self.player_life == 0:
            game.game_over = True
        # }}}








# }}}

# MAIN LOOP  {{{
game = Game(map)

while not game.game_over:
    game.print_map()
    game.read_commands()
    game.act()

    if game.player_life < 1:
        game.game_over = True
# }}}
