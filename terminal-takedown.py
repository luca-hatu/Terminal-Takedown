import curses
import time
import random

PLAYER_CHAR = "^"
BULLET_CHAR = "|"
ENEMY_CHAR = "V"
ENEMY_FAST_CHAR = "W"
POWERUP_CHAR = "*"
BULLET_SPEED = 0.05
ENEMY_SPEED = 0.1
FAST_ENEMY_SPEED = 0.15
POWERUP_SPAWN_RATE = 100
ENEMY_SPAWN_RATE = 15
PLAYER_SPEED = 2

class Game:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.sh, self.sw = self.stdscr.getmaxyx()
        self.player_x = self.sw // 2
        self.player_y = self.sh - 2
        self.bullets = []
        self.enemies = []
        self.powerups = []
        self.score = 0
        self.level = 1
        self.game_over = False
        self.enemy_spawn_counter = ENEMY_SPAWN_RATE

    def draw_player(self):
        self.stdscr.addch(self.player_y, self.player_x, PLAYER_CHAR)

    def draw_bullets(self):
        for bullet in self.bullets:
            self.stdscr.addch(bullet['y'], bullet['x'], BULLET_CHAR)

    def draw_enemies(self):
        for enemy in self.enemies:
            self.stdscr.addch(enemy['y'], enemy['x'], enemy['char'])

    def draw_powerups(self):
        for powerup in self.powerups:
            self.stdscr.addch(powerup['y'], powerup['x'], POWERUP_CHAR)

    def move_bullets(self):
        new_bullets = []
        for bullet in self.bullets:
            bullet['y'] -= 1
            if bullet['y'] >= 0:
                new_bullets.append(bullet)
        self.bullets = new_bullets

    def move_enemies(self):
        for enemy in self.enemies:
            enemy['y'] += 1 if enemy['char'] == ENEMY_CHAR else 2
        self.enemies = [e for e in self.enemies if e['y'] < self.sh]

    def move_powerups(self):
        for powerup in self.powerups:
            powerup['y'] += 1
        self.powerups = [p for p in self.powerups if p['y'] < self.sh]

    def shoot_bullet(self):
        bullet = {'x': self.player_x, 'y': self.player_y - 1}
        self.bullets.append(bullet)

    def spawn_enemy(self):
        if random.randint(0, self.enemy_spawn_counter) == 0:
            enemy_x = random.randint(0, self.sw - 1)
            enemy_type = ENEMY_CHAR if random.random() > 0.5 else ENEMY_FAST_CHAR
            enemy = {'x': enemy_x, 'y': 0, 'char': enemy_type}
            self.enemies.append(enemy)

    def spawn_powerup(self):
        if random.randint(0, POWERUP_SPAWN_RATE) == 0:
            powerup_x = random.randint(0, self.sw - 1)
            powerup = {'x': powerup_x, 'y': 0}
            self.powerups.append(powerup)

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
            self.player_x -= PLAYER_SPEED
        elif direction == "RIGHT" and self.player_x < self.sw - 1:
            self.player_x += PLAYER_SPEED

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

        for powerup in self.powerups:
            if powerup['x'] == self.player_x and powerup['y'] == self.player_y:
                self.powerups.remove(powerup)
                self.activate_powerup()

    def activate_powerup(self):
        self.enemy_spawn_counter = max(ENEMY_SPAWN_RATE - 5, 5) 

    def draw_score(self):
        score_str = f"Score: {self.score} Level: {self.level}"
        self.stdscr.addstr(0, 0, score_str)

    def show_game_over(self):
        self.stdscr.clear()
        game_over_msg = "GAME OVER"
        score_msg = f"Your Score: {self.score}"
        restart_msg = "Press 'r' to Restart or 'q' to Quit"
        self.stdscr.addstr(self.sh // 2 - 1, (self.sw - len(game_over_msg)) // 2, game_over_msg)
        self.stdscr.addstr(self.sh // 2, (self.sw - len(score_msg)) // 2, score_msg)
        self.stdscr.addstr(self.sh // 2 + 1, (self.sw - len(restart_msg)) // 2, restart_msg)
        self.stdscr.refresh()

    def level_up(self):
        if self.score > 0 and self.score % 10 == 0:
            self.level += 1
            self.enemy_spawn_counter = max(ENEMY_SPAWN_RATE - (self.level * 2), 5)

    def game_loop(self):
        while not self.game_over:
            self.stdscr.clear()
            self.handle_input()
            self.move_bullets()
            self.move_enemies()
            self.move_powerups()
            self.spawn_enemy()
            self.spawn_powerup()
            self.check_collisions()
            self.level_up()
            self.draw_player()
            self.draw_bullets()
            self.draw_enemies()
            self.draw_powerups()
            self.draw_score()
            self.stdscr.refresh()
            time.sleep(BULLET_SPEED)

        self.show_game_over()
        while True:
            key = self.stdscr.getch()
            if key == ord('r'):
                self.__init__(self.stdscr)
                self.game_loop()
            elif key == ord('q'):
                break

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(50) 

    game = Game(stdscr)
    game.game_loop()

curses.wrapper(main)
