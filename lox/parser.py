from typing import List, Optional

from lox import expressions, statements
from lox.tokens import Token, TokenType


class ParseError(RuntimeError):
    def __init__(self, token: Token, message: str) -> None:
        super().__init__(message)
        self.token = token


class Parser:
    def __init__(self, tokens: List[Token]) -> None:
        self.tokens = tokens
        self.current = 0

    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF

    def previous(self) -> Optional[Token]:
        return self.tokens[self.current - 1]

    def next(self) -> Token:
        if self.is_at_end():
            raise EOFError('End of file, cannot get next token.')

        return self.tokens[self.current + 1]

    def check(self, typ: TokenType) -> bool:
        if self.is_at_end():
            return False

        return self.peek().type == typ

    def advance(self) -> Optional[Token]:
        if not self.is_at_end():
            self.current += 1

        return self.previous()

    def peek(self) -> Token:
        return self.tokens[self.current]

    def match(self, *types: TokenType) -> bool:
        for typ in types:
            if self.check(typ):
                self.advance()
                return True

        return False

    @staticmethod
    def error(token: Token, message: str) -> ParseError:
        return ParseError(token, message)

    def consume(self, typ: TokenType, message: str) -> Token:
        if self.check(typ):
            return self.advance()

        raise self.error(self.peek(), message)

    def expression(self) -> expressions.Expr:
        return self.equality()

    def statement(self) -> statements.Stmt:
        if self.match(TokenType.PRINT):
            return self.print_statement()

        return self.expression_statement()

    def print_statement(self) -> statements.Stmt:
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")

        return statements.Print(value)

    def expression_statement(self) -> statements.Stmt:
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")

        return statements.Expression(expr)

    def assignment(self) -> expressions.Expr:
        pass

    def equality(self) -> expressions.Expr:
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = expressions.Binary(expr, operator, right)

        return expr

    def comparison(self) -> expressions.Expr:
        expr = self.addition()

        while self.match(
                TokenType.GREATER,
                TokenType.GREATER_EQUAL,
                TokenType.LESS,
                TokenType.LESS_EQUAL
        ):
            operator = self.previous()
            right = self.comparison()
            expr = expressions.Binary(expr, operator, right)

        return expr

    def primary(self) -> expressions.Expr:
        if self.match(TokenType.FALSE):
            return expressions.Literal(False)
        elif self.match(TokenType.TRUE):
            return expressions.Literal(True)
        elif self.match(TokenType.NULL):
            return expressions.Literal(None)

        if self.match(
                TokenType.INTEGER,
                TokenType.FLOAT,
                TokenType.STRING
        ):
            return expressions.Literal(self.previous().literal)

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return expressions.Grouping(expr)

        raise self.error(self.peek(), 'Expect expression.')

    def unary(self) -> expressions.Expr:
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()

            return expressions.Unary(operator, right)

        return self.primary()

    def binary(self) -> expressions.Expr:
        pass

    def addition(self) -> expressions.Expr:
        expr = self.multiplication()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.multiplication()
            expr = expressions.Binary(expr, operator, right)

        return expr

    def multiplication(self) -> expressions.Expr:
        expr = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = expressions.Binary(expr, operator, right)

        return expr

    def synchronize(self) -> None:
        self.advance()

        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return

            if self.peek().type in (
                    TokenType.CLASS,
                    TokenType.FUNCTION,
                    TokenType.VAR,
                    TokenType.FOR,
                    TokenType.IF,
                    TokenType.WHILE,
                    TokenType.PRINT,
                    TokenType.RETURN,
            ):
                return

            self.advance()

    def parse(self) -> List[statements.Stmt]:
        stmts: List[statements.Stmt] = []

        while not self.is_at_end():
            stmts.append(self.statement())

        return stmts
