from enum import IntEnum

class TokenType(IntEnum):
    INVALID = 0
    EOT = 1
    WORD = 2
    DELIMITER = 3
    INTEGER = 4
    NUMBER = 5
    NUMBERWITHDOT = 6
    ORDINAL = 7
    CPF = 8
    CNPJ = 9
    CEP = 10
    DATE = 11
    TIME = 12
    CODE = 13
    PHONE1 = 14
    EMAIL = 15
    URL = 16    
    PHONE2 = 17
    DDD = 18
    EMOJI = 19
    LAUGH = 20