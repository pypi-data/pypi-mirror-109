from .token_type import TokenType
from .lexycal_scanner_PTBR_3 import LexycalScanner_PTBR_3

class Lexycal_3:

    def __init__(self, idiom: str = 'PT_BR'):

        # Attributes
        self.tokens = []  # return list of tokens got by 'get_tokens()'
        self.token_ids = []     # return list of corresponding token types
        self._token_ids_enum = None
        if idiom == 'PT_BR':
            self.scan = LexycalScanner_PTBR_3()
        else:
            raise Exception("Invalid idiom '" + idiom + "'")

    def get_tokens(self, input_text: str, no_heuristics: bool = True):
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
        self._token_ids_enum = [TokenType(x) for x in self.token_ids]
        return self._token_ids_enum
