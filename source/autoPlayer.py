from source.escSeq import EscSeq
from source.player import Player
from source.point import getNextPoint, calculateDirection, getManhattenDistance, getSurroundingPoints
import time
from source.canvas import flush


class AutoPlayer(Player):
    def __init__(self, parent, index):
        self.closedList: set = set()
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

        if self._direction in new_direction[0]:
            if self.isDirectionValid(self._direction):
                next_point = getNextPoint(position, self._direction)
                if self.parent.isPointValid(next_point) and not self.parent.isPointInUse(next_point):
                    if next_point in self.closedList:
                        return

        for direction_lists in new_direction:
            for direction_list in direction_lists:
                for direction in direction_list:
                    if self.isDirectionValid(direction):
                        next_point = getNextPoint(position, direction)
                        if self.parent.isPointValid(next_point) and not self.parent.isPointInUse(next_point):
                            if next_point in self.closedList:
                                self._pending_direction.append(direction)
                                return

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
        next_point = getNextPoint(position, direction)
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

        for pixel in self.closedList:
            self.parent.canvas.paintPixels(pixel, EscSeq.CEND, '  ')
        self.closedList = self.getShortestPath(position, closest_bite[1])
        for bite in self.parent.bites:
            self.parent.canvas.paintPixels(bite, EscSeq.CREDBG2, '  ')
        self.parent.canvas.paintPixels(position, self.colourHead, '^^')
        flush()
        # time.sleep(10)
        return calculateDirection(position, closest_bite[1])

    def getShortestPath(self, start, destination):
        openList = {}
        closedList: set = set()
        # openList[start] = [start, getManhattenDistance(start, destination), 0]
        currentPointObject = [start, getManhattenDistance(start, destination), 0]
        openList[start] = currentPointObject

        while len(openList) != 0:
            # currentPointObject = min(openList.items(), key=lambda x: x[1][1])

            lowestPointObject = min(openList.items(), key=lambda x: x[1][1])[1]
            if currentPointObject and currentPointObject[1] == lowestPointObject[1]:
                currentPoint = currentPointObject[0]
                steps = currentPointObject[2] + 1
            else:
                currentPoint = lowestPointObject[0]
                steps = lowestPointObject[2] + 1

            currentPointObject = None

            # self.parent.debug("Obj:", str(currentPoint) + " - " + str(steps))
            # flush()
            # time.sleep(100)
            closedList.add(currentPoint)
            openList.pop(currentPoint)
            # if steps < 100:
            #     self.parent.canvas.paint_pixel(currentPoint, EscSeq.CGREYBG, str(steps))
            # distance = getManhattenDistance(currentPoint, destination)
            # if distance < 100:
            #     # self.parent.canvas.paint_pixel(currentPoint, EscSeq.CGREYBG, str(int(distance)).format())
            #     self.parent.canvas.paint_pixel(currentPoint, EscSeq.CGREYBG, f"{distance:}"[0:2])
            # else:
            self.parent.canvas.paintPixels(currentPoint, EscSeq.CGREYBG, 'XX')

            if destination in closedList:
                break

            adjacentPoints = []
            for point in getSurroundingPoints(currentPoint):
                if self.parent.isFuturePointFree(point, steps, self) and point not in closedList:
                    adjacentPoints.append(point)
                    if self.checkPointSurroundings(point, steps, closedList):
                        adjacentPoints.append(point)
                    else:
                        if not self.checkForClosedloop(point, steps, closedList):
                            adjacentPoints.append(point)

            if destination in adjacentPoints:
                closedList.add(destination)
                break

            for point in adjacentPoints:
                if point in closedList:
                    continue

                score = steps + getManhattenDistance(point, destination)
                if not self.checkPointSurroundings(point, steps, closedList):
                    score += score + 1  # Check for closed loop instead

                if not currentPointObject or score < currentPointObject[1]:
                    currentPointObject = [point, score, steps]

                if point not in openList:
                    openList[point] = [point, score, steps]
                else:
                    if score < openList[point][1]:
                        openList[point] = [point, score, steps]

        # self.parent.debug("ResultLength: ", len(closedList))
        return closedList

    def checkPointSurroundings(self, point, steps, closedList):
        for futurePoint in getSurroundingPoints(point):
            if futurePoint != self.current_snake[len(self.current_snake) - 1] \
                    and not self.parent.isFuturePointFree(futurePoint, steps, self):
                return False
            elif futurePoint in closedList:
                return False
        return True

    def checkForClosedloop(self, point, steps, closedList):
        return False
