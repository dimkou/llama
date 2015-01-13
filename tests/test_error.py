import unittest

from compiler import error


class TestLoggerMock(unittest.TestCase):
    """Test the API of the LoggerMock class."""

    @classmethod
    def setUpClass(cls):
        cls.logger_class = error.LoggerMock

    @classmethod
    def _make_logger(cls):
        return cls.logger_class()

    def setUp(self):
        self.logger = self._make_logger()

    def test_init(self):
        self.assertTrue(self.logger.perfect_success)

    def test_debug(self):
        self.logger.debug("This is debug message No %d", 42)
        self.assertTrue(self.logger.perfect_success)

    def test_info(self):
        self.logger.info("This is info message No %d", 42)
        self.assertTrue(self.logger.perfect_success)

    def test_warning(self):
        self.logger.warning("This is warning message No %d", 42)
        self.assertTrue(self.logger.success)
        self.assertFalse(self.logger.perfect_success)

    def test_error(self):
        self.logger.error("This is error message No %d", 42)
        self.assertFalse(self.logger.success)
        self.assertFalse(self.logger.perfect_success)

    def test_clear(self):
        self.logger.error("This is error message No %d", 42)
        self.logger.clear()
        self.assertTrue(self.logger.success)
        self.assertTrue(self.logger.perfect_success)

    def test_multiple_loggers(self):
        logger2 = self._make_logger()
        self.logger.error("This is error message No %d", 42)
        self.assertTrue(logger2.success)
        self.assertTrue(logger2.perfect_success)


class TestLogger(TestLoggerMock):
    """Test the API of the Logger class."""

    @classmethod
    def setUpClass(cls):
        cls.logger_class = error.Logger
