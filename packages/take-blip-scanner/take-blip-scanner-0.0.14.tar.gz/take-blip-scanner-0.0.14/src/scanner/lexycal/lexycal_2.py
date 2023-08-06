from .lexycal_scanner_PTBR_2 import LexycalScanner_PTBR_2
from typing import List


class Lexycal_2:

    def __init__(self, idiom: str = 'PT_BR'):

        # Attributes
        self.tokens: List[bytearray] = []  # return list of tokens got by 'get_tokens()'
        self.token_ids: List[int] = []     # return list of corresponding token types
        if idiom == 'PT_BR':
            self.scan = LexycalScanner_PTBR_2()
        else:
            raise Exception("Invalid idiom '" + idiom + "'")
        self.token_type: dict = {
            'INVALID': 0,
            'EOT': 1,
            'WORD': 2,
            'DELIMITER': 3,
            'INTEGER': 4,
            'NUMBER': 5,
            'NUMBERWITHDOT': 6,
            'ORDINAL': 7,
            'CPF': 8,
            'CNPJ': 9,
            'CEP': 10,
            'DATE': 11,
            'TIME': 12,
            'CODE': 13,
            'PHONE1': 14,

            'EMAIL': 15,
            'URL': 16,
            'PHONE2': 17,
            'DDD': 18,
            'EMOJI': 19,
            'LAUGH': 20
        }

    def get_tokens(self, input_text: bytes, no_heuristics: bool = True):
        self.scan.next_fragment(input_text)
        self.tokens = []
        self.token_ids = []

        try:
            while True:
                self.scan.next_token()
                self.tokens.append(self.scan.token)
                self.token_ids.append(self.scan.token_id)
                if self.scan.token_id == self.scan.token_type['EOT']:
                    if not no_heuristics:
                        self.scan.apply_heuristics()
                    break
        except Exception as ex:
            print("ERROR " + str(ex))
            raise ex
        finally:
            return

    def output_text(self):
        pass

    def output_token_types(self):
        pass
