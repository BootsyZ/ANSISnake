import snake.terminal as terminal


def write(x): return terminal.write(x)


def flush(): return terminal.flush()


class Canvas:
    __instance = None

    def __init__(self, parent):
        if Canvas.__instance is None:
            Canvas.__instance = Canvas.__Canvas(parent)

        self.__dict__['_Canvas__instance'] = Canvas.__instance

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)

    class __Canvas:
        width: int = 80
        height: int = 24
        _rawWidth: int = 80
        _rawHeight: int = 24
        _pixelWidth: int = 2
        _pixelHeight: int = 1

        def __init__(self, parent):
            self.parent = parent
            self.debug = parent.debug
            self._terminal = terminal.Terminal(self)
            self._terminal.refresh()

        def getCenter(self):
            start = [int(self.width / 2), int(self.height / 2)]
            for i in range(len(start)):
                if start[i] % 2 == 0:
                    start[i] += 1
            return tuple(start)

        def refresh(self):
            self._terminal.refresh()
            self._rawWidth = self._terminal.width
            self._rawHeight = self._terminal.height
            self.width = self._terminal.width / 2
            self.height = self._terminal.height

        def clear(self, col="\33[0m"):
            self._terminal.clear(col)

        def paint_pixel(self, point, colour, character=' '):
            terminal.paint_pixel(self.getRawPoint(point), colour, character)

        def getRawPoint(self, point):
            return [point[0] * self._pixelWidth, point[1] * self._pixelHeight]
