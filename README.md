# Lox language in Python

A Python (3.6+) implementation of the Lox language, from the in-progress book [Crafting Interpreters](https://craftinginterpreters.com/) by [Bob Nystrom](https://github.com/munificent).

This project is a port of **jlox**, the Java-based implementation presented throughout part of the book.

## What is Lox?

Lox is a full-featured, object-oriented scripting language with dynamic typing, garbage collection, lexical scope, first-class functions, closures, classes and inheritance, and more.


## Under development

This implementation is still ongoing, and there is a desire to extend the project later for educational purposes.

At the moment, the implementation follows almost every step and decision in the book, however:

- Not all challenges have been implemented yet
- I'll be using `self` instead of `this` (I'm a pythonist, just in case you are wondering)
- I will try to handle both `int` and `float` numbers instead of considering everything as `double` (yes, I know this is a tough task). If everything goes wrong or I get into trouble because of this decision, I will follow the book's decision to only use `double`. It should not be difficult to make the appropriate changes in the codebase (I think).
- The `TokenType` enum has many more tokens and keywords than those described by the book. I recorded all the ideas that came to mind while reading the language planning section.

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