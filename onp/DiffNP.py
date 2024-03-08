from structs import (EditType, Block)

class DiffNP:
    def __init__(self, A, B):
        self.swapped = False
        self.A = A
        self.B = B
        self.M = len(A)
        self.N = len(B)
        if self.M > self.N:
            self.A, self.B = self.B, self.A
            self.M, self.N = self.N, self.M
            self.swapped = True

    def collect(self, k):
        v0 = self.fp[k - 1] + 1
        v1 = self.fp[k + 1]
        if v0 > v1:
            dir = 1
        else:
            dir = -1
        maxV = max(v0, v1)
        sn = self.snake(k, maxV)
        self.trace.append((k, sn, dir))
        return sn

    def snake(self, k, y):
        x = y - k
        while x < self.M and y < self.N and self.A[x] == self.B[y]:
            x += 1
            y += 1
        return y

    def compare(self):
        self.fp = [-1] * ((self.M + 1) + (self.N + 1) + 1)
        self.trace = []
        Delta = self.N - self.M
        p = -1
        while True:
            p += 1
            for k in range(-p, Delta):
                self.fp[k] = self.collect(k)
            for k in range(Delta + p, Delta, -1):
                self.fp[k] = self.collect(k)
            self.fp[Delta] = self.collect(Delta)
            if self.fp[Delta] == self.N:
                break

    def findMainTrace(self):
        mainTrace = []
        nextIdx = self.trace[-1][0]
        for tuple in reversed(self.trace):
            k = tuple[0]
            if k != nextIdx:
                continue
            dir = tuple[2]
            nextIdx = k - dir
            mainTrace.append(tuple)
        return list(reversed(mainTrace))

    def backtrack(self):
        mainPath = self.findMainTrace()
        result = []
        lastDir = 0
        lastX = -1
        lastY = -1
        insDelType = EditType.Equal
        start = [0, 0]
        for i in range(0, len(mainPath) - 1):
            tuple = mainPath[i]
            nextTuple = mainPath[i + 1]
            dir = nextTuple[2]
            k = tuple[0]
            y = tuple[1]
            x = y - k
            if dir != lastDir or y != lastY and x != lastX:
                if lastX == -1:  # empty mainPath
                    if x > 0:
                        result.append(Block(EditType.Equal, 0, 0, x, y))
                else:
                    result.append(Block(insDelType, start[0], start[1],
                                   lastX + (insDelType == EditType.Delete),
                                   lastY + (insDelType == EditType.Insert)))
                    eqLen = min(x - lastX, y - lastY)
                    if eqLen > 0:
                        result.append(Block(EditType.Equal, x - eqLen, y - eqLen, x, y))

                if dir < 0:
                    insDelType = EditType.Delete
                else:
                    insDelType = EditType.Insert
                start[0] = x
                start[1] = y
            lastDir = dir
            lastX = x
            lastY = y

        if insDelType != EditType.Equal:
            result.append(Block(insDelType, start[0], start[1],
                           lastX + (insDelType == EditType.Delete),
                           lastY + (insDelType == EditType.Insert)))

        endA = self.M == lastX
        endB = self.N == lastY
        if not endA and not endB and lastX >= 0:
            eqLen = min(self.M - lastX, self.N - lastY)
            result.append(Block(EditType.Equal, self.M - eqLen, self.N - eqLen, self.M, self.N))

        if not result and self.A == self.B:
            result.append(Block(EditType.Equal, 0, 0, self.M, self.N))

        return result

    def walk(self):
        self.compare()
        self.script = self.backtrack()
        return self.script
