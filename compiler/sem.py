"""
# ----------------------------------------------------------------------
# sem.py
#
# The Llama Semantic Analyzer
# http://courses.softlab.ntua.gr/compilers/2012a/llama2012.pdf
#
# Author: Nick Korasidis <renelvon@gmail.com>
# ----------------------------------------------------------------------
"""

# TODO Store Constraints
from compiler import ast, error, infer, symbol
from compiler import type as typeM


class Analyzer:
    """A semantic analyzer for Llama programs."""

    def __init__(self, logger=None):
        """Initialize a new Analyzer."""
        self.symbol_table = symbol.Table()
        self.type_table = typeM.Table()
        if logger is None:
            self.logger = error.Logger()
        else:
            self.logger = logger

        self._dispatcher = {
            ast.Program: self.analyze,
            ast.LetDef: self.analyze_letdef,
            ast.FunctionDef: self.analyze_function_def,
            ast.VariableDef: self.analyze_variable_def,
            ast.ArrayVariableDef: self.analyze_array_variable_def,
            ast.Param: self.analyze_param,
            ast.BinaryExpression: self.analyze_binary_expression,
            ast.UnaryExpression: self.analyze_unary_expression,
            ast.ConstructorCallExpression:
                self.analyze_constructor_call_expression,
            ast.ArrayExpression: self.analyze_array_expression,
            ast.ConstExpression: self.analyze_const_expression,
            ast.ConidExpression: self.analyze_conid_expression,
            ast.GenidExpression: self.analyze_genid_expression,
            ast.DeleteExpression: self.analyze_delete_expression,
            ast.DimExpression: self.analyze_dim_expression,
            ast.ForExpression: self.analyze_for_expression,
            ast.FunctionCallExpression:
                self.analyze_function_call_expression,
            ast.LetInExpression: self.analyze_let_in_expression,
            ast.IfExpression: self.analyze_if_expression,
            ast.MatchExpression: self.analyze_match_expression,
            ast.NewExpression: self.analyze_new_expression,
            ast.WhileExpression: self.analyze_while_expression,
            ast.Clause: self.analyze_clause,
            ast.Pattern: self.analyze_pattern,
            ast.GenidPattern: self.analyze_genid_pattern,

            list: self.analyze_typedef,  # TODO: Redo ast.TypeDef?
            # NOTE: Some ast nodes are omitted, as they are
            # processed elsewhere. These include type annotations as
            # well as type declarations.
        }

    def _dispatch(self, node):
        return self._dispatcher[type(node)](node)

    def _insert_symbols(self, symbols):
        for s in symbols:
            try:
                self.symbol_table.insert_symbol(s)
            except symbol.SymbolError as e:
                self.logger.error(str(e))

    def analyze(self, program):
        for definition in program:
            self._dispatch(definition)
        return program

    def analyze_letdef(self, letdef):
        scope = self.symbol_table.open_scope()
        if letdef.isRec:
            assert scope.visible, 'New scope is invisible.'
            self._insert_symbols(letdef)
        else:
            scope.visible = False

        for definition in letdef:
            self.analyze_definition(definition)

        if not letdef.isRec:
            scope.visible = True
            self._insert_symbols(letdef)

    def analyze_typedef(self, typedef):
        try:
            self.type_table.process(typedef)
        except typeM.InvalidTypeError as e:
            self.logger.error(str(e))

    def analyze_definition(self, definition):
        return self._dispatch(definition)

    def analyze_function_def(self, definition):
        scope = self.symbol_table.open_scope()
        assert scope.visible, 'New scope is invisible'
        self._insert_symbols(definition.params)
        self.analyze_expression(definition.body)
        self.symbol_table.close_scope()

    def analyze_variable_def(self, definition):
        pass

    def analyze_array_variable_def(self, definition):
        pass

    def analyze_param(self, param):
        pass

    def analyze_expression(self, expression):
        return self._dispatch(expression)

    def make_expression_temp_type(expression):
            return infer.TempType(expression, spec_type=expression.type)

    def analyze_unary_expression(self, expression):
        operator = expression.operator
        if operator == '!':
            value_temp_type = self.make_expression_temp_type(expression)
            temp_ref = ast.Ref(value_temp_type)
            infer.SpecConstraint(expression, value_temp_type)
            infer.SpecConstraint(expression.operand, temp_ref)
            infer.NegSetConstraint(expression.operand)
        elif operator in ('+', '-'):
            value_temp_type = self.make_expression_temp_type(expression)
            infer.SpecConstraint(value_temp_type, ast.Int())
            infer.AsOfTypeConstraint(expression, expression.operand)

    def analyze_bang_expression(self, expression):
        pass

    def analyze_sign_expression(self, expression):
        pass

    def analyze_binary_expression(self, expression):
        pass

    def analyze_constructor_call_expression(self, expression):
        pass

    def analyze_array_expression(self, expression):
        pass

    def analyze_const_expression(self, expression):
        pass

    def analyze_conid_expression(self, expression):
        pass

    def analyze_genid_expression(self, expression):
        pass

    def analyze_delete_expression(self, expression):
        pass

    def analyze_dim_expression(self, expression):
        pass

    def analyze_for_expression(self, expression):
        pass

    def analyze_function_call_expression(self, expression):
        pass

    def analyze_let_in_expression(self, expression):
        pass

    def analyze_if_expression(self, expression):
        pass

    def analyze_match_expression(self, expression):
        pass

    def analyze_new_expression(self, expression):
        pass

    def analyze_while_expression(self, expression):
        pass

    def analyze_clause(self, clause):
        pass

    def analyze_pattern(self, pattern):
        pass

    def analyze_genid_pattern(self, pattern):
        pass


def analyze(program, logger=None):
    """
    Analyze the given AST. Resolve names, infer and verify types
    and check for semantic errors. Return the annotated AST.
    For customised error reporting, provide a 'logger'.
    """
    analyzer = Analyzer(logger=logger)
    return analyzer.analyze(program)


def quiet_analyze(program):
    """
    Analyze the given AST. Resolve names, infer and verify types
    and check for semantic errors. Return the annotated AST.
    Explicitly silence errors/warnings.
    """
    return analyze(program, logger=error.LoggerMock())
