import sys
from Transpiler import Transpiler

if __name__ == "__main__":
    print("Transpiler")

    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs source file as argument.")
    with open(sys.argv[1], 'r') as input_file:
        input = input_file.read()

    transpile = Transpiler(input=input, full_path="out.py")
    
    transpile.transpile()
    