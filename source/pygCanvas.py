import pygame
import pygame.freetype
from source.escSeq import EscSeq


class PygCanvas:
    __instance = None

    def __init__(self, parent):
        if PygCanvas.__instance is None:
            PygCanvas.__instance = PygCanvas.__Canvas(parent)

        self.__dict__['_Canvas__instance'] = PygCanvas.__instance

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)

    class __Canvas:
        fontSize = 12
        width: int = 40
        height: int = 24
        _rawSize = _rawWidth, _rawHeight = 800, 480
        _charWidth: int = _rawWidth / width
        _charHeight: int = _rawHeight / height
        _pixelWidth: int = 2
        _pixelHeight: int = 1

        def __init__(self, parent):
            self.parent = parent
            self.debug = parent.debug
            pygame.init()
            self.display = pygame.display.set_mode(self._rawSize, pygame.HWSURFACE | pygame.DOUBLEBUF)
            self.texture = pygame.Surface(self._rawSize)
            self.font = pygame.freetype.SysFont("mono", self.fontSize, bold=True)
            sampleText = "abcdefghijklmnopqrstuvwxyz  ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            text_surface, text_rect = self.font.render(sampleText)
            self._charWidth, self._charHeight = int(text_rect.width / len(sampleText)), int(
                text_rect.height * 1.4)
            self.width = int((self._rawWidth / self._charWidth) / self._pixelWidth)-1
            self.height = int(self._rawHeight / self._charHeight / self._pixelHeight)-1

        def getCenter(self):
            start = [int(self.width / 2), int(self.height / 2 + 0.5)]
            return tuple(start)

        def refresh(self):
            pass

        def clear(self, colour="\33[0m"):
            colour = EscSeq.GetColourValue(colour)
            self.texture.fill(colour)

        def paintPixels(self, point, colour, character=' '):
            rect = self.getRawRect(point, len(character))
            # if len(character) > 2:
            #     rect.width += int(len(character) / 2) * rect.width
            bgColour = EscSeq.GetColourValueBackground(colour)
            pygame.draw.rect(self.texture, bgColour, rect)
            if character != ' ':
                fgColour = EscSeq.GetColourValueForeground(colour)
                text_surface, text_rect = self.font.render(character, fgcolor=fgColour)
                dst_rect = pygame.Rect(rect.centerx - text_rect.width / 2,
                                       rect.centery - text_rect.height / 2,
                                       text_rect.width,
                                       text_rect.height
                                       )
                self.texture.blit(text_surface, dst_rect)

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

            width = (bottomRight[0] - topLeft[0])
            height = (bottomRight[1] - topLeft[1])

            startPoint = self.getRawPoint(topLeft)
            # startPoint = topLeft
            endPoint = (startPoint[0] + width, startPoint[1] + height)

            fillString = (fill * (int(width / len(fill) + 0.5) + 1))[0:width - len(line) + 1] if paintFill else fill

            if paintLine:
                for index in range(1, len(line) + 1):
                    self.paintPixels((startPoint[0], startPoint[1] + index - 1), lineColour,
                                     line[0:index] +
                                     line[index - 1:index] * ((width + 2) - (index * 2)) +
                                     line[0:index][::-1])

            for row in range(int(startPoint[1] + len(line)), int(endPoint[1] - len(line) + 1)):
                if paintLine:
                    self.paintPixels((startPoint[0], row), lineColour, line)
                if paintFill:
                    self.paintPixels((startPoint[0] + len(line), row), fillColour, fillString)
                if paintLine:
                    self.paintPixels((endPoint[0] + self._pixelWidth - len(line), row), lineColour, line[::-1])

            if paintLine:
                for index in range(1, len(line) + 1):
                    self.paintPixels((startPoint[0], endPoint[1] - index + 1), lineColour,
                                     line[0:index] +
                                     line[index - 1:index] * ((width + 2) - (index * 2)) +
                                     line[0:index][::-1])

        def getRawPoint(self, point):
            rawPoint = [point[0] * self._charWidth * self._pixelWidth, point[1] * self._charHeight * self._pixelHeight]
            return rawPoint

        def getRawRect(self, point, length):
            rawPoint = self.getRawPoint(point)
            return pygame.Rect(rawPoint[0], rawPoint[1], self._charWidth * length, self._charHeight)

        # @staticmethod
        # def flush():
        #     PygCanvas.display.fill((0, 0, 0))
        #     PygCanvas.display.blit(PygCanvas.texture, PygCanvas.texture.GetRect())
        #     pygame.display.flip()

        def flush(self):
            self.display.fill((0, 0, 0))
            self.display.blit(self.texture, self.texture.get_rect())
            pygame.display.flip()
