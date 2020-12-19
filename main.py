import copy
import shutil
import sys
import select
import tty
import termios
import time
import atexit
import threading
import random

Write = sys.__stdout__.write
Flush = sys.__stdout__.flush


class Cursor:
    visible: bool = False

    @staticmethod
    def show(visible=True):
        Cursor.visible = visible
        Write("\33[?25h") if visible else Write("\33[?25l")

    @staticmethod
    def up(rows=1):
        Write(f"\33[{rows}A")

    @staticmethod
    def down(rows=1):
        Write(f"\33[{rows}B")

    @staticmethod
    def right(columns=1):
        Write(f"\33[{columns}C")

    @staticmethod
    def left(columns=1):
        Write(f"\33[{columns}D")

    @staticmethod
    def set(row, column):
        Write(f"\33[{int(column)};{int(row)}H")

    @staticmethod
    def get():
        Write(f"\33[6n")

    @staticmethod
    def save():
        Write("\33[{s}")

    @staticmethod
    def restore():
        Write("\33[{u}")


class T:
    width: int = 80
    height: int = 24

    @staticmethod
    def refresh():
        T.width, T.height = shutil.get_terminal_size()

    @staticmethod
    def reset():
        Write("\33c")
        Cursor.show(Cursor.visible)
        Flush()

    # @staticmethod
    # def initialize(col="\33[0m"):
    #     T.refresh()
    #     Write(f"{col}\r" + f"{'o' * T.width}\33[0m\n" * (T.height - 1) + f"{'o' * T.width}\33[0m")
    #     Flush()

    @staticmethod
    def clear(col="\33[0m"):
        T.refresh()
        Cursor.set(0, 0)
        Write(f"{col})")
        Write(f"\r{' ' * T.width}\n" * (T.height - 1))
        Write(f"\r{' ' * T.width}")
        Flush()

    @staticmethod
    def linewrap(set_wrap=False):
        if set_wrap:
            Write("\33[7?h")
        elif not set_wrap:
            Write("\33[7?l")

    @staticmethod
    def paint_pixel(coordinate, colour, character=' '):
        Cursor.set(coordinate[0], coordinate[1])
        Write(f"{colour}{character}{A.CEND}")

    # @staticmethod
    # def fill(col="\33[0m"):
    #     T.refresh()
    #     Cursor.set(0, 0)
    #     Write(f"{col})")
    #     Write(f"\r{' ' * T.width}\n" * (T.height - 1))
    #     Write(f"\r{' ' * T.width}")
    #     Flush()


class A:
    CEND = '\33[0m'
    CBOLD = '\33[1m'
    CITALIC = '\33[3m'
    CURL = '\33[4m'
    CBLINK = '\33[5m'
    CBLINK2 = '\33[6m'
    CSELECTED = '\33[7m'

    CBLACK = '\33[30m'
    CRED = '\33[31m'
    CGREEN = '\33[32m'
    CYELLOW = '\33[33m'
    CBLUE = '\33[34m'
    CVIOLET = '\33[35m'
    CBEIGE = '\33[36m'
    CWHITE = '\33[37m'

    CBLACKBG = '\33[40m'
    CREDBG = '\33[41m'
    CGREENBG = '\33[42m'
    CYELLOWBG = '\33[43m'
    CBLUEBG = '\33[44m'
    CVIOLETBG = '\33[45m'
    CBEIGEBG = '\33[46m'
    CWHITEBG = '\33[47m'

    CGREY = '\33[90m'
    CRED2 = '\33[91m'
    CGREEN2 = '\33[92m'
    CYELLOW2 = '\33[93m'
    CBLUE2 = '\33[94m'
    CVIOLET2 = '\33[95m'
    CBEIGE2 = '\33[96m'
    CWHITE2 = '\33[97m'

    CGREYBG = '\33[100m'
    CREDBG2 = '\33[101m'
    CGREENBG2 = '\33[102m'
    CYELLOWBG2 = '\33[103m'
    CBLUEBG2 = '\33[104m'
    CVIOLETBG2 = '\33[105m'
    CBEIGEBG2 = '\33[106m'
    CWHITEBG2 = '\33[107m'

    CWORKING = '\33[1;30;45m'
    CFAILED = '\33[1;5;30;41m'
    CSUCCES = '\33[1;30;42m'
    CBASE = '\33[1;37;100m'
    CBORDER = '\33[1;37;40m'

    LWRAPOFF = "\33[?7l"
    LWRAPON = "\33[?7h"

    TRESET = "\33c"

    DHEIGHTT = "\33#3"
    DHEIGHTB = "\33#4"
    SWIDTH = "\33#5"
    DWIDTH = "\33#6"


