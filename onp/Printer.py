from DiffNP import DiffNP, EditType, Block


class Printer:
    def __init__(self, diff):
        self.diff = diff
        self.swapped = diff.swapped

    def alignBlock(self, block, text, number):
        type = block.type
        if number == 1:
            if type == EditType.Insert:
                type = EditType.Delete
            elif type == EditType.Delete:
                type = EditType.Insert
            block = Block(type, block.startY, block.startX, block.endY, block.endX)

        result = " "
        if type == EditType.Insert:
            for y in range(block.startY, block.endY):
                result += "-"
        else:
            for x in range(block.startX, block.endX):
                result += text[x]
        return result

    def alignOne(self, script, text, number):
        result = ""
        for block in script:
            result += self.alignBlock(block, text, number)
        return result

    def alignString(self, script):
        if self.diff.swapped:
            return self.alignOne(script, self.diff.B, 1) + '\n' + self.alignOne(script, self.diff.A, 0)
        else:
            return self.alignOne(script, self.diff.A, 0) + '\n' + self.alignOne(script, self.diff.B, 1)

    def printAlign(self):
        script = self.diff.walk()
        print(self.alignString(script))