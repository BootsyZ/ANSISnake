import random
import threading
import time
from enum import Enum, auto
from snake.canvas import Canvas, write, flush
from snake.escSeq import EscSeq
from snake.player import Player
from snake.autoPlayer import AutoPlayer
from snake.point import getNextPoint


class SnakeThread(threading.Thread):
    def __init__(self, parent):
        self.parent = parent
        self.canvas = parent.canvas
        self.canvas.refresh()
        self.start_length = 6
        self.width = self.canvas.width
        self.height = self.canvas.height
        self.center = self.canvas.getCenter()
        self.playerCount: int = 1
        self.biteCount = 1
        self.timeSleep = 0.08
        self.players: list = []
        self.bites: set = {self.newBite(paint=False)}
        threading.Thread.__init__(self, daemon=True)

    def run(self):
        self.game_menu()

    def game_menu(self):
        class Options(Enum):
            START = auto
            PLAYERS = auto
            EXIT = auto

        selection = Options.START

        if selection == Options.START:
            self.game_start()
            flush()
            self.game_loop()

    def game_start(self):
        for index in range(0, self.playerCount):
            self.players.append(AutoPlayer(self, index))

        steps = 0 if self.width >= self.height else 1
        for step in range(int(((self.width if steps == 0 else self.height) + 2) / 2)):
            pos = [self.center[0] - step, self.center[1] - step]
            for row in range(1, step * 2):

                if 0 < pos[0] <= (self.width - 0.5) and 0 < pos[1] + row <= self.height:

                    if row == 1 or row == step * 2 - 1 or pos[1] + row == 1 or pos[1] + row == self.height:
                        self.canvas.paint_pixel([pos[0], pos[1] + row], "x" * step * 4, '')
                    else:
                        self.canvas.paint_pixel([pos[0], pos[1] + row], f"x{' ' * (step * 4 - 2)}x", '')

            flush()
            time.sleep(0.1)
        self.canvas.paint_pixel((1, self.height), 'Bite: ', str(self.bites))
        for bite in self.bites:
            self.canvas.paint_pixel(bite, EscSeq.CREDBG2, '  ')
        flush()

    def game_loop(self):
        while True:
            while len(self.bites) < self.biteCount:
                self.bites.add(self.newBite())
            self.move()
            for player in self.players:
                for index in range(1, len(player.current_snake) - 1):
                    self.canvas.paint_pixel(player.current_snake[index], player.colour, '  ')
                self.canvas.paint_pixel(player.current_snake[len(player.current_snake) - 1], player.colourHead, '^^')
                self.canvas.paint_pixel([self.width / len(self.players) * player.index, 1],
                                        "[ Player " + str(player.index + 1) + ": ",
                                        str(self.score(player)) + " ]")
            for bite in self.bites:
                self.canvas.paint_pixel(bite, EscSeq.CREDBG2, '  ')
            flush()
            time.sleep(self.timeSleep)

    def move(self):
        for player in self.players:
            direction = player.getDirection()
            position = player.current_snake[len(player.current_snake) - 1]
            next_point = getNextPoint(position, direction)

            # for index in range(1, len(player.current_snake) - 1):
            #     self.canvas.paint_pixel(player.current_snake[index], player.colour, '  ')
            # self.canvas.paint_pixel(player.current_snake[len(player.current_snake) - 1], player.colourHead, '^^')

            if self.isPointValid(next_point) and not self.isPointInUse(next_point):
                player.current_snake.append(next_point)
                # self.canvas.paint_pixel(player.current_snake[len(player.current_snake) - 2], player.colour, '  ')
                # self.canvas.paint_pixel(player.current_snake[len(player.current_snake) - 1], player.colourHead, '^^')
                if next_point in self.bites:
                    self.bites.discard(next_point)
                    self.bites.add(self.newBite())
                else:
                    del player.current_snake[0]
                    self.canvas.paint_pixel(player.current_snake[0], EscSeq.CEND, '  ')
            # else: # restart when dead
            #     for point in player.current_snake:
            #         self.canvas.paint_pixel(point, EscSeq.CEND, '  ')
            #     self.players[player.index] = AutoPlayer(self, player.index)

    def setDirection(self, direction, index):
        self.players[index].setDirection(direction)

    def newBite(self, **kwargs):
        while True:
            bite = (random.randrange(3, self.width - 2, 2), random.randrange(2, self.height - 1))
            if not self.isPointInUse(bite):
                try:
                    if bite not in self.bites:
                        break
                except AttributeError:
                    break
                finally:
                    if kwargs.get("paint", True):
                        self.canvas.paint_pixel((1, self.height), 'Bite: ', str(bite))
                        self.canvas.paint_pixel(bite, EscSeq.CREDBG2, '  ')
                    return bite

    def isPointInUse(self, point):
        for player in self.players:
            if point in player.current_snake:
                return player
        return None

    def isPointFree(self, point):
        if not self.isPointValid(point):
            return False
        for player in self.players:
            if point in player.current_snake:
                return False
        return True

    def isFuturePointFree(self, point, steps, askingPlayer):
        if not self.isPointValid(point):
            return False
        for player in self.players:
            if point in player.current_snake[steps - 1:len(player.current_snake) - 1]:
                return False
            # if player == askingPlayer:
            #     if point in player.current_snake[steps-1:len(player.current_snake) - 1]:
            #         return False
            # elif point in player.current_snake:
            #     return False
        return True

    def isPointValid(self, point):
        return 1 < point[0] <= (self.width - 1.5) and 1 < point[1] <= (self.height - 1)

    def score(self, player):
        return str(len(player.current_snake) - self.start_length)
        # return int(((len(player.current_snake) - self.start_length) / (
        #         (self.width / 2) * self.height - self.start_length)) * 10000)

    def init_snake(self):
        current_snake = [self.center]
        for i in range(1, self.start_length):
            latest = current_snake[len(current_snake) - 1]
            current_snake.append(latest)
        return current_snake

    def debug(self, string, value):
        self.canvas.paint_pixel((self.width / 2, self.height), "[ " + string + ": ", str(value) + " ]")

    def debug1(self, value):
        self.canvas.paint_pixel((0, self.height - 1), "1: ", str(value))

    def debug2(self, value):
        self.canvas.paint_pixel((self.width / 4, self.height - 1), "2: ", str(value))

    def debug3(self, value):
        self.canvas.paint_pixel(((self.width / 4) * 2, self.height - 1), "3: ", str(value))

    def debug4(self, value):
        self.canvas.paint_pixel(((self.width / 4) * 3, self.height - 1), "4: ", str(value))
