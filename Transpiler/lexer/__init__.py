import sys
from Transpiler.token import Token, TokenTypes

class Lexer:
    """Lexer that break down source code into sequence of tokens."""
    
    def __init__(self, input: str) -> None:
        self.input = input + "\n"
        self.current_char = ""
        self.current_pos = -1
        self.next_char()
        
    def next_char(self) -> None:
        """Process the next character."""
        self.current_pos += 1
        if self.current_pos >= len(self.input):
            self.current_char = "\0"
        else:
            self.current_char = self.input[self.current_pos]
            
    def peek(self) -> str:
        """Return the next character."""
        return "\0" if self.current_pos + 1 >= len(self.input) else self.input[self.current_pos + 1]

    def abort(self, message: str) -> None:
        """Return error message"""
        sys.exit(f"Lexer error. Error: {message}")
        
    def skip_white_space(self) -> None:
        while self.current_char == ' ' or self.current_char == '\r': # or self.current_char == '\t' 
            self.next_char()
    
    def skip_comment(self) -> None:
        """Skip comments in the code."""
        if self.current_char == "#":
            while self.current_char != '\n':
                self.next_char()
            
    def get_token(self) -> Token:
        """Return the next token."""
        self.skip_white_space()
        self.skip_comment()
        
        token = None
        
        if self.current_char == '+': # Add
            token = Token(self.current_char, TokenTypes.ADDITION)
            
        elif self.current_char == '-': # Subtract
            token = Token(self.current_char, TokenTypes.SUBTRACTION)
            
        elif self.current_char == '*': # Multiple
            token = Token(self.current_char, TokenTypes.MULTIPLICATION)
            
        elif self.current_char == '/': # Divide
            token = Token(self.current_char, TokenTypes.DIVISION)
            
        elif self.current_char == '^': # Raised to the power of
            token = Token(self.current_char, TokenTypes.POWER)
            
        elif self.current_char == '\n': # Newline
            token = Token(self.current_char, TokenTypes.NEWLINE)
            
        elif self.current_char == '\0': # End of file
            token = Token('', TokenTypes.EOF)
            
        elif self.current_char == '←': # Assign
            token = Token(self.current_char, TokenTypes.EQ)
            
        elif self.current_char == '=': # Equal to (Not assigning)
            token = Token(self.current_char, TokenTypes.EQEQ)
            
        elif self.current_char == '<': 
            if self.peek() == '=': # Less than or equal to
                last_char = self.current_char
                self.next_char()
                token = Token(last_char + self.current_char, TokenTypes.LTEQ)
            elif self.peek() == '>': # Not equal to
                last_char = self.current_char
                self.next_char()
                token = Token(last_char + self.current_char, TokenTypes.NOTEQ)
            else: # Less than
                token = Token(self.current_char, TokenTypes.LT)
                
        elif self.current_char == '>': 
            if self.peek() == '=': # Greater than or equal to
                last_char = self.current_char
                self.next_char()
                token = Token(last_char + self.current_char, TokenTypes.GTEQ)
            else: # Greater than
                token = Token(self.current_char, TokenTypes.GT)
                
        elif self.current_char == '\"': # String
            self.next_char()
            start_pos = self.current_pos
            while self.current_char != '\"':
                if (self.current_char == '\r' or 
                    self.current_char == '\n' or 
                    self.current_char == '\t' or 
                    self.current_char == '\\' or 
                    self.current_char == '%'):
                    self.abort("Illegar character in string.")
                self.next_char()
            token_text = self.input[start_pos: self.current_pos]
            token = Token(token_text, TokenTypes.STRING)
            
        elif self.current_char.isdigit(): # Number
            start_pos = self.current_pos
            while self.peek().isdigit():
                self.next_char()
            if self.peek() == '.':
                self.next_char()
                
                if not self.peek().isdigit():
                    # Error
                    self.abort("Illegal character in number.")
                while self.peek().isdigit():
                    self.next_char()
            token_text = self.input[start_pos: self.current_pos + 1]
            token = Token(token_text, TokenTypes.NUMBER)
        
        elif self.current_char.isalpha(): # Keyword
            start_pos = self.current_pos
            while self.peek().isalnum():
                self.next_char()
            token_text = self.input[start_pos : self.current_pos + 1]
            keyword = Token.check_keyword(token_text)
            if keyword is None: # Identifier
                token = Token(token_text, TokenTypes.IDENT)
            else:
                token = Token(token_text, keyword)
        else:
            self.abort(f"Unknown token: {self.current_char}")
        
        self.next_char()
        
        return token