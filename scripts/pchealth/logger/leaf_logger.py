
import logging

from enum import Enum

class level(Enum):
    """Enum for the different logging levels."""
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

class appLogger( logging.Logger ):
    """
    Class that overrides the default Logeer class in python.
    
    It provides the basic configuration of a log file for our project.

    :param name: The name of the file to which you would like to output to.
    :type logging: str

    :param min_logger_level: The minimum debug level for this object.,
        Defaults to level.DEBUG
    :type logging: level

    :param format: The format of the data you want to log.
    :type logging: str
    """

    def __init__(self, name, min_logger_level=level.DEBUG, format="%(asctime)s-[%(levelname)s]:%(message)s"):
        
        super().__init__(name)
        
        self.setLevel(min_logger_level)
        
        formatter = logging.Formatter("%(asctime)s-[%(levelname)s]:%(message)s")

        fileHandler = logging.FileHandler(name+".log")
        fileHandler.setFormatter(formatter)

        self.addHandler(fileHandler)

if __name__ == "__main__":

    logger = appLogger(__name__)

    logger.debug("This is a DEBUG")
    logger.info("This is an INFO")
    logger.warning("This is a Warning")
    logger.error("This is an error")
    logger.critical("This is a Critical")