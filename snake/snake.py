import select
import sys
import time

import snake.terminal as terminal
from snake.snakeThread import SnakeThread


def write(x): return terminal.write(x)


def flush(): return terminal.flush()


class Snake:
    def __init__(self, *args, **kwargs):
        self.debug = True if "debug" in args else False
        self.terminal = terminal.Terminal(self)
        self._snakeThread = SnakeThread(self)

    def start(self):
        self._snakeThread.start()
        self.input_loop()

    def input_loop(self):
        while True:
            read, *_ = select.select([sys.stdin], [], [], 0)
            if sys.stdin in read:
                char = ord(sys.stdin.read(1))
                if char == 3 or char == 81 or char == 113:  # CTRL-C or Q or q
                    sys.exit(0)
                else:
                    if char == 27:
                        next1, next2 = ord(sys.stdin.read(1)), ord(sys.stdin.read(1))
                        if next1 == 91:
                            if next2 == 68:  # Left
                                self._snakeThread.direction = 'w'
                            elif next2 == 67:  # Right
                                self._snakeThread.direction = 'e'
                            elif next2 == 66:  # Down
                                self._snakeThread.direction = 's'
                            elif next2 == 65:  # Up
                                self._snakeThread.direction = 'n'
            self.terminal.refresh()
            if self.terminal.width != self._snakeThread.width or self.terminal.height != self._snakeThread.height:
                sys.exit(0)
            time.sleep(0.0001)
