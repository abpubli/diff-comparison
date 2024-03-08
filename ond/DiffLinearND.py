from structs import (EditType, Block, Box)

class DiffLinearND:
    def __init__(self, A, B):
        self.A = A
        self.B = B
        self.M = len(A)
        self.N = len(B)

    def add_to_list(self, list, block):
        if not list:
            list.append(block)
        else:
            last = list[-1]
            if last.type != block.type:
                list.append(block)
            else:
                last.make_union(block)

    def forward(self, box, vf, vb, d):
        for k in range(d, -d - 1, -2):
            c = k - box.delta()
            if k == -d or (k != d and vf[k - 1] < vf[k + 1]):
                x = vf[k + 1]
                px = x
            else:
                x = vf[k - 1] + 1
                px = x - 1

            y = box.startY + (x - box.startX) - k
            py = y if d == 0 or x != px else y - 1

            while x < box.endX and y < box.endY and self.A[x] == self.B[y]:
                x += 1
                y += 1

            vf[k] = x

            if box.delta() % 2 != 0 and c >= -(d - 1) and c <= d - 1 and y >= vb[c]:
                snake = Box(px, py, x, y)
                return snake
        return None

    def backward(self, box, vf, vb, d):
        for c in range(d, -d - 1, -2):
            k = c + box.delta()
            if c == -d or (c != d and vb[c - 1] > vb[c + 1]):
                py = y = vb[c + 1]
            else:
                py = vb[c - 1]
                y = py - 1

            x = box.startX + (y - box.startY) + k
            px = x if d == 0 or y != py else x + 1

            while x > box.startX and y > box.startY and self.A[x - 1] == self.B[y - 1]:
                x -= 1
                y -= 1

            vb[c] = y

            if box.delta() % 2 == 0 and k >= -d and k <= d and x <= vf[k]:
                snake = Box(x, y, px, py)
                return snake
        return None

    def middleSnake(self, box):
        if box.size()==0:
            return None
        # round up box.size()/2
        max = (box.size()+1) // 2
        vf = [0] * (2 * max + 1)
        vf[1] = box.startX
        vb = [0] * (2 * max + 1)
        vb[1] = box.endY

        for d in range(0, max+1):
            forwardSnake = self.forward(box, vf, vb, d)
            if forwardSnake is not None:
                return forwardSnake

            backwardSnake = self.backward(box, vf, vb, d)
            if backwardSnake is not None:
                return backwardSnake
        return None

    def find_path(self, cpos):
        snake = self.middleSnake(cpos)
        if snake is None:
            return []
        
        head = self.find_path(cpos.changeFinish(snake))
        tail = self.find_path(cpos.changeStart(snake))
        if not head:
            head.append(snake.start())
        if not tail:
            tail.append(snake.finish())

        list = head + tail
        return list

    def compare(self):
        self.path = self.find_path(Box(0, 0, self.M, self.N))


    def backtrack(self):
        self.script = []
        if not self.path:
            return []
        for i in range(len(self.path) - 1):
            point0 = self.path[i]
            point1 = self.path[i + 1]

            if point0.x < point1.x and point0.y < point1.y and self.A[point0.x] == self.B[point0.y]:
                diagLen = min(point1.x - point0.x, point1.y - point0.y)
                block = Block(EditType.Equal, point0.x, point0.y, point0.x + diagLen, point0.y + diagLen)
                self.add_to_list(self.script, block)
                point0.x += diagLen
                point0.y += diagLen

            diff = (point1.x - point0.x) - (point1.y - point0.y)
            if diff == -1:
                block = Block(EditType.Insert, point0.x, point0.y, point0.x, point0.y + 1)
                self.add_to_list(self.script, block)
                point0.y += 1
            elif diff == 1:
                block = Block(EditType.Delete, point0.x, point0.y, point0.x + 1, point0.y)
                self.add_to_list(self.script, block)
                point0.x += 1

            if point0.x < point1.x and point0.y < point1.y and self.A[point0.x] == self.B[point0.y]:
                diagLen = min(point1.x - point0.x, point1.y - point0.y)
                block = Block(EditType.Equal, point0.x, point0.y, point0.x + diagLen, point0.y + diagLen)
                self.add_to_list(self.script, block)

    def walk(self):
        self.compare()
        script = self.backtrack()
        script = list(reversed(self.script))
        return script
