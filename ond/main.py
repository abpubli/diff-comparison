from DiffND import DiffND
from DiffLinearND import DiffLinearND
from Printer import Printer

if __name__ == '__main__':
    diff = DiffND("ABCABBA", "CBABAC")
    printer = Printer(diff)
    printer.printAlign()

    diff = DiffLinearND("ABCABBA", "CBABAC")
    printer = Printer(diff)
    printer.printAlign()
