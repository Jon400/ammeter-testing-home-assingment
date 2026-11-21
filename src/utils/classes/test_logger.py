import logging


class TestLogger:
    def __init__(self, test_name: str, log_file: str, log_level: str = "DEBUG"):
        self._test_name = test_name
        self._log_file = log_file
        self._log_level = log_level
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """
        Set up the logger with a custom format, writing to the log file and to the console.
        """
        logger = logging.getLogger(f"test_{self._test_name}")
        logger.setLevel(self._log_level)
        logger.handlers.clear()  # don't add the handlers twice if the same test runs again

        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

        file_handler = logging.FileHandler(self._log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        return logger

    def info(self, message: str):
        self.logger.info(message)

    def error(self, message: str):
        self.logger.error(message)

    def debug(self, message: str):
        self.logger.debug(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def close(self):
        """Close the log file. Call it when the test is done."""
        for handler in self.logger.handlers:
            handler.close()
        self.logger.handlers.clear()
