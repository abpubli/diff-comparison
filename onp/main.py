from DiffNP import DiffNP
from Printer import Printer

if __name__ == '__main__':
    diff = DiffNP("ABCABBA", "CBABAC")
    printer = Printer(diff)
    printer.printAlign()
