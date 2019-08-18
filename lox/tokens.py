from enum import Enum
from typing import Dict, Any, Tuple


class TokenType(Enum):
    # Single-character tokens
    LEFT_PAREN = '('
    RIGHT_PAREN = ')'
    LEFT_BRACKET = '['
    RIGHT_BRACKET = ']'
    LEFT_CURLY_BRACE = '{'
    RIGHT_CURLY_BRACE = '}'
    COMMA = ','
    DOT = '.'
    MINUS = '-'
    PLUS = '+'
    COLON = ':'
    SEMICOLON = ';'
    SLASH = '/'
    BACKSLASH = '\\'
    STAR = '*'
    UNDERSCORE = '_'
    QUOTATION_MARK = '?'
    PERCENT = '%'
    AT_SIGN = '@'
    AMPERSAND = '&'
    DOLLAR_SIGN = '$'
    CARET = '^'
    TILDE = '~'
    PIPE = '|'

    # One or two+ character tokens
    BANG = '!'
    BANG_EQUAL = '!='
    EQUAL = '='
    EQUAL_EQUAL = '=='
    GREATER = '>'
    GREATER_EQUAL = '>='
    LESS = '<'
    LESS_EQUAL = '<='
    ARROW = '=>'
    SHEBANG = '#!'
    HASH = '#'
    ELLIPSIS = '...'
    TRIPLE_QUOTE = '"""'

    # Keywords
    GET = 'get'
    SET = 'set'
    DELETE = 'delete'
    AND = 'and'
    OR = 'or'
    NOT = 'not'
    IF = 'if'
    ELSE = 'else'
    SWITCH = 'switch'
    CASE = 'case'
    WHEN = 'when'
    WHILE = 'while'
    UNLESS = 'unless'
    BREAK = 'break'
    FOR = 'for'
    IN = 'in'
    DO = 'do'
    NULL = 'null'
    TRUE = 'true'
    FALSE = 'false'
    TRY = 'try'
    CATCH = 'catch'
    FINALLY = 'finally'
    NEW = 'new'
    CLASS = 'class'
    EXTENDS = 'extends'
    SUPER = 'super'
    SELF = 'self'
    INTERFACE = 'interface'
    IMPLEMENTS = 'implements'
    FUNCTION = 'function'
    RETURN = 'return'
    GENERATOR = 'generator'
    YIELD = 'yield'
    ASYNC = 'async'
    AWAIT = 'await'
    STATIC = 'static'
    LAMBDA = 'lambda'
    CONST = 'const'
    LET = 'let'
    VAR = 'var'
    PRIVATE = 'private'
    END = 'end'
    PRINT = 'print'

    # String starters
    SINGLE_QUOTE = "'"
    DOUBLE_QUOTE = '"'

    # New line
    NEW_LINE = '\n'

    # Space
    TAB = '\t'
    SPACE = ' '

    # String terminator
    NULL_CHARACTER = '\0'

    # End-user identifiers
    IDENTIFIER = 'identifier'
    INTEGER = 'int'
    FLOAT = 'float'
    STRING = 'str'

    # end-of-file
    EOF = ''


_keywords: Tuple[str] = (
    'true', 'false', 'null', 'and', 'or', 'if', 'else', 'function', 'return',
    'for', 'class', 'super', 'self', 'const', 'let', 'while', 'var', 'print'
)

KEYWORDS: Dict[str, TokenType] = {key: TokenType(key) for key in _keywords}

SINGLE_CHARS: Tuple[str] = (
    '(', ')', '{', '}', ',', '.', '-', '+', ';', '*', '/',
)

ONE_OR_MORE_CHARS: Tuple[str] = ('!', '!=', '=', '==', '>', '>=', '<', '<=')

WHITESPACE: Tuple[str] = (' ', '\r', '\t')

STRING_STARTERS: Tuple[str] = ('"', "'")


class Token:
    def __init__(
            self,
            typ: TokenType,
            lexeme: str,
            literal: Any,
            line: int
    ) -> None:
        self.type = typ
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self) -> str:
        return f'{self.type}: {self.lexeme}, {self.literal}, {self.line}'

    def __repr__(self) -> str:
        properties = f'{self.type}, {self.lexeme}, {self.literal}, {self.line}'
        return f'{self.__class__.__name__}({properties})'