class Snake(threading.Thread):
    def __init__(self):
        T.refresh()
        self.start_length = 6
        self.width = T.width
        self.height = T.height
        self.center = self.init_center()
        self.__direction, self.pending_direction = 'e', ['e']
        self.current_snake: list = self.init_snake()
        self.bites: set = {self.new_bite(paint=False)}
        threading.Thread.__init__(self, daemon=True)

    def run(self):
        while True:
            self.game_start()
            Flush()
            self.game_loop()

    def game_start(self):
        steps = 0 if self.width / 2 >= self.height else 1
        for step in range(int(((self.width / 2 if steps == 0 else self.height) + 2) / 2)):
            pos = [self.center[0] - step * 2, self.center[1] - step]
            for row in range(1, step * 2):

                if 0 < pos[0] <= (self.width - 0.5) and 0 < pos[1] + row <= self.height:

                    if row == 1 or row == step * 2 - 1 or pos[1] + row == 1 or pos[1] + row == self.height:
                        T.paint_pixel([pos[0], pos[1] + row], "x" * step * 4, '')
                    else:
                        T.paint_pixel([pos[0], pos[1] + row], f"x{' ' * (step * 4 - 2)}x", '')
            Flush()
            time.sleep(0.05)
        # T.clear()
        T.paint_pixel((1, self.height), 'Bite: ', str(self.bites))
        for bite in self.bites:
            T.paint_pixel(bite, A.CREDBG2, '  ')
        Flush()
        # time.sleep(1)

    def game_loop(self):
        while True:
            try:
                self.__direction = self.pending_direction.pop(0)
            except IndexError:
                pass
            self.move()
            T.paint_pixel([1, 1], 'Score: ', str(self.score()))
            Flush()
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
            T.paint_pixel(self.current_snake[len(self.current_snake) - 1], A.CGREENBG2, '  ')
            T.paint_pixel((self.height, self.width / 2), "Position: ", str(next_coord))
            if next_coord in self.bites:
                self.bites.discard(next_coord)
                self.bites.add(self.new_bite())
            else:
                del self.current_snake[0]
                T.paint_pixel(self.current_snake[0], A.CEND, '  ')

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
                        T.paint_pixel((1, self.height), 'Bite: ', str(bite))
                        T.paint_pixel(bite, A.CREDBG2, '  ')
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


def exit_handler():
    Cursor.show(True)
    termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, original_stdin)
    T.reset()


try:
    original_stdin = termios.tcgetattr(sys.stdin.fileno())
    atexit.register(exit_handler)
    tty.setraw(sys.stdin)
except termios.error as e:
    print("termios.error:", e)
    print("Probably this terminal emulator is not supported...")
    sys.exit(1)

T.reset()
Cursor.show(False)
T.linewrap(False)


# ======================================================================================================================


def input_loop():
    while True:
        read, *_ = select.select([sys.stdin], [], [], 0)
        if sys.stdin in read:
            char = ord(sys.stdin.read(1))
            if char == 3 or char == 113:  # CTRL-C
                sys.exit(0)
            else:
                if char == 27:
                    next1, next2 = ord(sys.stdin.read(1)), ord(sys.stdin.read(1))
                    if next1 == 91:
                        if next2 == 68:  # Left
                            game.direction = 'w'
                        elif next2 == 67:  # Right
                            game.direction = 'e'
                        elif next2 == 66:  # Down
                            game.direction = 's'
                        elif next2 == 65:  # Up
                            game.direction = 'n'
        T.refresh()
        if T.width != game.width or T.height != game.height:
            sys.exit(0)
        time.sleep(0.0001)


game = Snake()
game.start()
input_loop()
