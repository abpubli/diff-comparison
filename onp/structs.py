from enum import Enum

class EditType(Enum):
    Insert = 1
    Delete = -1
    Equal = 0


class Block:
    def __init__(self, type, startX, startY, endX, endY):
        self.type = type
        self.startX = startX
        self.startY = startY
        self.endX = endX
        self.endY = endY
