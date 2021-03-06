import copy
import random
import threading
import time
from enum import Enum, auto
import snake.terminal as terminal
from snake import escSeq


def write(x): return terminal.write(x)


def flush(): return terminal.flush()


class SnakeThread(threading.Thread):
    def __init__(self, parent):
        self.parent = parent
        self.terminal = parent.terminal
        self.terminal.refresh()
        self.start_length = 6
        self.width = self.terminal.width
        self.height = self.terminal.height
        self.center = self.init_center()
        self.__direction: str
        self.pending_direction: list
        self.current_snake: list = self.init_snake()
        self.bites: set = {self.new_bite(paint=False)}
        threading.Thread.__init__(self, daemon=True)

    def run(self):
        self.game_menu()

    def game_menu(self):
        class Options(Enum):
            START = auto
            EXIT = auto

        selection = Options.START

        if selection == Options.START:
            self.game_start()
            flush()
            self.game_loop()

    def game_start(self):
        self.__direction, self.pending_direction = 'e', ['e']
        steps = 0 if self.width / 2 >= self.height else 1
        for step in range(int(((self.width / 2 if steps == 0 else self.height) + 2) / 2)):
            pos = [self.center[0] - step * 2, self.center[1] - step]
            for row in range(1, step * 2):

                if 0 < pos[0] <= (self.width - 0.5) and 0 < pos[1] + row <= self.height:

                    if row == 1 or row == step * 2 - 1 or pos[1] + row == 1 or pos[1] + row == self.height:
                        terminal.paint_pixel([pos[0], pos[1] + row], "x" * step * 4, '')
                    else:
                        terminal.paint_pixel([pos[0], pos[1] + row], f"x{' ' * (step * 4 - 2)}x", '')
            flush()
            time.sleep(0.05)
        terminal.paint_pixel((1, self.height), 'Bite: ', str(self.bites))
        for bite in self.bites:
            terminal.paint_pixel(bite, escSeq.CREDBG2, '  ')
        flush()

    def game_loop(self):
        while True:
            try:
                self.__direction = self.pending_direction.pop(0)
            except IndexError:
                pass
            self.move()
            terminal.paint_pixel([1, 1], 'Score: ', str(self.score()))
            flush()
            time.sleep(0.08)

    def move(self):
        direction = self.direction
        latest = self.current_snake[len(self.current_snake) - 1]
        next_coord: tuple
        if direction == 'n':
            next_coord = (latest[0], latest[1] - 1)
        elif direction == 'e':
            next_coord = (latest[0] + 2, latest[1])
        elif direction == 's':
            next_coord = (latest[0], latest[1] + 1)
        elif direction == 'w':
            next_coord = (latest[0] - 2, latest[1])
        else:
            raise ValueError

        if 0 < next_coord[0] <= (self.width - 0.5) and 0 < next_coord[1] <= self.height \
                and next_coord not in self.current_snake:
            self.current_snake.append(next_coord)
            terminal.paint_pixel(self.current_snake[len(self.current_snake) - 1], escSeq.CGREENBG2, '  ')
            terminal.paint_pixel((self.height, self.width / 2), "Position: ", str(next_coord))
            if next_coord in self.bites:
                self.bites.discard(next_coord)
                self.bites.add(self.new_bite())
            else:
                del self.current_snake[0]
                terminal.paint_pixel(self.current_snake[0], escSeq.CEND, '  ')

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, direction):
        if len(self.pending_direction) <= 1:
            current_direction = self.direction if len(self.pending_direction) == 0 else self.pending_direction[0]
            try:
                if direction == 'n' and current_direction != 's' \
                        or direction == 'e' and current_direction != 'w' \
                        or direction == 's' and current_direction != 'n' \
                        or direction == 'w' and current_direction != 'e':
                    if len(self.pending_direction) == 0:
                        self.pending_direction = list(direction)
                    elif len(self.pending_direction) == 1:
                        new_pending_direction = copy.copy(self.pending_direction)
                        new_pending_direction.append(direction)
                        self.pending_direction = new_pending_direction
                else:
                    raise ValueError
            except ValueError:
                pass

    def new_bite(self, **kwargs):
        while True:
            bite = (random.randrange(1, self.width, 2), random.randrange(2, self.height))
            if bite not in self.current_snake:
                try:
                    if bite not in self.bites:
                        break
                except AttributeError:
                    break
                finally:
                    if kwargs.get("paint", True):
                        terminal.paint_pixel((1, self.height), 'Bite: ', str(bite))
                        terminal.paint_pixel(bite, escSeq.CREDBG2, '  ')
                    return bite

    def score(self):
        return int(((len(self.current_snake) - self.start_length) / (
                (self.width / 2) * self.height - self.start_length)) * 10000)

    def init_center(self):
        start = [int(self.width / 2), int(self.height / 2)]
        for i in range(len(start)):
            if start[i] % 2 == 0:
                start[i] += 1
        return tuple(start)

    def init_snake(self):
        current_snake = [self.center]
        for i in range(1, self.start_length):
            latest = current_snake[len(current_snake) - 1]
            current_snake.append(latest)
        return current_snake
