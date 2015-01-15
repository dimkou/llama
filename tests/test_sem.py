import unittest

from compiler import error, parse, sem

# pylint: disable=no-member


class TestAnalyzer(unittest.TestCase):
    """Test the semantic analyzer."""

    def setUp(self):
        self.logger = error.LoggerMock()
        self.analyzer = sem.Analyzer(logger=self.logger)

    def test_init(self):
        self.analyzer.should.have.property("symbol_table")
        self.analyzer.should.have.property("type_table")
        self.analyzer.should.have.property("logger").being(self.logger)

    def test_analyze(self):
        simple_ast = parse.quiet_parse("let x = 42")
        self.analyzer.analyze(simple_ast)


class TestSemModuleAPI(unittest.TestCase):
    """Test API of the sem module."""

    def setUp(self):
        self.ast = parse.quiet_parse("let x = 42")

    def test_analyze_logger(self):
        sem.analyze(self.ast, logger=error.LoggerMock())

    def test_analyze_no_logger(self):
        sem.analyze(self.ast)

    def test_quiet_analyze(self):
        sem.quiet_analyze(self.ast)
