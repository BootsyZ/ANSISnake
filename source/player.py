import copy
from source.escSeq import EscSeq


class Player:
    def __init__(self, parent, index):
        self.parent = parent
        self.index = index
        self.colour = self.getColour(index)
        self.colourHead = self.getColourHead(index)
        self._direction, self._pending_direction = self.getStartDirection(index), [self.getStartDirection(index)]
        self.current_snake: list = parent.init_snake()

    def getDirection(self):
        try:
            self._direction = self._pending_direction.pop(0)
        except IndexError:
            pass
        return self._direction

    def isDirectionValid(self, direction):
        current_direction = self._direction if len(self._pending_direction) == 0 else self._pending_direction[0]
        if direction == 'n' and current_direction != 's' \
                or direction == 'e' and current_direction != 'w' \
                or direction == 's' and current_direction != 'n' \
                or direction == 'w' and current_direction != 'e':
            return True
        else:
            return False

    def setDirection(self, direction):
        if len(self._pending_direction) <= 1:
            try:
                if self.isDirectionValid(direction):
                    if len(self._pending_direction) == 0:
                        self._pending_direction = list(direction)
                    elif len(self._pending_direction) == 1:
                        new_pending_direction = copy.copy(self._pending_direction)
                        new_pending_direction.append(direction)
                        self._pending_direction = new_pending_direction
                else:
                    raise ValueError
            except ValueError:
                return False
            else:
                return True

    def getStartPosition(self, index):
        return self.parent.center

    @staticmethod
    def getColour(index):
        if index == 0:
            return EscSeq.CGREENBG2
        elif index == 1:
            return EscSeq.CBLUEBG2
        elif index == 2:
            return EscSeq.CVIOLETBG2
        elif index == 3:
            return EscSeq.CYELLOWBG2
        else:
            return EscSeq.CGREYBG

    @staticmethod
    def getColourHead(index):
        if index == 0:
            return EscSeq.CGREENBG
        elif index == 1:
            return EscSeq.CBLUEBG
        elif index == 2:
            return EscSeq.CVIOLETBG
        elif index == 3:
            return EscSeq.CYELLOWBG
        else:
            return EscSeq.CGREYBG

    @staticmethod
    def getStartDirection(index):
        if index == 0:
            return 'e'
        elif index == 1:
            return 'w'
        elif index == 2:
            return 'n'
        elif index == 3:
            return 's'
        else:
            return None
