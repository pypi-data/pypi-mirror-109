from .token_type import TokenType

class LexycalScanner_PTBR_3:
    """
    IMPLEMENTATION CONCEPTS
    -----------------------

    (1) The main targets of this implementation is performance and accuracy
        to recognize syntatic units usual in Natural Language messages.
    (2) The code mindset is "C like", uses only primitive Python resources and
        could be translated to C code "as is" (each Python statement could be 
        converted to a single, or a few, C statement).
    (3) In many cases code repetition is used instead of function calls.
    (4) The characters of each parsed text are read from left to right and
        each character is READ ONLY ONCE. An index keeps track of the parse
        current position. This index moves ahead one character at a time. This
        means that, just looking at the character currently pointed to by the index,
        the process can decide whether this character belongs to the token being
        parsed, or if it marks the end of that token.
    (5) When a token is recognized the index should be pointing to the character
        immediately following the token just recognized. If this do not happens,
        the index must be moved ahead one character, to meet this requirement.
    (6) When an INVALID sequence of characters is parsed (a token of type INVALID)
        the index must be moved one character ahead, so that it points to the
        character immediately following the character that invalidated the token.
    (7) Blanks, tabs, and newlines are handled as "delimiters", that is, no token
        may contain blanks.
    (8) Each delimiter is a token by itself, of type DELIMITER.
    (9) Some non-alpha and non-digit characters may appear as part of numeric tokens
        like numbers with dot separator ('.') and certain kinds of 'code' like CPF.
    (10)The parser must be initialized only once and returns to its initial state
        whenever a new fragment to be parsed is supplied.
    (11)End-of-text (EOT) is a token explicitly returned by the parser to signify
        that the fragment text has been fully parsed. It should be always present 
        as the last token of a fragment of text. A fragment of text
        submitted to the parser may contain one or more "new-line" characters.
    (12)The parser accepts multi-line fragment text, that is, text containing several 
        end-of-line characters (these are handled as blanks).
        
   HEURISTICS
   ----------
   Some tokens cannot be recognized properly in a left-to-right scan without 
   backtracking, that is, looking at each character only once. 
   Some simple heuristics are used to circumvent this, allowing for the
   recognition of some tokens. The downside of this approach is that in many
   situations these heuristics may ignore existing tokens that would be
   recognized otherwise.
   (A) CODE: any text starting with a digit and terminated by a "blank" (a"blank" 
       is explicitly define by the parser - space, tab, end-of-line). The
       idea behind this heuristic is that CODE will appear between two "blanks" or
       between a "delimiter" and a "blank" (token of type CODE is recognized whenever
       the parsing of a token starting with a digit fails).
    (B) URL is a set of tokens that together can be recognized as a valid URL
    (C) EMAIL is a set of tokens that can be recognized as a valid valid email address
    (D) LAUGH is a WORD formed by certain sequences
    (E) EMOJI is a set of tokens with a specific pattern, occurring immediately after '/'
    (F) MONEY is a set of tokens recognized as a monetary value
    (G) DDD indicates operator and/or DDD code of a phone number
    (H) PHONE2 is a PHONE1 preceded by DDD 
    """

    def __init__(self):
        
        # Attributes
        self.fragment: str    # reference to text fragment received by 'next_fragment()'
        self.token: str   # text of token returned by 'next_token()'
        self.token_id: int      # type of token returned

        # Protected
        self._alpha = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÁÀÂÃáàâãÉÈÊéàêÍÌíìÓÒÔÕóòôõÚÙúùÇç_")
        self._digit = set("0123456789")
        self._ordinal = set("ºª")
        self._delimiter = set(" \r\n\t\'\"!#%&*()=+{[}]<><;?|@$")
        self._blank = set(" \r\n\t") # also in self._delimiter
        self._numeric_part = set(":/-.,") # not in delimiter
        
        self.token_type = {i.name: i.value for i in TokenType}
        self._length: int = 0           # length of text fragment
        self._pos: int = 0              # next character position on the text fragment
        self._c = " "   # current character being processed

    def next_fragment(self, fragment):
        self.fragment = fragment
        self.token = ""
        self.token_id = self.token_type['INVALID']

        self._length = len(self.fragment)
        self._pos = 0
        self._c = " "

    def next_token(self):
        self.token = ""
        self.token_id = self.token_type['INVALID']

        while True:
            # Ignore blanks
            self.__ignore_blanks()

            # Check end-of-text
            if self._c == "\0":
                self.token_id = self.token_type['EOT']
                return

            # WORD (EMAIL MONEY URL LAUGH)
            if self._c in self._alpha:
                return self.__get_alpha()

            # DELIMITER
            if self._c in self._delimiter or self._c in self._numeric_part:
                self.token_id = self.token_type['DELIMITER']
                self.token = self.token + self._c
                self.__get_char()  # move to the next char
                return
            
            # INTEGER (NUMBER DATE TIME CNPJ CPF CEP ORDINAL PHONE1)
            if self._c in self._digit:
                return self.__get_digit()

            # INVALID
            self.__get_char()
            return

    def __ignore_blanks(self):
        while self._c in self._blank:
            self.__get_char()
        return

    def __get_char(self):
        if self._pos >= self._length:
            self._c = "\0"
            return
        self._c = self.fragment[self._pos]
        self._pos += 1
        return
    
    def __remove_last_char(self):
        self._c = self.token[-1]
        self.token = self.token[:-1]
        # self._pos -= 1
        return

    def __get_alpha(self):
        # WORD -> (r'^\w+$')
        self.token_id = self.token_type['WORD']
        while self._c in self._alpha:
            self.token = self.token + self._c
            self.__get_char()
        if self._c in self._digit:
            self.__replace_invalid()
        return

    def __set_token(self, token_type):
        self.token_id = self.token_type[token_type]
        self.token = self.token + self._c

    def __update_token(self, count):
        while self._c in self._digit:
            count += 1
            self.token = self.token + self._c
            self.__get_char()
        return count

    def __get_number(self):
        self.__set_token('NUMBER')
        self.__get_char()
        
        while self._c in self._digit:
            self.token = self.token + self._c
            self.__get_char()
            
        if self.token[-1] == ',':
            self.token_id = self.token_type['INTEGER']
            self.__remove_last_char()
            return

    def __get_phone(self):
        self.__set_token('PHONE1')
        count = 0
        self.__get_char()
        count = self.__update_token(count)
        if count == 4:
            return
        self.token = self.token + self._c
        self.__replace_invalid()
        return

    def __get_cep(self):
        self.__set_token('CEP')
        count = 0
        self.__get_char()
        count = self.__update_token(count)
        if count == 3:
            return
        self.__replace_invalid()
        return

    def __get_phone_or_cep(self):
        count = 0
        self.__get_char()
        count = self.__update_token(count)
        if count == 3:
            self.__set_token('CEP')
            return
        elif count == 4:
            self.__set_token('PHONE1')
            return
        self.__replace_invalid()
        return

    def __get_cpf(self, first_group_length):
        self.__set_token('CPF')
        if first_group_length < 3:
            self.__replace_invalid()
            return
        count = 0
        self.__get_char()
        count = self.__update_token(count)
        if count == 2:
            return
        self.__replace_invalid()
        return

    def __get_cnpj(self, first_group_length):
        self.__set_token('CNPJ')
        if first_group_length < 2:
            self.__replace_invalid()
            return
        count = 0
        self.__get_char()
        count = self.__update_token(count)
        self.token = self.token + self._c
        if count != 4 or self._c != "-":  # '-'
            self.__replace_invalid()
            return
        count = 0
        self.__get_char()
        count = self.__update_token(count)
        if count == 2:
            return
        self.__replace_invalid()
        return

    def __get_number_with_dot(self, count):
        if count > 3:
            return
        self.token_id = self.token_type['NUMBERWITHDOT']
        first_group_length = count
        group = 0
        while self._c == ".":  # '.'
            group += 1
            self.token = self.token + self._c
            count = 0
            self.__get_char()
            count = self.__update_token(count)
            if count != 3:
                if count == 0:
                    self.__remove_last_char()
                    return
                self.__replace_invalid()
                return
        if self._c == ",":  # ','
            self.token = self.token + self._c
            self.__get_char()
            while self._c in self._digit:
                self.token = self.token + self._c
                self.__get_char()
            if (self._c in self._blank or self._c == "\0") and self.token[-1] not in self._digit:
                self.__remove_last_char()
                return
            return

        # CEP -> (r'^\d{2\.\d{3}}-\d{3}$')   (with '.' separator)
        if self._c == "-" and first_group_length == 2 and group:  # '-'
            self.__get_cep()
            return

        # CPF -> (r'^\d{3}(\.\d{3}){2}}(\-\d{2})$')
        if self._c == "-":  # '-'
            self.__get_cpf(first_group_length)
            return

        # CNPJ -> (r'^\d{2,3}(\.\d{3}){2}(\/\d{4}\-\d{2})$')
        if self._c == "/":  # '/'
            self.__get_cnpj(first_group_length)
            return

        # NUMBERWITHDOT -> (r'^\d{1,3}(\.\d{3})*$')
        if self._c in self._delimiter:
            return

    def __check_delimiter(self, token):
        if token == 'DATE':
            return self._c in ('/', '-')
        elif token == 'TIME':
            return self._c == ':'
        return False

    def __get_date_time(self, token, count):
        self.__set_token(token)
        if count == 1 or count == 2:
            count = 0
            self.__get_char()
            count = self.__update_token(count)
            if (count == 1 or count == 2) and self.__check_delimiter(token):
                self.token = self.token + self._c
                self.__get_char()
                count = 0
                count = self.__update_token(count)
                if count == 2:
                    return
                elif token == 'DATE' and count == 4:
                    return
            self.__replace_invalid()
            return
        self.__replace_invalid()
        return

    def __get_digit(self):
        # INTEGER -> (r'^\d+$')
        self.token_id = self.token_type['INTEGER']
        count = 0
        count = self.__update_token(count)
        if self._c in self._delimiter:
            return

        # NUMBER -> (r'^\d+(\,\d*){0,1}$')
        if self._c == ",":  # ','
            self.__get_number()
            return

        # ORDINAL -> (r'^\d+[ºª]$')
        if self._c in self._ordinal:
            self.__set_token('ORDINAL')
            return

        # PHONE1 (with no operator or DDD) -> (r'^\d{4,5}-\d{4}$')
        # CEP -> (r'^\d{5}-\d{3}$')   (no '.' separator)

        if self._c == '-':
            if count == 4:
                self.__get_phone()
                return
            elif count == 5:
                self.__get_phone_or_cep()
                return

        # NUMBERWITHDOT -> (r'^\d{1,3}(\.\d{3})*(\,\d*){0,1}$')
        if self._c == ".":  # '.'
            self.__get_number_with_dot(count)
            return

        # DATE -> (r^\d{1,2}[\-\/]\d{1,2}([\-\/]\d{2,4}$'')
        if self._c == "/" or self._c == "-":  # '/' e '-'
            self.__get_date_time('DATE', count)
            return

        # TIME -> (r'^\d{1,2}\:\d{1,2}(\:\d{1,2}){0,1}$')
        if self._c == ":":  # ':'
            self.__get_date_time('TIME', count)
            return

        # INVALID
        self.__replace_invalid()
        return

    def __replace_invalid(self):
        while self._c not in self._blank and self._c != '\0':
            self.__set_token('CODE')
            self.__get_char()

    def apply_heuristics(self):
        pass

    def correct_orthography(self):
        pass

    def replace_synonyms(self):
        pass

    def replace_number_names(self):
        pass

    def replace_date_names(self):
        pass

    def replace_relative_date_names(self):
        pass
