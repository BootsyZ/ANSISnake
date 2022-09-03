import source.terminal as terminal


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

        @staticmethod
        def flush():
            return terminal.flush()

        def getCenter(self):
            start = [int(self.width / 2), int(self.height / 2 + 0.5)]
            # for i in range(len(start)):
            #     if start[i] % 2 == 0:
            #         start[i] += 1
            return tuple(start)

        def refresh(self):
            self._terminal.refresh()
            self._rawWidth = self._terminal.width
            self._rawHeight = self._terminal.height
            self.width = int(self._terminal.width / self._pixelWidth) - 1
            self.height = int(self._terminal.height / self._pixelHeight) - 1

        def clear(self, col="\33[0m"):
            self._terminal.clear(col)

        def paintPixels(self, point, colour, character=' '):
            terminal.painPixels(self.getRawPoint(point), colour, character)

        def paintRect(self, **kwargs):
            topLeft = kwargs.get("topLeft", (0, 0))
            bottomRight = kwargs.get("bottomRight", (self.width, self.height))
            if not 0 <= topLeft[0] < bottomRight[0] or not 0 <= topLeft[1] < bottomRight[1]:
                raise ValueError

            paintLine = True if kwargs.get("line") or kwargs.get("lineColour") else False
            line = kwargs.get("line", " ")
            lineColour = kwargs.get("lineColour")

            paintFill = True if kwargs.get("fill") or kwargs.get("fillColour") else False
            fill = kwargs.get("fill", " ")
            fillColour = kwargs.get("fillColour")

            width = (bottomRight[0] - topLeft[0]) * self._pixelWidth
            height = (bottomRight[1] - topLeft[1]) * self._pixelHeight

            startPoint = self.getRawPoint(topLeft)
            endPoint = (startPoint[0] + width, startPoint[1] + height)

            fillString = (fill * (int(width / len(fill) + 0.5) + 1))[0:width - len(line) + 1] if paintFill else fill
            # lineString = (line * (int(width / len(line) + 0.5) + 2))[0:width + 2] if paintLine else line

            if paintLine:
                for index in range(1, len(line) + 1):
                    terminal.painPixels((startPoint[0], startPoint[1] + index - 1), lineColour,
                                        line[0:index] +
                                        line[index - 1:index] * ((width + 2) - (index * 2)) +
                                        line[0:index][::-1])
                    # line[-len(line)-5:-(len(line) + index):-1])

            for row in range(startPoint[1] + len(line), endPoint[1] - len(line) + 1):
                # terminal.painPixels((self._rawWidth - 16, 10 + row), lineColour, str(row))
                if paintLine:
                    terminal.painPixels((startPoint[0], row), lineColour, line)
                if paintFill:
                    terminal.painPixels((startPoint[0] + len(line), row), fillColour, fillString)
                if paintLine:
                    terminal.painPixels((endPoint[0] + self._pixelWidth - len(line), row), lineColour, line[::-1])

            if paintLine:
                for index in range(1, len(line) + 1):
                    terminal.painPixels((startPoint[0], endPoint[1] - index + 1), lineColour,
                                        line[0:index] +
                                        line[index - 1:index] * ((width + 2) - (index * 2)) +
                                        line[0:index][::-1])

        def getRawPoint(self, point):
            rawPoint = [point[0] * self._pixelWidth + 1, point[1] * self._pixelHeight + 1]
            return rawPoint
