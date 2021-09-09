import atexit
import shutil
import sys
import termios
import tty


def write(text):
    sys.stdout.write(text)


def flush():
    sys.stdout.flush()


class Terminal:
    __instance = None

    def __init__(self, parent):
        if Terminal.__instance is None:
            Terminal.__instance = Terminal.__Terminal(parent)

        self.__dict__['_Terminal__instance'] = Terminal.__instance

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)

    class __Terminal:
        width: int = 80
        height: int = 24
        cursor_visible: bool = False
        linewrap: bool = False

        def __init__(self, parent):
            self.parent = parent
            try:
                self._original_stdin = termios.tcgetattr(sys.stdin.fileno())
                atexit.register(self._exit_handler)
                tty.setraw(sys.stdin)
                self.refresh()
                self.reset()
                self.set_cursor_visible(False)
                self.set_linewrap(False)
            except termios.error as e:
                print("termios.error:", e)
                print("This terminal emulator is probably not supported...")
                sys.exit(1)

        def _exit_handler(self):
            self.set_cursor_visible(True)
            self.set_linewrap(True)
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, self._original_stdin)
            if not self.parent.debug:
                self.reset()

        def getCenter(self):
            start = [int(self.width / 2 + 0.5), int(self.height / 2 + 0.5)]
            # for i in range(len(start)):
            #     if start[i] % 2 == 0:
            #         start[i] += 1
            return tuple(start)

        def refresh(self):
            self.width, self.height = shutil.get_terminal_size()

        def clear(self, col="\33[0m"):
            self.refresh()
            cursor_set(0, 0)
            write(f"{col})")
            write(f"\r{' ' * self.width}\n" * (self.height - 1))
            write(f"\r{' ' * self.width}")
            flush()

        def set_cursor_visible(self, arg_visible=True):
            self.cursor_visible = arg_visible
            write("\33[?25h") if self.cursor_visible else write("\33[?25l")

        def set_linewrap(self, arg_linewrap=True):
            self.linewrap = arg_linewrap
            write("\33[7?h") if self.linewrap else write("\33[7?l")

        def reset(self):
            write("\33c")
            self.set_cursor_visible(self.cursor_visible)
            self.set_linewrap(self.linewrap)
            flush()

        # def initialize(self, col="\33[0m"):
        #     self.refresh()
        #     write(f"{col}\r" + f"{'o' * self.width}\33[0m\n" * (self.height - 1) + f"{'o' * self.width}\33[0m")
        #     flush()

        # def fill(self, col="\33[0m"):
        #     self.refresh()
        #     self.set_cursor_visible(0, 0)
        #     write(f"{col})")
        #     write(f"\r{' ' * self.width}\n" * (self.height - 1))
        #     write(f"\r{' ' * self.width}")
        #     flush()


def painPixels(point, colour, character=' '):
    cursor_set(point[0], point[1])
    colour = colour or ""
    write(f"{colour}{character}\33[0m")


def cursor_up(rows=1):
    write(f"\33[{rows}A")


def cursor_down(rows=1):
    write(f"\33[{rows}B")


def cursor_right(columns=1):
    write(f"\33[{columns}C")


def cursor_left(columns=1):
    write(f"\33[{columns}D")


def cursor_set(row, column):
    write(f"\33[{int(column)};{int(row)}H")


def cursor_get():
    write(f"\33[6n")


def cursor_save():
    write("\33[{s}")


def cursor_restore():
    write("\33[{u}")
