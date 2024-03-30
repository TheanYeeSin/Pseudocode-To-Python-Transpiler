from Transpiler.lexer import Lexer
from Transpiler.token import Token, TokenTypes
from Transpiler.parser import Parser
from Transpiler.emitter import Emitter

class Transpiler:
    
    def __init__(self, input: str, full_path: str) -> None:
        self.lexer = Lexer(input)
        self.emitter = Emitter(full_path)
        self.parser = Parser(self.lexer, self.emitter)

    def transpile(self) -> None:
        self.parser.program() # Start the parser.
        self.emitter.write_file() 
        print("Parsing completed.")