import sys

from Controllers.main_cont import *
from Views.main_view import *
from Model.model import *


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.model = Model()
        self.main_ctrl = MainController(self, self.model)
        self.main_view = MainView(self.model, self.main_ctrl)
        self.main_view.show()


def main(argv):
    graphics = True

    if graphics:
        graphic_mode()
    else:
        console_mode()


def graphic_mode():
    app = App(sys.argv)
    sys.exit(app.exec_())


def console_mode():
    pass


if __name__ == "__main__":
    main(sys.argv[1:])






