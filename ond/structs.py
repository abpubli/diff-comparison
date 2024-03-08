from enum import Enum


class EditType(Enum):
    Insert = 1
    Delete = -1
    Equal = 0


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Box:
    def __init__(self, px=0, py=0, x=0, y=0):
        self.startX = px
        self.startY = py
        self.endX = x
        self.endY = y

    def width(self):
        return self.endX - self.startX

    def height(self):
        return self.endY - self.startY

    def size(self):
        return self.width() + self.height()

    def delta(self):
        return self.width() - self.height()

    def changeStart(self, snake):
        return Box(snake.endX, snake.endY, self.endX, self.endY)

    def changeFinish(self, snake):
        return Box(self.startX, self.startY, snake.startX, snake.startY)

    def start(self):
        return Point(self.startX, self.startY)

    def finish(self):
        return Point(self.endX, self.endY)


class Block:
    def __init__(self, type, startX, startY, endX, endY):
        self.type = type
        self.startX = startX
        self.startY = startY
        self.endX = endX
        self.endY = endY

    def make_union(self, block):
        self.startX = min(self.startX, block.startX)
        self.startY = min(self.startY, block.startY)
        self.endX = max(self.endX, block.endX)
        self.endY = max(self.endY, block.endY)

