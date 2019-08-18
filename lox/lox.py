from pathlib import Path
from sys import version_info, platform

from lox.ast_printer import AstPrinter
from lox.interpreter import Interpreter, LoxRuntimeError
from lox.parser import Parser, ParseError
from lox.scanner import Scanner
from lox.tokens import Token, TokenType


def lox_copyright():
    print(
        'Copyright (c) 2018-2018 Foo Bar Foundation.\n'
        'All Rights Reserved.'
    )


def lox_license():
    print('MIT License')


def lox_credits():
    print(
        'Thanks to Foo, Bar, Baz, Qux and a cast of thousands for supporting '
        'Lox development. See example.org for more information.'
    )


COMMANDS = {
    'exit': exit,
    'credits': lox_credits,
    'copyright': lox_copyright,
    'license': lox_license,
}


class Lox:
    interpreter = Interpreter()
    had_error = False
    had_runtime_error = False

    @staticmethod
    def repl_intro() -> None:
        python_version = '.'.join(str(i) for i in version_info[:3])

        print(
            'Lox REPL',
            f'[CPython {python_version}] on {platform}',
            'Type "copyright", "credits" or "license" for more information.',
            'Type "exit" or press Ctrl-D (i.e. EOF) to leave.',
            sep='\n'
        )

    @staticmethod
    def usage(code: int) -> None:
        print('Usage: lox [file]')
        exit(code)

    @staticmethod
    def report(line: int, where: str, message: str) -> None:
        print(f'[line {line}] Error{where}: {message}')

        Lox.had_error = True

    @staticmethod
    def error(token: Token, message: str) -> None:
        if token.type == TokenType.EOF:
            Lox.report(token.line, ' at end', message)
        else:
            Lox.report(token.line, f" at '{token.lexeme}'", message)

    @staticmethod
    def runtime_error(error: LoxRuntimeError) -> None:
        print(f'{error}\n[line {error.token.line}]')

        Lox.had_runtime_error = True

    @staticmethod
    def run(source: str) -> None:
        try:
            scanner = Scanner(source)
            tokens = scanner.scan_tokens()
            parser = Parser(tokens)
            expr = parser.parse()

            Lox.interpreter.interpret(expr)
        except ParseError as pe:
            Lox.error(pe.token, str(pe))
        except LoxRuntimeError as lre:
            Lox.runtime_error(lre)

    @staticmethod
    def run_file(filename) -> None:
        path = Path(filename).absolute()
        source = path.read_text(encoding='utf-8', errors='strict')
        Lox.run(source)

        if Lox.had_error:
            exit(65)
        elif Lox.had_runtime_error:
            exit(70)

    @staticmethod
    def prompt() -> None:
        Lox.repl_intro()

        while True:
            try:
                print('>>> ', end='')

                expr = input()
                first = expr.split(' ')[0]

                if first in COMMANDS:
                    COMMANDS[first]()
                else:
                    Lox.run(expr)
                    Lox.had_error = False
                    Lox.had_runtime_error = False
            except KeyboardInterrupt as ki:
                print(f'\n{ki.__class__.__name__}')
            except EOFError:
                exit(0)
