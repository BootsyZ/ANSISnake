from source.canvas import Canvas
from source.pygCanvas import PygCanvas


class MultiCanvas:
    __instance = None

    def __init__(self, parent):
        if MultiCanvas.__instance is None:
            MultiCanvas.__instance = MultiCanvas.__Canvas(parent)

        self.__dict__['_Canvas__instance'] = MultiCanvas.__instance

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)

    class __Canvas:

        def __init__(self, parent):
            self.pygCanvas = PygCanvas(parent)
            self.canvas = Canvas(parent)
            self.width = self.pygCanvas.width
            self.height = self.pygCanvas.height
            self._rawWidth = self.pygCanvas._rawWidth
            self._rawHeight = self.pygCanvas._rawHeight

        def eventLoop(self):
            self.pygCanvas.eventLoop()

        def getCenter(self):
            return self.pygCanvas.getCenter()

        def refresh(self):
            self.canvas.refresh()
            self.pygCanvas.refresh()

        def clear(self, colour="\33[0m"):
            self.canvas.clear(colour)
            self.pygCanvas.clear(colour)

        def paintPixels(self, point, colour, character=' '):
            self.canvas.paintPixels(point, colour, character)
            self.pygCanvas.paintPixels(point, colour, character)

        def paintRect(self, **kwargs):
            self.canvas.paintRect(**kwargs)
            self.pygCanvas.paintRect(**kwargs)

        # def getRawPoint(self, point):
        #     return self.pygCanvas.getRawPoint(point)
        #
        # def getRawRect(self, point, length):
        #     return self.pygCanvas.getRawRect(point, length)

        def flush(self):
            self.canvas.flush()
            self.pygCanvas.flush()
