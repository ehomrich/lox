from lox import expressions
from lox.tokens import Token, TokenType


class AstPrinter(expressions.ExprVisitor):
    def print(self, expr: expressions.Expr):
        return expr.accept(self)

    def parenthesize(self, name: str, *exprs: expressions.Expr) -> str:
        content = ' '.join(expr.accept(self) for expr in exprs)

        return f'({name} {content})'

    def visit_assign_expr(self, expr: expressions.Assign) -> str:
        return self.parenthesize('=', expr.name.lexeme, expr.value)

    def visit_binary_expr(self, expr: expressions.Binary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_call_expr(self, expr: expressions.Call) -> str:
        return self.parenthesize('call', expr.callee, expr.arguments)

    def visit_get_expr(self, expr: expressions.Get) -> str:
        return self.parenthesize('.', expr.obj, expr.name.lexeme)

    def visit_grouping_expr(self, expr: expressions.Grouping) -> str:
        return self.parenthesize('group', expr.expression)

    def visit_literal_expr(self, expr: expressions.Literal) -> str:
        return str(expr.value)

    def visit_logical_expr(self, expr: expressions.Logical) -> str:
        name = f'logical {expr.operator.lexeme}'
        return self.parenthesize(name, expr.left, expr.right)

    def visit_self_expr(self, expr: expressions.Self) -> str:
        return 'self'

    def visit_set_expr(self, expr: expressions.Set) -> str:
        return self.parenthesize('=', expr.obj, expr.name.lexeme, expr.value)

    def visit_super_expr(self, expr: expressions.Super) -> str:
        return self.parenthesize('super', expr.method)

    def visit_unary_expr(self, expr: expressions.Unary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def visit_variable_expr(self, expr: expressions.Variable) -> str:
        return expr.name.lexeme


if __name__ == '__main__':
    exp = expressions.Binary(
        expressions.Unary(
            Token(TokenType.MINUS, '-', '', 1),
            expressions.Literal(123)
        ),
        Token(TokenType.STAR, '*', '', 1),
        expressions.Grouping(expressions.Literal(45.67))
    )

    printer = AstPrinter()
    print(printer.print(exp))
