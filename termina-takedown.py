import curses
import time
import random

PLAYER_CHAR = "^"
BULLET_CHAR = "|"
ENEMY_CHAR = "V"
INITIAL_PLAYER_X = 0
INITIAL_PLAYER_Y = 0

class Game:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.sh, self.sw = self.stdscr.getmaxyx()
        self.player_x = self.sw // 2
        self.player_y = self.sh - 2
        self.bullets = []
        self.enemies = []
        self.score = 0
        self.game_over = False

    def draw_player(self):
        self.stdscr.addch(self.player_y, self.player_x, PLAYER_CHAR)

    def move_player(self, direction):
        if direction == "LEFT" and self.player_x > 0:
            self.player_x -= 1
        elif direction == "RIGHT" and self.player_x < self.sw - 1:
            self.player_x += 1

    def handle_input(self):
        key = self.stdscr.getch()
        if key == curses.KEY_LEFT:
            self.move_player("LEFT")
        elif key == curses.KEY_RIGHT:
            self.move_player("RIGHT")
        elif key == ord('q'):
            self.game_over = True

    def game_loop(self):
        while not self.game_over:
            self.stdscr.clear()

            self.handle_input()

            self.draw_player()

            self.stdscr.refresh()
            time.sleep(0.1)

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    game = Game(stdscr)
    game.game_loop()

curses.wrapper(main)
