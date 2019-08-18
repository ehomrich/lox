from typing import List, Union, Any, Optional

from lox.tokens import (
    TokenType,
    Token,
    KEYWORDS,
    SINGLE_CHARS,
    ONE_OR_MORE_CHARS,
    STRING_STARTERS,
    WHITESPACE,
)


class Scanner:
    def __init__(self, source: str) -> None:
        self.source = source
        self.tokens: List[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1

    @property
    def current_token(self) -> str:
        return self.source[self.start:self.current]

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def reset(self) -> None:
        self.start = 0
        self.current = 0
        self.line = 1

    def advance_line(self) -> None:
        self.line += 1

    def advance(self) -> str:
        self.current += 1
        return self.current_token

    def peek(self) -> str:
        if self.is_at_end():
            return '\0'

        return self.source[self.current]

    def peek_next(self) -> str:
        if (self.current + 1) > len(self.source):
            return '\0'

        return self.source[self.current + 1]

    def match(self, expected: str) -> bool:
        if self.is_at_end() or self.peek() != expected:
            return False

        self.advance()
        return True

    def identifier(self) -> None:
        while self.peek().isalnum():
            self.advance()

        text: str = self.current_token
        typ: TokenType = KEYWORDS.get(text, TokenType.IDENTIFIER)
        self.add_token(typ)

    def number(self) -> None:
        def consume_digits():
            while self.peek().isdigit():
                self.advance()

        typ: TokenType = TokenType.INTEGER
        consume_digits()

        if self.peek() == '.' and self.peek_next().isdigit():
            typ = TokenType.FLOAT
            self.advance()
            consume_digits()

        if self.peek() == '.':
            raise SyntaxError('invalid syntax')

        token: str = self.current_token
        value: Union[float, int] = float(token) if '.' in token else int(token)

        self.add_token(typ, value)

    def string(self, starter: str) -> None:
        while self.peek() != starter and not self.is_at_end():
            if self.peek() == '\n':
                self.advance_line()
            self.advance()

        self.advance()
        text: str = self.source[(self.start + 1):(self.current - 1)]
        self.add_token(TokenType.STRING, text)

    def comment(self):
        while self.peek() != '\n' and not self.is_at_end():
            self.advance()

        self.add_token(TokenType.HASH)

    def add_token(self, typ: TokenType, literal: Optional[Any] = None) -> None:
        token = Token(typ, self.current_token, literal, self.line)
        self.tokens.append(token)

    def scan_token(self) -> None:
        char = self.advance()

        if char in SINGLE_CHARS:
            self.add_token(TokenType(char))
        elif char in ONE_OR_MORE_CHARS:
            compounds = [i
                         for i in ONE_OR_MORE_CHARS
                         if i.startswith(char) and len(i) == 2]

            token = char

            for compound in compounds:
                if self.match(compound[1]):
                    token = compound
                    break

            self.add_token(TokenType(token))
        elif char in WHITESPACE:
            return
        elif char == '\n':
            self.advance_line()
        elif char == '#':
            self.comment()
        elif char in STRING_STARTERS:
            self.string(char)
        elif char.isdigit():
            self.number()
        elif char.isalpha():
            self.identifier()
        else:
            raise SyntaxError(f'Unexpected character "{char}" at '
                              f'line {self.line}')

    def scan_tokens(self) -> List[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, TokenType.EOF.value, None, self.line))
        return self.tokens
