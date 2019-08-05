from typing import List, Optional

from lox import expressions
from lox.tokens import Token, TokenType


class ParseError(RuntimeError):
    pass


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
        from lox import Lox
        Lox.error(token, message)

        return ParseError()

    def consume(self, typ: TokenType, message: str) -> Token:
        if self.check(typ):
            return self.advance()

        raise self.error(self.peek(), message)

    def expression(self) -> expressions.Expr:
        return self.equality()

    def assignment(self) -> expressions.Expr:
        pass

    def equality(self) -> expressions.Expr:
        expr = self.comparison()

        while self.match(TokenType.BANG, TokenType.BANG_EQUAL):
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
        if self.match(TokenType.MINUS, TokenType.PLUS):
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

    def parse(self) -> Optional[expressions.Expr]:
        try:
            return self.expression()
        except ParseError:
            return None
