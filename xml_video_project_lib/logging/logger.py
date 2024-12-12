import logging
import sys
from pathlib import Path
from xml_video_project_lib.config import config  # Import the config instance

class SingletonMeta(type):
    """
    A thread-safe implementation of Singleton.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Logger(metaclass=SingletonMeta):
    """
    Singleton Logger class to handle logging across the library.
    """
    def __init__(self):
        self.logger = logging.getLogger("xml_video_project_lib")
        if not self.logger.handlers:
            self._configure_logger()

    def _configure_logger(self):
        """
        Configures the logger with handlers and formatters.
        """
        # Set the default logging level
        log_level = config.get('Logging', 'level', fallback='INFO').upper()
        self.logger.setLevel(getattr(logging, log_level, logging.INFO))

        # Create console handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(getattr(logging, log_level, logging.INFO))

        # Create formatter
        log_format = config.get('Logging', 'format', fallback='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        formatter = logging.Formatter(log_format)

        # Add formatter to handlers
        ch.setFormatter(formatter)

        # Add handlers to the logger
        self.logger.addHandler(ch)

    def get_logger(self):
        """
        Returns the configured logger instance.
        """
        return self.logger

# Instantiate the Logger singleton
logger_instance = Logger()
logger = logger_instance.get_logger()