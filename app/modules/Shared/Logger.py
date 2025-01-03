from os import system, path
from config import LOGGER_PATH
from logging import getLogger, DEBUG, FileHandler, Formatter


class LoggerClass():
    def __init__(self):
        if not path.exists(LOGGER_PATH):
            system(f'touch {LOGGER_PATH}')

        self.logger = getLogger('APP')
        self.logger.setLevel(DEBUG)

        self._handler = FileHandler(LOGGER_PATH)
        self._handler.setLevel(DEBUG)

        self._formatter = Formatter('[%(name)s] - %(levelname)s - %(asctime)s - %(message)s')
        self._handler.setFormatter(self._formatter)
        self.logger.addHandler(self._handler)

    def getLogger(self):
        return self.logger


logger = LoggerClass().getLogger()
