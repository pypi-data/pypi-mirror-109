import logging, sys
from datetime import datetime

class MyLogger(logging.Logger):
    """ A simply callable logger class, put inside modules to minimize dependecies """

    def __init__(self, name):
        super().__init__(name, level=logging.DEBUG)
        self.start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.name = name
        self.handler = logging.StreamHandler(sys.stdout)
        self.handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        self.handler.setFormatter(formatter)
        self.addHandler(self.handler)
        self.setFile(file=f"./data/logs/{self.start_time}_{self.name}_logs.txt")

    def _log(self, level, msg, *args, **kwargs):
        """ Can modify all error messages """
        super()._log(level, msg, *args, **kwargs)

    def setLevel(self, level):
        """ For streaming to console """
        level = level.lower()
        if level == "debug":
            self.handlers[0].setLevel(logging.DEBUG)
        elif level == "info":
            self.handlers[0].setLevel(logging.INFO)
        elif level == "warning":
            self.handlers[0].setLevel(logging.WARNING)
        elif level == "error":
            self.handlers[0].setLevel(logging.ERROR)

    def setFile(self, file):
        self.handlers = []
        fh = logging.FileHandler(file)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        self.addHandler(self.handler)
        self.addHandler(fh)

log = MyLogger('OP')