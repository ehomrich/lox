from typing import Any, List

from lox import expressions, statements
from lox.tokens import TokenType, Token


class LoxRuntimeError(RuntimeError):
    def __init__(self, token: Token, message: str) -> None:
        super().__init__(message)
        self.token = token

    def __str__(self) -> str:
        return super().__str__()

    def __repr__(self) -> str:
        return super().__repr__()


class Interpreter(expressions.ExprVisitor, statements.StmtVisitor):
    def evaluate(self, expr: expressions.Expr) -> Any:
        return expr.accept(self)

    def execute(self, stmt: statements.Stmt) -> None:
        stmt.accept(self)

    def interpret(self, stmts: List[statements.Stmt]) -> None:
        for stmt in stmts:
            self.execute(stmt)

    @staticmethod
    def stringify(obj: Any) -> str:
        if isinstance(obj, str):
            return obj

        if obj is None:
            return 'null'

        if isinstance(obj, bool):
            return str(obj).lower()

        return str(obj)

    @staticmethod
    def is_truthy(obj: Any) -> bool:
        return bool(obj)

    @staticmethod
    def is_equal(a: Any, b: Any) -> bool:
        return a == b

    @staticmethod
    def is_number(obj: Any) -> bool:
        return isinstance(obj, (int, float))

    def check_number_operand(self, operator: Token, operand: Any) -> None:
        if self.is_number(operand):
            return

        raise LoxRuntimeError(operator, 'Operand must be a numeric object.')

    def check_number_operands(self, operator: Token, left: Any, right: Any) -> None:
        if self.is_number(left) and self.is_number(right):
            return

        raise LoxRuntimeError(operator, 'Operands must be numeric objects.')

    def visit_expression_stmt(self, stmt: statements.Expression) -> None:
        self.evaluate(stmt.expression)

        return None

    def visit_print_stmt(self, stmt: statements.Print) -> None:
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))

        return None

    def visit_assign_expr(self, expr: expressions.Expr) -> Any:
        pass

    def visit_binary_expr(self, expr: expressions.Binary) -> Any:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        token_type = expr.operator.type

        if token_type == TokenType.BANG_EQUAL:
            return not self.is_equal(left, right)
        elif token_type == TokenType.EQUAL_EQUAL:
            return self.is_equal(left, right)
        elif token_type == TokenType.GREATER:
            self.check_number_operands(expr.operator, left, right)
            return left > right
        elif token_type == TokenType.GREATER_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return left >= right
        elif token_type == TokenType.LESS:
            self.check_number_operands(expr.operator, left, right)
            return left < right
        elif token_type == TokenType.LESS_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return left <= right
        elif token_type == TokenType.MINUS:
            self.check_number_operands(expr.operator, left, right)
            return left - right
        elif token_type == TokenType.PLUS:
            if (self.is_number(left) and self.is_number(right)) \
                    or (isinstance(left, str) and isinstance(right, str)):
                return left + right

            raise LoxRuntimeError(expr.operator,
                                  'Operands must be two strings or two numeric objects.')
        elif token_type == TokenType.SLASH:
            self.check_number_operands(expr.operator, left, right)
            return left / right
        elif token_type == TokenType.STAR:
            self.check_number_operands(expr.operator, left, right)
            return left * right

        return None

    def visit_call_expr(self, expr: expressions.Expr) -> Any:
        pass

    def visit_get_expr(self, expr: expressions.Expr) -> Any:
        pass

    def visit_grouping_expr(self, expr: expressions.Grouping) -> Any:
        return self.evaluate(expr.expression)

    def visit_literal_expr(self, expr: expressions.Literal) -> Any:
        return expr.value

    def visit_logical_expr(self, expr: expressions.Expr) -> Any:
        pass

    def visit_this_expr(self, expr: expressions.Expr) -> Any:
        pass

    def visit_set_expr(self, expr: expressions.Expr) -> Any:
        pass

    def visit_super_expr(self, expr: expressions.Expr) -> Any:
        pass

    def visit_unary_expr(self, expr: expressions.Unary) -> Any:
        right = self.evaluate(expr.right)

        if expr.operator.type == TokenType.BANG:
            return not self.is_truthy(right)
        elif expr.operator.type == TokenType.MINUS:
            self.check_number_operand(expr.operator, right)
            return -right

        return None

    def visit_variable_expr(self, expr: expressions.Expr) -> Any:
        pass
