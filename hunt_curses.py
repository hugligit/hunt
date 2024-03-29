import curses
import logging
import os


BROWSER_WIDTH = 30
# SETTINGS {{{
COLOUR_WALL = 242
COLOUR_FLOOR = 235
COLOUR_PLAYER = 33
TILES = """
───□
┌┬┐│
├┼┤│
└┴┘│
"""

TILES_BOLD = """
─━─ 
┏┯┓│
┠┼┨┃
┗┷┛│
"""
# }}}
root = os.path.dirname(__file__)
mazes_dir = "mazes"
mazes_path = os.path.join(root, mazes_dir)
print(mazes_path)

class Game(object): # {{{
    def __init__(self): # {{{
        fmt = '%(levelname)s : %(asctime)s : %(message)s'
        self.maps = os.listdir(mazes_path)
        self.current = 0
        logging.basicConfig(filename="hunt.log", level=logging.INFO, format=fmt)
        self.key = None
        self.game_over = False
        self.player_health = 100
        self.x = 0
        self.y = 0
        curses.wrapper(self.mainloop)
    # }}}
    def mainloop(self, stdscr): # {{{
        self.read_map(os.path.join( mazes_path, self.maps[self.current] ))
        self.setup(stdscr)
        while not self.game_over:
            self.display(stdscr)
            self.input(stdscr)
            self.update()
    # }}}
    def resize(self, stdscr): # {{{
        y, x = stdscr.getmaxyx()

        self.browser.mvwin(0, x-BROWSER_WIDTH)
        self.browser.mvderwin(0, x-BROWSER_WIDTH)
        self.browser.resize(y, BROWSER_WIDTH)
        # self.browser.resize(15, 20)

        self.hud.mvwin(0, 0)
        self.hud.resize(5, x-BROWSER_WIDTH)
        # self.hud.resize(5, 10)

        self.maze.mvwin(5, 1)
        self.maze.mvderwin(5, 1)
        self.maze.resize(y-10, x-BROWSER_WIDTH-2)
        # self.maze.resize(y-10, 35)

        self.hints.mvwin(y-5, 0)
        self.hints.mvderwin(y-5, 0)
        self.hints.resize(5, x-BROWSER_WIDTH)

        logging.debug(f"resized the screen elements for {x}, {y}")
    # }}}
    def setup(self, stdscr): # {{{
        self.screen_size = stdscr.getmaxyx()
        curses.curs_set(0)
        curses.init_pair(1, COLOUR_WALL, COLOUR_FLOOR)
        curses.init_pair(2, COLOUR_PLAYER, COLOUR_FLOOR)
        curses.init_pair(3, 240, 232)
        curses.init_pair(4, 34, COLOUR_FLOOR)
        self.C_BACKGROUND =  curses.color_pair(1)
        self.C_PLAYER =  curses.color_pair(2)
        self.C_UI = curses.color_pair(3)
        self.C_EXIT = curses.color_pair(4)
        self.filelist = curses.newpad(len(self.maps), 28)
        self.filelist.addstr("\n".join(self.maps))

        self.browser = stdscr.derwin(1,1,0,1)
        self.hud = stdscr.derwin(1,1,0,0)
        self.maze = stdscr.derwin(1,1,1,0)
        self.hints = stdscr.derwin(1,1,2,0)

        stdscr.bkgd(" ", self.C_BACKGROUND)
        self.browser.bkgd(" ", self.C_UI)
        self.hud.bkgd(" ", self.C_UI)
        self.maze.bkgd(" ", self.C_BACKGROUND)
        self.hints.bkgd(" ", self.C_UI)

        self.resize(stdscr)
        
        stdscr.clear()
        self.browser.clear()
        self.hud.clear()
        self.maze.clear()
        self.hints.clear()


        stdscr.refresh()
        self.browser.refresh()
        self.hud.refresh()
        self.maze.refresh()
        self.hints.refresh()


    # }}}
    def display(self, stdscr): # {{{

        stdscr.clear()
        self.browser.clear()
        self.hud.clear()
        self.maze.clear()
        self.hints.clear()

        new_size = stdscr.getmaxyx()
        y, x = new_size
        if (self.screen_size[0] != y) or (self.screen_size[1] != x):
        #     logging.debug("screen resized")
            self.resize(stdscr)
            self.screen_size = new_size

        for w in (self.hud, self.hints, self.browser):
            w.attron(self.C_UI)
            w.border(0, 0, 0, 0, 0, 0, 0, 0)
            w.attroff(self.C_UI)

        self.hud.addstr(1, 1, "%s:%s | %s" % (self.x, self.y, self.key))
        self.hud.addstr(2, 1, "%s: %s" % (self.current, self.maps[self.current]))
        self.maze.addstr(0, 0, self.render_map())
        self.maze.addstr(self.y, self.x, "☻", self.C_PLAYER)
        self.maze.addstr(self.exit_y, self.exit_x, "★", self.C_EXIT)

        stdscr.refresh()
        self.browser.refresh()
        self.hud.refresh()
        self.maze.refresh()
        self.hints.refresh()
        # self.filelist.refresh(self.current, -3, 1, x-BROWSER_WIDTH+1, y-2, x)
        self.filelist.refresh(self.current, -3, 1, x+1-BROWSER_WIDTH, y-2, x-1)

    # }}}
    def input(self, stdscr): # {{{
        self.key = stdscr.getkey()
    # }}}
    def update(self): # {{{
        if self.player_health < 1:
            self.game_over = True

        if self.key == "Q":
            self.game_over = True
        elif self.key == "a":
            if self.map[self.y][self.x-1] != "█": 
                self.x -= 1
            else: logging.debug("Bump")
        elif self.key == "s":
            if self.map[self.y+1][self.x] != "█": 
                self.y += 1
        elif self.key == "w":
            if self.map[self.y-1][self.x] != "█": 
                self.y -= 1
        elif self.key == "d":
            if self.map[self.y][self.x+1] != "█": 
                self.x += 1
        elif self.key == "n":
            self.current += 1
            self.current %= len(self.maps)
            self.read_map(os.path.join( mazes_path, self.maps[self.current] ))
        elif self.key == "p":
            self.current -= 1
            self.current %= len(self.maps)
            self.read_map(os.path.join( mazes_path, self.maps[self.current] ))
    # }}}

    def read_map(self, filename): # {{{
        self.map = []
        with open(filename) as m:
            logging.debug(f"reading {filename}")
            maze = m.readlines()
            for i, l in enumerate(maze):
                row = []
                for j, c in enumerate(l):
                    if c == "S":
                        self.x = j
                        self.y = i
                    if c == "E":
                        self.exit_x = j
                        self.exit_y = i

                    if c == "#":
                        row.append("█")
                    else:
                        row.append(" ")
                self.map.append(row)
    # }}}
    def render_map(self): # {{{
        output = []
        width = len(self.map[0])
        height = len(self.map)

        h = 0

        while h < height:
            row = []
            w = 0
            conversion = [4, 19, 1, 16, 9, 14, 6, 11, 3, 18, 2, 17, 8, 13, 7, 12]
            while w < width:
                c = " "
                if self.map[h][w] == "█":
                    n = 0
                    if h > 0:
                        if self.map[h-1][w] == "█": n += 0b0001
                    if h+1 < height:
                        if self.map[h+1][w] == "█": n += 0b0100
                    if w > 0:
                        if self.map[h][w-1] == "█": n += 0b1000
                    if w+1 < width:
                        if self.map[h][w+1] == "█": n += 0b0010
                    if h in (0, height-1) or w in (0, width-2):
                        c = TILES_BOLD[conversion[n]]
                    else:
                        c = TILES[conversion[n]]
                row.append(c)
                w += 1
            output.append(row)
            h += 1


        return "\n".join(["".join(r) for r in output])
    # }}}
# }}}

game = Game()
