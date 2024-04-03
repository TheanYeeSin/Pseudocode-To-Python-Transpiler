class Emitter:
    """Emitter that emit code in python."""
    
    def __init__(self, full_path: str) -> None:
        self.full_path = full_path
        self.header = ""
        self.code = ""
        self.indent_count = 0
        
    def emit(self, code: str) -> None:
        """Emit new code."""
        self.code += code
        
    def emit_line(self, code: str) -> None:
        """Emit new code with new line."""
        self.code += f"{code}\n" + "\t" * self.indent_count
        
    def remove_indent(self) -> None:
        """Remove indentation from code."""
        if self.code.endswith("\t"):
            self.code = self.code[:-1]
        
    def header_line(self, code: str) -> None:
        """Emit the header code."""
        self.header += f"{code}\n"
        
    def write_file(self) -> None:
        """Create a file contain python code."""
        with open(self.full_path, 'w') as output_file:
            output_file.write(self.header + self.code)