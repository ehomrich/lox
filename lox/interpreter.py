from typing import Any, Union

from lox import expressions
from lox.tokens import TokenType


class Interpreter(expressions.ExprVisitor):
    def evaluate(self, expr: expressions.Expr) -> Any:
        return expr.accept(self)

    @staticmethod
    def is_truthy(obj: Any) -> bool:
        return bool(obj)

    @staticmethod
    def is_equal(a: Any, b: Any) -> bool:
        return a == b

    @staticmethod
    def is_number(obj: Any) -> bool:
        return isinstance(obj, (int, float))

    @staticmethod
    def coerce_number(obj: Any) -> Union[int, float]:
        value = float(obj)

        if value.is_integer():
            return int(value)

        return value

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
            return self.coerce_number(left) > self.coerce_number(right)
        elif token_type == TokenType.GREATER_EQUAL:
            return self.coerce_number(left) >= self.coerce_number(right)
        elif token_type == TokenType.LESS:
            return self.coerce_number(left) < self.coerce_number(right)
        elif token_type == TokenType.LESS_EQUAL:
            return self.coerce_number(left) <= self.coerce_number(right)
        elif token_type == TokenType.MINUS:
            return self.coerce_number(left) - self.coerce_number(right)
        elif token_type == TokenType.PLUS:
            if self.is_number(left) and self.is_number(right):
                return self.coerce_number(left) + self.coerce_number(right)
            elif isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)
        elif token_type == TokenType.SLASH:
            return self.coerce_number(left) / self.coerce_number(right)
        elif token_type == TokenType.STAR:
            return self.coerce_number(left) * self.coerce_number(right)

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

    def visit_self_expr(self, expr: expressions.Expr) -> Any:
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
            return -(self.coerce_number(right))

        return None

    def visit_variable_expr(self, expr: expressions.Expr) -> Any:
        pass
