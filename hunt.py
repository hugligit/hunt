import sys, maze_gen


# GAME CLASS {{{

class Game(object):
    def __init__(self, map): # {{{
        self.x = 0
        self.y = 0
        self.game_over = False
        self.player_life = 9
        self.width = 16
        self.height = 16
        self.l = ["w", "a", "s", "d", "q", "die"]
        # print("running Game.__init__")
        # }}}

    def print_map(self): # {{{
        # print("running Game.print_map")
        for line in maze_gen.maze:
            print (line)
        print("Bob at [%s: %s]  HP:%s" % (self.x, 0-self.y, self.player_life))
        # }}}

    def read_commands(self): # {{{
        # print("running Game.read_commands")
        self.command = input(">  " )
        # }}}
    def exit(self):
        sys.exit()

    def act(self): # {{{
        #print("running Game.act"
            if self.command in self.l:
                if self.command == 'a':
                    if maze_gen.maze [self.y] [self.x-1] == 0:
                        self.x -= 1
                        print ("You moved left")
                    else:
                        print ("Ow! You hit a wall")
                if self.command == 'd':
                    if maze_gen.maze [self.y] [self.x+1] == 0:
                        self.x += 1
                        print ("You moved right")
                    else: 
                        print ("Ow! You hit a wall")
                if self.command == 'w':
                    if maze_gen.maze [self.y-1] [self.x] == 0:
                        self.y -= 1
                        print ("You moved forward")
                    else:
                        print ("Ow! You hit a wall")
                if self.command == 's':
                    if maze_gen.maze [self.y+1] [self.x] == 0:
                        self.y += 1
                        print ("You moved backwards")
                    else:
                        print ("Ow! You hit a wall")
                if self.command == 'die':
                    self.player_life -=1
                    print ("You were killed by a shopkeeper...")
                if self.player_life == 0:
                    game.game_over = True
                    print ("You used up all your nine lives")
                if self.command == 'q':
                    self.exit()
                    print ("Goodbye!")
            else:
                 print ("You said %s. Well done!" %self.command)
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
