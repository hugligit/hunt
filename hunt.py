

# GAME CLASS {{{

class Game(object):
    def __init__(self, map): # {{{
        self.game_over = False
        self.player_life = 1
        print("running Game.__init__")
        # }}}

    def print_map(self): # {{{
        print("running Game.print_map")
        # }}}

    def read_commands(self): # {{{
        print("running Game.read_commands")
        # }}}


    def act(self): # {{{
        print("running Game.act")
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
