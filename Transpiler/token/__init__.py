from enum import Enum
from typing import Optional


class Token:
    def __init__(self, token_text: str, token_type: "TokenTypes"):
        self.text = token_text
        self.type = token_type

    @staticmethod
    def check_keyword(token_text: str) -> Optional["TokenTypes"]:
        for type in TokenTypes:
            if (
                type.name == token_text.upper()
                and type.value >= 100
                and type.value < 200
            ):
                return type
        return None

    @staticmethod
    def check_typing(token_text: str) -> Optional["TokenTypes"]:
        for type in TokenTypes:
            if type.name == token_text.upper() and type.value >= 10 and type.value < 20:
                return type
        return None


class TokenTypes(Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2  # IDENTIFIER

    # TYPING
    INTEGER = 10
    REAL = 11
    CHAR = 12
    STRING = 13
    BOOLEAN = 14

    # KEYWORDS
    OUTPUT = 101
    INPUT = 102
    IF = 103
    THEN = 104
    ENDIF = 105
    WHILE = 106
    REPEAT = 107
    ENDWHILE = 108
    DECLARE = 109

    # TODO: Support more keywords

    # ARITHMETIC OPERATORS
    EQ = 201
    ADDITION = 202
    SUBTRACTION = 203
    MULTIPLICATION = 204
    DIVISION = 205
    POWER = 206

    # LOGICAL OPERATORS
    EQEQ = 207
    NOTEQ = 208
    LT = 209
    LTEQ = 210
    GT = 211
    GTEQ = 212

    COLON = 213
