# Lox language in Python

A Python (3.6+) implementation of the Lox language, from the in-progress book [Crafting Interpreters](https://craftinginterpreters.com/) by [Bob Nystrom](https://github.com/munificent).

This project is a port of **jlox**, the Java-based implementation presented throughout part of the book.

> The implementation is still **under development**.

## What is Lox?

Lox is a full-featured, object-oriented scripting language with dynamic typing, garbage collection, lexical scope, first-class functions, closures, classes and inheritance, and more.

## Requirements

The only requirement to run this project is Python 3.6+, due to the type hints used almost everywhere.

This project was developed on OS X, but it should work on any OS without any problems.

## Usage

#### REPL

```shell
python -m lox
```

Enter `exit` or press Ctrl+D to leave.

#### Running a file:

```shell
python -m lox path/to/file
```

## License

MIT License