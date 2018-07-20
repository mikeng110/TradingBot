import sys
from Core.MainCore import StartProgram
from PyQt5.QtWidgets import QApplication

def main(argv):
    graphicMode = True

    if graphicMode:
        App = QApplication(sys.argv).instance()
        mainProgram = StartProgram(App)
        ret = App.exec()
        sys.exit(ret)

if __name__ == "__main__":
    main(sys.argv[1:])






