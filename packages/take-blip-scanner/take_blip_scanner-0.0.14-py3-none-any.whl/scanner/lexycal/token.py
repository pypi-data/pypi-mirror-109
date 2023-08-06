
from .token_type import TokenType

class Token:
    """
    Data structure returned by LabNLP lexical analyzer
    representing a lexical unit
    """

    def __init__(self, text: str, token_type: TokenType):
        self.text = text
        self.token_type = token_type

    def __repr__(self):
        return repr((self.text, self.token_type))
