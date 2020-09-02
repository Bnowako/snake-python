import pygame
import threading
import time
import sys
import random
window_size = (800, 600)


class Score:
    points = 0

    def update_scoreboard(self):
        font_style = pygame.font.SysFont("bahnschrift", 25)
        value = font_style.render(
            "Your Score: " + str(self.points), True, (255, 0, 0))
        display.blit(value, [0, 0])


class Snake:

    segments_count = 0

    red = (255, 0, 0)
    black = (0, 0, 0)

    pos_x = window_size[0]/2
    pos_y = window_size[1]/2

    prev_pos = [(pos_x, pos_y)]

    x_change = 0
    y_change = 0

    def draw(self):
        pygame.draw.rect(display, self.red, [
                         self.pos_x, self.pos_y, 10, 10])
        pygame.display.update()

    def direction(self, key_code):
        if self.segments_count == 0:
            if key_code == 273:
                # up
                self.x_change = 0
                self.y_change = -10
                # self.pos_y += -10
            elif key_code == 274:
                # down
                self.x_change = 0
                self.y_change = 10
                # self.pos_y += 10
            elif key_code == 276:
                # left
                self.x_change = -10
                self.y_change = 0
                # self.pos_x += -10
            elif key_code == 275:
                # right
                self.x_change = 10
                self.y_change = 0
                # self.pos_x += 10
        elif self.segments_count > 0:
            if key_code == 273 and self.y_change != 10:
                # up
                self.x_change = 0
                self.y_change = -10
                # self.pos_y += -10
            elif key_code == 274 and self.y_change != -10:
                # down
                self.x_change = 0
                self.y_change = 10
                # self.pos_y += 10
            elif key_code == 276 and self.x_change != 10:
                # left
                self.x_change = -10
                self.y_change = 0
                # self.pos_x += -10
            elif key_code == 275 and self.x_change != -10:
                # right
                self.x_change = 10
                self.y_change = 0
                # self.pos_x += 10

    def movement(self):
        self.prev_pos.append((self.pos_x, self.pos_y))
        self.pos_x += self.x_change
        self.pos_y += self.y_change

        self.prev_pos = self.prev_pos[-1000:]
        self.boundaries_handler()
        self.collision_handler()

        display.fill(self.black)
        pygame.draw.rect(display, self.red, [
            self.pos_x, self.pos_y, 10, 10])

        for segment in range(self.segments_count):
            pygame.draw.rect(display, self.red, [
                self.prev_pos[-(segment+1)][0], self.prev_pos[-(segment+1)][1], 10, 10])
        score.update_scoreboard()
        pygame.display.update()

    def boundaries_handler(self):

        if self.pos_x == -10:
            self.pos_x = window_size[0] - 10
        elif self.pos_x == window_size[0]:
            self.pos_x = 0
        elif self.pos_y == -10:
            self.pos_y = window_size[1] - 10
        elif self.pos_y == window_size[1]:
            self.pos_y = 0

    def collision_handler(self):
        for segment in range(self.segments_count):
            print(self.prev_pos[-(segment+1)][0])
            if self.pos_x == self.prev_pos[-(segment+1)][0] and self.pos_y == self.prev_pos[-(segment+1)][1]:
                self.restart_game()
                time.sleep(2)
                break

    def add_new_segment(self):
        self.segments_count += 50

    def restart_game(self):
        self.x_change = 0
        self.y_change = 0
        self.pos_x = window_size[0]/2
        self.pos_y = window_size[1]/2
        self.segments_count = 0
        self.prev_pos = [(self.pos_x, self.pos_y)]
        score.points = 0


class Food:
    rand_x = round(random.randrange(0, window_size[0]-10), -1)
    rand_y = round(random.randrange(0, window_size[1]-10), -1)

    def new_pos(self):
        self.rand_x = round(random.randrange(0, window_size[0]-10), -1)
        self.rand_y = round(random.randrange(0, window_size[1]-10), -1)

    def draw(self):
        blue = (0, 0, 255)
        pygame.draw.rect(display, blue, [
            self.rand_x, self.rand_y, 10, 10])
        pygame.display.update()


pygame.init()
display = pygame.display.set_mode(window_size)


pygame.display.update()
snake = Snake()
food = Food()
score = Score()

snake.draw()
clock = pygame.time.Clock()


while 1:

    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            snake.direction(event.__dict__['key'])

    snake.movement()
    food.draw()

    if snake.pos_x == food.rand_x and snake.pos_y == food.rand_y:
        food.new_pos()
        score.points += 1
        snake.add_new_segment()

clock.tick(30)
pygame.quit()
quit()
