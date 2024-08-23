import curses
import time
import random

PLAYER_CHAR = "^"
BULLET_CHAR = "|"
ENEMY_CHAR = "V"
BULLET_SPEED = 0.05
ENEMY_SPEED = 0.5
ENEMY_SPAWN_RATE = 10

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
        self.enemy_spawn_counter = ENEMY_SPAWN_RATE

    def draw_player(self):
        self.stdscr.addch(self.player_y, self.player_x, PLAYER_CHAR)

    def draw_bullets(self):
        for bullet in self.bullets:
            self.stdscr.addch(bullet['y'], bullet['x'], BULLET_CHAR)

    def draw_enemies(self):
        for enemy in self.enemies:
            self.stdscr.addch(enemy['y'], enemy['x'], ENEMY_CHAR)

    def move_bullets(self):
        new_bullets = []
        for bullet in self.bullets:
            bullet['y'] -= 1
            if bullet['y'] >= 0:
                new_bullets.append(bullet)
        self.bullets = new_bullets

    def move_enemies(self):
        for enemy in self.enemies:
            enemy['y'] += 1
        self.enemies = [e for e in self.enemies if e['y'] < self.sh]

    def shoot_bullet(self):
        bullet = {'x': self.player_x, 'y': self.player_y - 1}
        self.bullets.append(bullet)

    def spawn_enemy(self):
        if random.randint(0, self.enemy_spawn_counter) == 0:
            enemy_x = random.randint(0, self.sw - 1)
            enemy = {'x': enemy_x, 'y': 0}
            self.enemies.append(enemy)

    def handle_input(self):
        key = self.stdscr.getch()
        if key == curses.KEY_LEFT:
            self.move_player("LEFT")
        elif key == curses.KEY_RIGHT:
            self.move_player("RIGHT")
        elif key == ord(' '):
            self.shoot_bullet()
        elif key == ord('q'):
            self.game_over = True

    def move_player(self, direction):
        if direction == "LEFT" and self.player_x > 0:
            self.player_x -= 1
        elif direction == "RIGHT" and self.player_x < self.sw - 1:
            self.player_x += 1

    def check_collisions(self):
        new_bullets = []
        for bullet in self.bullets:
            hit = False
            for enemy in self.enemies:
                if bullet['x'] == enemy['x'] and bullet['y'] == enemy['y']:
                    self.enemies.remove(enemy)
                    hit = True
                    self.score += 1
                    break
            if not hit:
                new_bullets.append(bullet)
        self.bullets = new_bullets

        for enemy in self.enemies:
            if enemy['x'] == self.player_x and enemy['y'] == self.player_y:
                self.game_over = True

    def draw_score(self):
        score_str = f"Score: {self.score}"
        self.stdscr.addstr(0, 0, score_str)

    def game_loop(self):
        while not self.game_over:
            self.stdscr.clear()
            self.handle_input()
            self.move_bullets()
            self.move_enemies()
            self.spawn_enemy()
            self.check_collisions()
            self.draw_player()
            self.draw_bullets()
            self.draw_enemies()
            self.draw_score()
            self.stdscr.refresh()
            time.sleep(BULLET_SPEED)

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(50)

    game = Game(stdscr)
    game.game_loop()

curses.wrapper(main)
