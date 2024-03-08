import copy
from structs import (EditType, Block)

class DiffND:
    def __init__(self, A, B):
        self.A = A
        self.B = B
        self.M = len(A)
        self.N = len(B)

    def forward(self, d):
        for k in range(-d, d + 1, 2):
            if k == -d or (k != d and self.v[k - 1] < self.v[k + 1]):
                x = self.v[k + 1]
            else:
                x = self.v[k - 1] + 1
            y = x - k
            while x < self.M and y < self.N and self.A[x] == self.B[y]:
                x += 1
                y += 1

            self.v[k] = x
            if x >= self.M and y >= self.N:
                return True
        return False

    def compare(self):
        Max = self.M + self.N
        self.v = [0] * (2 * Max + 1)
        self.trace = []
        for d in range(0, Max + 1):
            if self.forward(d):
                self.trace.append(copy.copy(self.v))
                return
            self.trace.append(copy.copy(self.v))

    def add_to_list(self, list, block):
        if not list:
            list.append(block)
        else:
            last = list[-1]
            if last.type != block.type:
                list.append(block)
            else:
                last.make_union(block)

    def backtrack(self):
        script = []
        x = self.M
        y = self.N
        for d in range(len(self.trace) - 1, -1, -1):
            v = self.trace[d]
            k = x - y
            if k == -d or (k != d and v[k - 1] < v[k + 1]):
                prev_k = k + 1
            else:
                prev_k = k - 1
            prev_x = v[prev_k]
            prev_y = prev_x - prev_k

            if x > prev_x and y > prev_y:
                diagLen = min(x - prev_x, y - prev_y)
                block = Block(EditType.Equal, x - diagLen, y - diagLen, x, y)
                self.add_to_list(script, block)
                x -= diagLen
                y -= diagLen

            if d > 0:
                if prev_x == x:
                    block= Block(EditType.Insert, prev_x, prev_y, x, y)
                    self.add_to_list(script, block)
                else:
                    block = Block(EditType.Delete, prev_x, prev_y, x, y)
                self.add_to_list(script, block)

            x = prev_x
            y = prev_y

        return script

    def walk(self):
        self.compare()
        self.script = self.backtrack()
        self.script = list(reversed(self.script))
        return self.script
