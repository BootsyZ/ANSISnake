import random
import threading
import time
from enum import Enum, auto

from source.canvas import Canvas, write, flush
from source.escSeq import EscSeq
from source.player import Player
from source.autoPlayer import AutoPlayer
from source.point import getNextPoint


class SnakeThread(threading.Thread):
    def __init__(self, parent):
        self.parent = parent
        self.canvas = parent.canvas
        self.canvas.refresh()
        self.start_length = 6
        self.width = self.canvas.width
        self.height = self.canvas.height
        self.center = self.canvas.getCenter()
        self.playerCount: int = 3
        self.biteCount = 64
        # self.biteCount = (self.width - 2) * (self.height - 2) + self.playerCount * self.start_length
        self.timeSleep = 0.08
        # self.timeSleep = 2.4
        self.restart = True
        self.players: list = []
        # self.bites: set = {self.newBite(paint=False)}
        self.bites: set = set()
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

    def introAnimation(self):
        topLeft = [0, 0]
        bottomRight = [self.width, self.height]

        pointA = list(self.center)
        pointB = list(self.center)

        while True:
            if pointA[0] > topLeft[0]:
                pointA[0] -= 1
            if pointA[1] > topLeft[1]:
                pointA[1] -= 1
            if pointB[0] < bottomRight[0]:
                pointB[0] += 1
            if pointB[1] < bottomRight[1]:
                pointB[1] += 1

            self.canvas.paintRect(topLeft=(pointA[0], pointA[1]), bottomRight=(pointB[0], pointB[1]), line="x",
                                  fill=" ")

            flush()
            if pointA == topLeft and pointB == bottomRight:
                break
            time.sleep(0.01)

    def game_start(self):
        for index in range(0, self.playerCount):
            self.players.append(AutoPlayer(self, index))

        self.canvas.paintPixels(self.center, EscSeq.CBLUEBG, '--')
        self.canvas.paintPixels((0, 0), EscSeq.CBLUEBG, '--')
        self.canvas.paintPixels((0, self.height), EscSeq.CBLUEBG, '--')
        self.canvas.paintPixels((self.width, 0), EscSeq.CBLUEBG, '--')
        self.canvas.paintPixels((self.width, self.height), EscSeq.CBLUEBG, '--')

        self.introAnimation()
        # self.canvas.paintRect(topLeft=(self.width - 5, 0), bottomRight=(self.width, 5), line="x", fill="-")
        # self.canvas.paintRect(topLeft=(0, 0), bottomRight=(5, 5), fill="o", line="x")
        # self.canvas.paintRect(topLeft=(8, 1), bottomRight=(16, 6), line="xy", fill="-0")
        # self.canvas.paintRect(topLeft=(20, 4), bottomRight=(30, 12), line="xyz", fill="=")
        # self.canvas.paintRect(topLeft=(38, 4), bottomRight=(48, 12), line="123")
        # self.canvas.paintRect(topLeft=(6, 8), bottomRight=(10, 12), lineColour=EscSeq.CVIOLETBG2,
        #                       fillColour=EscSeq.CVIOLETBG)
        # self.canvas.paintRect(topLeft=(15, 15), bottomRight=(25, 25), line="+", fill="-")
        # self.canvas.paintRect(topLeft=(48, 15), bottomRight=(56, 25), line="+", lineColour=EscSeq.CBLUE2, fill="-",
        #                       fillColour=EscSeq.CRED)
        # self.canvas.paintRect(topLeft=(32, 15), bottomRight=(44, 25), line="12", fill="-")

        # if self.parent.debug:
        self.canvas.paintPixels(self.center, EscSeq.CBLUEBG, '--')
        self.canvas.paintPixels((0, 0), EscSeq.CBLUEBG, '--')
        self.canvas.paintPixels((0, self.height), EscSeq.CBLUEBG, '--')
        self.canvas.paintPixels((self.width, 0), EscSeq.CBLUEBG, '--')
        self.canvas.paintPixels((self.width, self.height), EscSeq.CBLUEBG, '--')
        self.debug1("raw w/h " + str(self.canvas._rawWidth) + " / " + str(self.canvas._rawHeight))
        self.debug2("game w/h " + str(self.canvas.width) + " / " + str(self.canvas.height))
        self.debug3("Center: " + str(self.center))

        for i in range(self.width + 1):
            if i == 0 or i % 2 == 0:
                self.canvas.paintPixels((i, 0), EscSeq.CWHITEBG, "  ")
                self.canvas.paintPixels((i, 0), EscSeq.CBLACKONWHITE, str(i))
            else:
                self.canvas.paintPixels((i, 0), EscSeq.CBLACKBG, "  ")
                self.canvas.paintPixels((i, 0), EscSeq.CWHITEONBLACK, str(i))

        for i in range(self.height + 1):
            if i == 0 or i % 2 == 0:
                self.canvas.paintPixels((0, i), EscSeq.CWHITEBG, "  ")
                self.canvas.paintPixels((0, i), EscSeq.CBLACKONWHITE, str(i))
            else:
                self.canvas.paintPixels((0, i), EscSeq.CBLACKBG, "  ")
                self.canvas.paintPixels((0, i), EscSeq.CWHITEONBLACK, str(i))
        flush()
        time.sleep(3)

        # self.canvas.paintPixels((0, self.height), '[ Bite: ', str(self.bites) + " ]")
        # for bite in self.bites:
        #     self.canvas.paintPixels(bite, EscSeq.CREDBG2, '  ')
        # flush()
        while len(self.bites) < self.biteCount:
            self.bites.add(self.newBite(paint=False))

    def game_loop(self):
        while True:
            self.move()
            for player in self.players:
                for index in range(1, len(player.current_snake) - 1):
                    self.canvas.paintPixels(player.current_snake[index], player.colour, '  ')
                self.canvas.paintPixels(player.current_snake[len(player.current_snake) - 1], player.colourHead, '^^')
                # self.canvas.paintPixels([self.width / len(self.players) * player.index, 1],
                #                         "[ Player " + str(player.index + 1) + ": ",
                #                         str(self.score(player)) + " ]")
            for bite in self.bites:
                self.canvas.paintPixels(bite, EscSeq.CREDBG2, '  ')

            self.canvas.paintPixels(self.center, EscSeq.CBLUEBG, '--')
            self.canvas.paintPixels((0, 0), EscSeq.CBLUEBG, '--')
            self.canvas.paintPixels((0, self.height), EscSeq.CBLUEBG, '--')
            self.canvas.paintPixels((self.width, 0), EscSeq.CBLUEBG, '--')
            self.canvas.paintPixels((self.width, self.height), EscSeq.CBLUEBG, '--')
            flush()
            time.sleep(self.timeSleep)

    def move(self):
        for player in self.players:
            direction = player.getDirection()
            position = player.current_snake[len(player.current_snake) - 1]
            next_point = getNextPoint(position, direction)

            # for index in range(1, len(player.current_snake) - 1):
            #     self.canvas.paintPixels(player.current_snake[index], player.colour, '  ')
            # self.canvas.paintPixels(player.current_snake[len(player.current_snake) - 1], player.colourHead, '^^')

            if self.isPointValid(next_point) and not self.isPointInUse(next_point):
                player.current_snake.append(next_point)
                # self.canvas.paintPixels(player.current_snake[len(player.current_snake) - 2], player.colour, '  ')
                # self.canvas.paintPixels(player.current_snake[len(player.current_snake) - 1], player.colourHead, '^^')
                if next_point in self.bites:
                    self.bites.discard(next_point)
                    self.bites.add(self.newBite())
                else:
                    del player.current_snake[0]
                    self.canvas.paintPixels(player.current_snake[0], EscSeq.CEND, '  ')
            elif self.restart:  # restart when dead
                for point in player.current_snake:
                    self.canvas.paintPixels(point, EscSeq.CEND, '  ')
                self.players[player.index] = AutoPlayer(self, player.index)

    def setDirection(self, direction, index):
        self.players[index].setDirection(direction)

    def newBite(self, **kwargs):
        while True:
            # bite = (random.randrange(1, self.width), random.randrange(1, self.height))
            bite = (random.randrange(1, self.width), random.randrange(1, self.height))
            if not self.isPointInUse(bite):
                try:
                    if bite not in self.bites:
                        break
                except AttributeError:
                    break
                finally:
                    if kwargs.get("paint", True):
                        self.canvas.paintPixels((1, self.height), 'Bite: ', str(bite))
                        self.canvas.paintPixels(bite, EscSeq.CREDBG2, '  ')
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
        return 0 < point[0] < self.width and 0 < point[1] < self.height

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
        self.canvas.paintPixels((self.width / 2, self.height), "[ " + string + ": ", str(value) + " ]")

    def debug1(self, value):
        self.canvas.paintPixels((0, self.height - 1), "[ 1: ", str(value) + " ]")

    def debug2(self, value):
        self.canvas.paintPixels((self.width / 4, self.height - 1), "[ 2: ", str(value) + " ]")

    def debug3(self, value):
        self.canvas.paintPixels(((self.width / 4) * 2, self.height - 1), "[ 3: ", str(value) + " ]")

    def debug4(self, value):
        self.canvas.paintPixels(((self.width / 4) * 3, self.height - 1), "[ 4: ", str(value) + " ]")
