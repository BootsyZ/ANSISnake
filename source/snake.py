import select
import sys
import time

from source.multiCanvas import MultiCanvas
from source.snakeThread import SnakeThread

from source.canvas import Canvas
from source.pygCanvas import PygCanvas


class Snake:
    def __init__(self, *args, **kwargs):
        self.debug = True if "debug" in args else False
        self.timeSleep = 0.02
        # self.timeSleep = 0.6
        self.canvas = MultiCanvas(self) if "multiCanvas" in args else \
            PygCanvas(self) if "emulated" in args else Canvas(self)
        self._snakeThread = SnakeThread(self)

    def start(self):
        self._snakeThread.run()
        self.game_loop()

    def game_loop(self):
        while True:
            t_end = time.time() + self.timeSleep
            self._snakeThread.game_loop()
            self.canvas.eventLoop()
            while time.time() < t_end:
                self.input_loop()

    def input_loop(self):
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
                            self._snakeThread.setDirection('w', 0)
                        elif next2 == 67:  # Right
                            self._snakeThread.setDirection('e', 0)
                        elif next2 == 66:  # Down
                            self._snakeThread.setDirection('s', 0)
                        elif next2 == 65:  # Up
                            self._snakeThread.setDirection('n', 0)
                elif char == 87 or char == 119:  # W
                    self._snakeThread.setDirection('n', 1)
                elif char == 83 or char == 115:  # S
                    self._snakeThread.setDirection('s', 1)
                elif char == 68 or char == 100:  # D
                    self._snakeThread.setDirection('e', 1)
                elif char == 65 or char == 97:  # A
                    self._snakeThread.setDirection('w', 1)
                elif char == 85 or char == 117:  # U
                    self._snakeThread.setDirection('n', 2)
                elif char == 72 or char == 104:  # H
                    self._snakeThread.setDirection('w', 2)
                elif char == 74 or char == 106:  # J
                    self._snakeThread.setDirection('s', 2)
                elif char == 75 or char == 107:  # K
                    self._snakeThread.setDirection('e', 2)
                elif char == 56:  # U
                    self._snakeThread.setDirection('n', 3)
                elif char == 52:  # H
                    self._snakeThread.setDirection('w', 3)
                elif char == 53:  # J
                    self._snakeThread.setDirection('s', 3)
                elif char == 54:  # K
                    self._snakeThread.setDirection('e', 3)

        self.canvas.refresh()
        if self.canvas.width != self._snakeThread.width or self.canvas.height != self._snakeThread.height:
            sys.exit(0)
        time.sleep(0.0001)
