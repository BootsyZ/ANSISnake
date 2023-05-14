from source.escSeq import EscSeq
from source.player import Player
from source.point import GetPointFromDirection, calculateDirection, getManhattenDistance, getSurroundingPoints, \
    getAllSurroundingPoints, GetDirectionFromPoint
import time
from source.canvas import flush


class AutoPlayer(Player):
    def __init__(self, parent, index):
        self.shortestPath: list = list()
        super().__init__(parent, index)

    def getDirection(self):
        if len(self._pending_direction) < 1:
            self.setAutoDirection()
        return super().getDirection()

    def setAutoDirection(self):
        new_direction = self.getAutoDirection()
        position = self.current_snake[len(self.current_snake) - 1]

        # debugstring = self._direction + "-" + str(new_direction)
        # if self.index == 0:
        #     self.parent.debug1(debugstring)
        # elif self.index == 1:
        #     self.parent.debug2(debugstring)
        # elif self.index == 2:
        #     self.parent.debug3(debugstring)
        # elif self.index == 3:
        #     self.parent.debug4(debugstring)

        # if len(self.closedList) > 0:
        #     if self.parent.isPointValid(self.closedList[0]) and not self.parent.isPointInUse(self.closedList[0]):
        #         self._pending_direction.append(
        #             GetDirectionFromPoint(self.current_snake[len(self.current_snake) - 1], self.closedList[0])
        #         )
        #         return

        if self._direction in new_direction[0]:
            if self.isDirectionValid(self._direction):
                next_point = GetPointFromDirection(position, self._direction)
                if self.parent.isPointValid(next_point) and not self.parent.isPointInUse(next_point):
                    if next_point in self.shortestPath:
                        return

        for direction_lists in new_direction:
            for direction_list in direction_lists:
                for direction in direction_list:
                    if self.isDirectionValid(direction):
                        next_point = GetPointFromDirection(position, direction)
                        if self.parent.isPointValid(next_point) and not self.parent.isPointInUse(next_point):
                            if next_point in self.shortestPath:
                                self._pending_direction.append(direction)
                                return

        # for point in getSurroundingPoints(self.current_snake[len(self.current_snake) - 1]):
        #     if self.parent.isPointValid(point) and not self.parent.isPointInUse(point):
        #         self._pending_direction.append(
        #             GetDirectionFromPoint(self.current_snake[len(self.current_snake) - 1], point)
        #         )
        #         return

    # for steps in range(16, 0, -1):
    #     for direction_lists in new_direction:
    #         for direction_list in direction_lists:
    #             for direction in direction_list:
    #                 if self.isDirectionValid(direction):
    #                     next_point = getNextPoint(position, direction)
    #                     if self.parent.isPointValid(next_point) and not self.parent.isPointInUse(next_point):
    #                         if self.isNotDumb(next_point, direction, steps):
    #                             self._pending_direction.append(direction)
    #                             return
    # self._pending_direction.append(new_direction[0][0])

    def isNotDumb(self, position, direction, run):
        run -= 1
        next_point = GetPointFromDirection(position, direction)
        if self.parent.isPointFree(next_point):
            if run > 0 and next_point not in self.parent.bites:
                return self.isNotDumb(next_point, direction, run)
            else:
                return True
        else:
            return False

    def getAutoDirection(self):
        biteSet = self.parent.bites
        position = self.current_snake[len(self.current_snake) - 1]
        iterator = iter(biteSet)
        bitelist = []
        for _ in range(len(biteSet)):
            bite = next(iterator)
            bitelist.append((getManhattenDistance(position, bite), bite))
        bitelist.sort(key=lambda x: x[0])
        closest_bite = bitelist[0]

        for pixel in self.shortestPath:
            self.parent.canvas.paintPixels(pixel, EscSeq.CEND, '  ')
        self.shortestPath = self.getShortestPath(position, closest_bite[1])
        for bite in self.parent.bites:
            self.parent.canvas.paintPixels(bite, EscSeq.CREDBG2, '  ')
        self.parent.canvas.paintPixels(position, self.colourHead, '^^')
        flush()
        # time.sleep(10)
        return calculateDirection(position, closest_bite[1])

    def getShortestPath(self, start, destination):
        openList = {}
        closedList = {}
        currentPointObject = [None, getManhattenDistance(start, destination), 0]
        openList[start] = currentPointObject

        while len(openList) != 0:
            lowestPointObject = min(openList.items(), key=lambda x: x[1][1])
            currentPoint = lowestPointObject[0]
            currentPointObject = lowestPointObject[1]
            steps = currentPointObject[2] + 1

            closedList[currentPoint] = currentPointObject
            openList.pop(currentPoint)

            adjacentPoints = []
            for point in getSurroundingPoints(currentPoint):
                if self.parent.isFuturePointFree(point, steps, self) and point not in closedList:
                    adjacentPoints.append(point)

            # We found a path!
            if destination in adjacentPoints:
                closedList[destination] = [currentPoint, getManhattenDistance(start, destination), steps]
                break

            for point in adjacentPoints:
                if point in closedList:
                    continue

                score = steps + getManhattenDistance(point, destination)
                score += self.checkPointSurroundings(point, steps)

                if point in openList:
                    if score < openList[point][1]:
                        openList[point] = [currentPoint, score, steps]
                else:
                    openList[point] = [currentPoint, score, steps]

        path = []
        try:
            current = destination
            currentObject = closedList[destination]
            while current is not None:
                self.parent.canvas.paintPixels(current, EscSeq.CGREYBG, 'XX')
                path.append(current)
                current = currentObject[0]
                if current is not None:
                    currentObject = closedList[current]
        except KeyError:
            # return [start]
            pass
        return path[::-1]  # Return reversed path

    def checkPointSurroundings(self, point, steps):
        # for futurePoint in getAllSurroundingPoints(point):
        value = 0
        for futurePoint in getSurroundingPoints(point):
            if futurePoint != self.current_snake[len(self.current_snake) - 1] \
                    and not self.parent.isFuturePointFree(futurePoint, steps, self):  # or instead of and?
                value += 1
        return value

    def checkForClosedloop(self, point, steps, closedList):
        for x in getSurroundingPoints(point):
            if x in self.current_snake or x in closedList:
                return True
        return False
