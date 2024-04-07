import sys
from Transpiler.lexer import Lexer
from Transpiler.emitter import Emitter
from Transpiler.token import Token, TokenTypes


class Parser:
    """Parser that generates the equivalent code"""

    def __init__(self, lexer: Lexer, emitter: Emitter) -> None:
        self.lexer = lexer
        self.emitter = emitter

        self.current_token: Token = None
        self.peek_token: Token = None
        self.next_token()
        self.next_token()

    def check_token(self, type: TokenTypes) -> bool:
        """Return true if the current token matches."""
        return self.current_token.type == type

    def check_peek(self, type: TokenTypes) -> bool:
        """Return true if the next token matches."""
        return self.peek_token.type == type

    def next_token(self) -> None:
        """Advances to the next token."""
        self.current_token = self.peek_token
        self.peek_token = self.lexer.get_token()

    def match(self, type: TokenTypes) -> None:
        """Try to match the current token. If not, output error."""
        print(self.current_token.text)
        if not self.check_token(type):
            self.abort(
                f"Expected {type.name}, got {self.current_token.type.name} instead."
            )
        self.next_token()

    def abort(self, message: str) -> None:
        """Return error message"""
        sys.exit(f"Parser error. Error: {message}")

    # Production Rules

    def program(self) -> None:
        # program ::= {statement}
        while self.check_token(TokenTypes.NEWLINE):
            self.next_token()

        while not self.check_token(TokenTypes.EOF):
            self.statement()

    def statement(self) -> None:
        # statement ::= "PRINT" (expression | string) nl
        #     | "IF" comparison "THEN" nl {statement} "ENDIF" nl
        #     | "WHILE" comparison "REPEAT" nl {statement} "ENDWHILE" nl
        #     | "DECLARE" ident type
        #     | "GOTO" ident nl
        #     | "LET" ident "=" expression nl
        #     | "INPUT" ident nl

        # Check the first token to see what kind of statement this is.
        if self.check_token(TokenTypes.OUTPUT):
            print("STATEMENT-OUTPUT")

            self.next_token()

            if self.check_token(TokenTypes.STRING):
                # Simple string.
                self.emitter.emit_line(f"print('{self.current_token.text}')")
                print("STRING")
                self.next_token()
            else:
                self.emitter.emit_line(f"print({self.current_token.text})")
                print("EXPRESSION")
                self.expression()

        # "IF" comparison "THEN" {statement} "ENDIF"
        elif self.check_token(TokenTypes.IF):
            print("STATEMENT-IF")
            self.next_token()
            self.emitter.emit(f"if ")
            self.comparison()

            self.match(TokenTypes.THEN)
            self.nl()
            self.emitter.indent_count += 1
            self.emitter.emit_line(":")

            while not self.check_token(TokenTypes.ENDIF):
                self.statement()

            # Last statement inside IF block will still add the indentation, so remove it here
            self.emitter.indent_count -= 1
            self.emitter.remove_indent()
            self.match(TokenTypes.ENDIF)

        # "WHILE" comparison "REPEAT" {statement} "ENDWHILE"
        elif self.check_token(TokenTypes.WHILE):
            print("STATEMENT-WHILE")
            self.next_token()
            self.emitter.emit(f"while ")
            self.comparison()

            self.match(TokenTypes.REPEAT)
            self.nl()
            self.emitter.indent_count += 1
            self.emitter.emit_line(":")

            while not self.check_token(TokenTypes.ENDWHILE):
                self.statement()

            self.emitter.indent_count -= 1
            self.emitter.remove_indent()
            self.match(TokenTypes.ENDWHILE)

        # "DECLARE" ident : type
        elif self.check_token(TokenTypes.DECLARE):
            # TODO: FIX to fit pseudocode and python
            print("STATEMENT-DECLARE")
            self.next_token()

            self.emitter.emit(self.current_token.text + " = ")
            self.match(TokenTypes.IDENT)
            self.match(TokenTypes.EQ)
            self.expression()
            self.emitter.emit_line("")

        # "INPUT" ident
        elif self.check_token(TokenTypes.INPUT):
            print("STATEMENT-INPUT")
            self.next_token()

            self.match(TokenTypes.IDENT)

        else:
            self.abort(
                f"Invalid statement at {self.current_token.text} ({self.current_token.type.name})"
            )

        # Newline.
        self.nl()

    def nl(self) -> None:
        """Newline"""
        print("NEWLINE")

        # Require at least one newline.
        self.match(TokenTypes.NEWLINE)

        # But we will allow extra newlines too, of course
        while self.check_token(TokenTypes.NEWLINE):
            self.next_token()

    def comparison(self) -> None:
        print("COMPARISON")

        self.expression()

        if self.is_comparison_operator():
            self.emitter.emit(self.current_token.text)
            self.next_token()
            self.expression()

        else:
            self.abort(f"Expected comparison operator at: {self.current_token.text}")

        while self.is_comparison_operator():
            print(self.current_token.text)
            self.next_token()
            self.expression()

    def is_comparison_operator(self) -> bool:
        """Return true if the current token is a comparison operator."""
        return (
            self.check_token(TokenTypes.GT)
            or self.check_token(TokenTypes.GTEQ)
            or self.check_token(TokenTypes.LT)
            or self.check_token(TokenTypes.LTEQ)
            or self.check_token(TokenTypes.EQEQ)
            or self.check_token(TokenTypes.NOTEQ)
        )

    # expression ::= term {( "-" | "+" ) term}
    def expression(self) -> None:
        print("EXPRESSION")
        self.term()

        # Can have more than 1 terms with (+/-)
        while self.check_token(TokenTypes.ADDITION) or self.check_token(
            TokenTypes.SUBTRACTION
        ):
            self.emitter.emit(self.current_token.text)
            self.next_token()
            self.term()

    # term ::= unary {( "/" | "*" ) unary}
    def term(self) -> None:
        print("TERM")
        self.unary()

        # Can have more than 1 unaries
        while self.check_token(TokenTypes.MULTIPLICATION) or self.check_token(
            TokenTypes.DIVISION
        ):
            self.emitter.emit(self.current_token.text)
            self.next_token()
            self.unary()

    # unary ::= ["+" | "-"] primary
    def unary(self) -> None:
        print("UNARY")

        # Optional unary +/-
        if self.check_token(TokenTypes.ADDITION) or self.check_token(
            TokenTypes.SUBTRACTION
        ):
            self.emitter.emit(self.current_token.text)
            self.next_token()
        self.primary()

    # primary
    # primary ::= number | ident
    def primary(self) -> None:
        print(f"PRIMARY ({self.current_token.text})")

        if self.check_token(TokenTypes.NUMBER):
            print("NUMBER")
            self.emitter.emit(self.current_token.text)
            self.next_token()
        elif self.check_token(TokenTypes.IDENT):
            print("IDENT")
            # Ensure the variable already exists.
            # if self.current_token.text not in self.symbols:
            #     self.abort(f"Referencing variable before assignment: {self.current_token.text}")
            self.emitter.emit(self.current_token.text)
            self.next_token()
        else:
            # Error
            self.abort(f"Unexpected token at {self.current_token.text}")
