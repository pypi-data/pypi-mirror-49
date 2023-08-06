import os
import datetime
from granate.utils import name

class Printer:
    def __init__(self, trace_file=os.getpid()):
        """

        :param trace_file:
        """
        self.trace_file = trace_file
        self.name = name(self.trace_file)

    def __call__(self, str):
        print("{} | {} >> {}".format(datetime.datetime.now(), self.name, str))
        with open(self.trace_file, "a") as f:
            f.write("{}\n".format(str))
