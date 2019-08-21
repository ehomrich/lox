from argparse import ArgumentParser
from pathlib import Path
from typing import Dict, Iterable, Tuple, TextIO

arg_parser = ArgumentParser(usage='generate_ast.py <output directory>')
arg_parser.add_argument('output',
                        help='Directory where the generated result '
                             'will be stored. Default: /lox',
                        )
args = arg_parser.parse_args()

ASTDict = Dict[str, Tuple[str]]

DEFAULT_IMPORTS: Tuple[str] = ('from abc import ABC, abstractmethod',)

EXPRESSIONS_IMPORTS: Tuple[str] = DEFAULT_IMPORTS + (
    'from typing import Any, List',
    'from lox.scanner import Scanner',
    'from lox.tokens import Token',
)

STATEMENTS_IMPORTS: Tuple[str] = DEFAULT_IMPORTS + ('from lox.expressions import Expr',)

EXPRESSIONS: ASTDict = {
    'Assign': ('name: Token', 'value: Expr'),
    'Binary': ('left: Expr', 'operator: Token', 'right: Expr'),
    'Call': ('callee: Expr', 'paren: Token', 'arguments: List[Expr]'),
    'Get': ('obj: Expr', 'name: Token'),
    'Grouping': ('expression: Expr',),
    'Literal': ('value: Any',),
    'Logical': ('left: Expr', 'operator: Token', 'right: Expr'),
    'Set': ('obj: Expr', 'name: Token', 'value: Expr'),
    'Super': ('keyword: Token', 'method: Token'),
    'This': ('keyword: Token',),
    'Unary': ('operator: Token', 'right: Expr'),
    'Variable': ('name: Token',)
}

STATEMENTS: ASTDict = {
    'Expression': ('expression: Expr',),
    'Print': ('expression: Expr',),
}

INDENTATION = '    '


def define_ast(path: Path, base_name: str, types: ASTDict, imports: Tuple[str]) -> None:
    name = base_name.title()
    visitor = f'{base_name}Visitor'

    with path.open(mode='w', encoding='utf-8') as file:
        define_imports(file, imports)
        define_visitor(file, base_name, types.keys())
        file.write('\n\n')
        file.write(f'class {name}(ABC):')
        file.write('\n')
        file.write(f'{INDENTATION}@abstractmethod')
        file.write('\n')
        file.write(f'{INDENTATION}def accept(self, visitor: {visitor}):')
        file.write('\n')
        file.write(f'{INDENTATION * 2}pass')
        file.write('\n\n')

        for class_name, fields in types.items():
            file.write('\n')
            define_type(file, name, class_name, fields)
            file.write('\n')


def define_imports(file: TextIO, lines: Tuple[str]) -> None:
    file.write('\n'.join(lines))


def define_type(file: TextIO, base_name: str, class_name: str, fields: Tuple[str]) -> None:
    file.write(f'class {class_name}({base_name}):')
    file.write('\n')
    file.write(f'{INDENTATION}')
    file.write(f'def __init__(self, {", ".join(fields)}) -> None:')
    file.write('\n')

    for field in fields:
        attr = field.split(':')[0]
        file.write(f'{INDENTATION * 2}self.{attr} = {attr}')
        file.write('\n')

    file.write('\n')
    file.write(f'{INDENTATION}')
    file.write(f'def accept(self, visitor: {base_name}Visitor) -> None:')
    file.write('\n')
    file.write(f'{INDENTATION * 2}')
    file.write(f'return visitor.visit_{class_name.lower()}_{base_name.lower()}(self)')
    file.write('\n')


def define_visitor(file: TextIO, base_name: str, types: Iterable[str]) -> None:
    name = base_name.lower()
    visitor = f'{base_name}Visitor'

    file.write('\n\n\n')
    file.write(f'class {visitor}(ABC):')

    for typ in types:
        file.write('\n')
        file.write(f'{INDENTATION}@abstractmethod')
        file.write('\n')
        file.write(f'{INDENTATION}')
        file.write(f"def visit_{typ.lower()}_{name}(self, expr: '{base_name}'):")
        file.write('\n')
        file.write(f'{INDENTATION * 2}pass')
        file.write('\n')


def main() -> None:
    path = Path(args.output).resolve()

    if not path.is_dir():
        arg_parser.error('output must be a valid directory')

    define_ast(path / 'expressions.py', 'Expr', EXPRESSIONS, EXPRESSIONS_IMPORTS)
    define_ast(path / 'statements.py', 'Stmt', STATEMENTS, STATEMENTS_IMPORTS)


if __name__ == '__main__':
    main()
