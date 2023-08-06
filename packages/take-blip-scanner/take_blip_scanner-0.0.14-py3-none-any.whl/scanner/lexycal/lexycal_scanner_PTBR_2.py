class LexycalScanner_PTBR_2:
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
        self.fragment: bytes    # reference to text fragment received by 'next_fragment()'
        self.token: bytearray   # text of token returned by 'next_token()'
        self.token_id: int      # type of token returned

        # Protected
        self._alpha: bytes = bytes(
            'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÁÀÂÃáàâãÉÈÊéàêÍÌíìÓÒÔÕóòôõÚÙúùÇç_',
            'utf-8')
        self._digit: bytes = bytes('0123456789', 'utf-8')
        self._ordinal: bytes = bytes('ºª', 'utf-8')
        self._delimiter: bytes = bytes(' \r\n\t\'\"!#%&*()=+{[}]<><;?|@$', 'utf-8')
        self._blank: bytes = bytes(' \r\n\t', 'utf-8')       # also in self._delimiter
        self._numeric_part: bytes = bytes(':/-.,', 'utf-8')  # not in delimiter
        #   0   :
        #   1   /
        #   2   -
        #   3   .
        #   4   ,
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
        self._length: int = 0           # length of text fragment
        self._pos: int = 0              # next character position on the text fragment
        self._c: int = self._blank[0]   # current character being processed

    def next_fragment(self, fragment: bytes):
        self.fragment = fragment
        self.token = bytearray('', 'utf-8')
        self.token_id = self.token_type['INVALID']

        self._length = len(self.fragment)
        self._pos = 0
        self._c = self._blank[0]

    def next_token(self):
        self.token = bytearray('', 'utf-8')
        self.token_id = self.token_type['INVALID']

        while True:

            # Ignore blanks
            self.__ignore_blanks()

            # Check end-of-text
            if self._c == 0:
                self.token_id = self.token_type['EOT']
                return

            # WORD (EMAIL MONEY URL LAUGH)
            if self._c in self._alpha:
                return self.__get_alpha()

            # INTEGER (NUMBER DATE TIME CNPJ CPF CEP ORDINAL PHONE1)
            if self._c in self._digit:
                return self.__get_digit()

            # DELIMITER
            if self._c in self._delimiter or self._c in self._numeric_part:
                self.token_id = self.token_type['DELIMITER']
                self.token.append(self._c)
                self.__get_char()  # move to the next char
                return

            # INVALID
            self.__get_char()
            return

    def __ignore_blanks(self):
        while self._c in self._blank:
            self.__get_char()
        return

    def __get_char(self):
        if self._pos == self._length:
            self._c = 0
            return
        self._c = self.fragment[self._pos]
        self._pos += 1
        return

    def __get_alpha(self):

        # WORD -> (r'^\w+$')
        self.token_id = self.token_type['WORD']
        while self._c in self._alpha or self._c in self._digit:
            self.token.append(self._c)
            self.__get_char()
        return

    def __get_digit(self):

        # INTEGER -> (r'^\d+$')
        self.token_id = self.token_type['INTEGER']
        count = 0
        while self._c in self._digit:
            count += 1
            self.token.append(self._c)
            self.__get_char()
        if self._c in self._delimiter:
            return

        # NUMBER -> (r'^\d+(\,\d*){0,1}$')
        if self._c == self._numeric_part[4]:  # ','
            self.token_id = self.token_type['NUMBER']
            self.token.append(self._c)
            self.__get_char()
            while self._c in self._digit:
                self.token.append(self._c)
                self.__get_char()
            return

        # ORDINAL -> (r'^\d+[ºª]$')
        if self._c in self._ordinal:
            self.token_id = self.token_type['ORDINAL']
            self.token.append(self._c)
            return

        # PHONE1 (with no operator or DDD) -> (r'^\d{3,4}-\d{4}$')
        if self._c == self._numeric_part[2] and (count == 3 or count == 4):  # '-'
            self.token_id = self.token_type['PHONE1']
            self.token.append(self._c)
            count = 0
            self.__get_char()
            while self._c in self._digit:
                count += 1
                self.token.append(self._c)
                self.__get_char()
            if count == 4:
                return
            self.token.append(self._c)
            self.__replace_invalid()
            return

        # CEP -> (r'^\d{5}-\d{3}$')   (no '.' separator)
        if self._c == self._numeric_part[2] and (count == 5):  # '-'
            self.token_id = self.token_type['CEP']
            self.token.append(self._c)
            count = 0
            self.__get_char()
            while self._c in self._digit:
                count += 1
                self.token.append(self._c)
                self.__get_char()
            if count == 3:
                return
            self.__replace_invalid()
            return

        # NUMBERWITHDOT -> (r'^\d{1,3}(\.\d{3})*(\,\d*){0,1}$')
        if self._c == self._numeric_part[3]:  # '.'
            self.token_id = self.token_type['NUMBERWITHDOT']
            if count > 3:
                self.__replace_invalid()
                return
            first_group_length = count
            group = 0
            while self._c == self._numeric_part[3]:  # '.'
                group += 1
                self.token.append(self._c)
                count = 0
                self.__get_char()
                while self._c in self._digit:
                    count += 1
                    self.token.append(self._c)
                    self.__get_char()
                if count != 3:
                    self.__replace_invalid()
                    return
            if self._c == self._numeric_part[4]:  # ','
                self.token.append(self._c)
                self.__get_char()
                while self._c in self._digit:
                    self.token.append(self._c)
                    self.__get_char()
                return

            # CEP -> (r'^\d{2\.\d{3}}-\d{3}$')   (with '.' separator)
            if self._c == self._numeric_part[2] and first_group_length == 2 and group:  # '-'

                self.token_id = self.token_type['CEP']
                self.token.append(self._c)
                count = 0
                self.__get_char()
                while self._c in self._digit:
                    count += 1
                    self.token.append(self._c)
                    self.__get_char()
                if count == 3:
                    return
                self.__replace_invalid()
                return

            # CPF -> (r'^\d{3}(\.\d{3}){2}}(\-\d{2})$')
            if self._c == self._numeric_part[2]:  # '-'
                self.token_id = self.token_type['CPF']
                self.token.append(self._c)
                if first_group_length < 3:
                    self.__replace_invalid()
                    return
                count = 0
                self.__get_char()
                while self._c in self._digit:
                    count += 1
                    self.token.append(self._c)
                    self.__get_char()
                if count == 2:
                    return
                self.__replace_invalid()
                return

            # CNPJ -> (r'^\d{2,3}(\.\d{3}){2}(\/\d{4}\-\d{2})$')
            if self._c == self._numeric_part[1]:  # '/'

                self.token_id = self.token_type['CNPJ']
                self.token.append(self._c)
                if first_group_length < 2:
                    self.__replace_invalid()
                    return
                count = 0
                self.__get_char()
                while self._c in self._digit:
                    count += 1
                    self.token.append(self._c)
                    self.__get_char()
                self.token.append(self._c)
                if count != 4 or self._c != self._numeric_part[2]:  #'-'
                    self.__replace_invalid()
                    return
                count = 0
                self.__get_char()
                while self._c in self._digit:
                    count += 1
                    self.token.append(self._c)
                    self.__get_char()
                if count == 2:
                    return
                self.__replace_invalid()
                return

            # NUMBERWITHDOT -> (r'^\d{1,3}(\.\d{3})*$')
            if self._c in self._delimiter:
                return

        # DATE -> (r^\d{1,2}[\-\/]\d{1,2}([\-\/]\d{2,4}$'')
        if self._c == self._numeric_part[1] or self._c == self._numeric_part[2]:  # '/' e '-'
            self.token_id = self.token_type['DATE']
            self.token.append(self._c)
            if count == 1 or count == 2:
                count = 0
                self.__get_char()
                while self._c in self._digit:
                    count += 1
                    self.token.append(self._c)
                    self.__get_char()
                if (count == 1 or count == 2) and (self._c == self._numeric_part[1] or self._c == self._numeric_part[2]):  # '/' e '-'
                    self.token.append(self._c)
                    self.__get_char()
                    count = 0
                    while self._c in self._digit:
                        count += 1
                        self.token.append(self._c)
                        self.__get_char()
                    if count == 2 or count == 4:
                        return
                self.__replace_invalid()
                return
            self.__replace_invalid()
            return

        # TIME -> (r'^\d{1,2}\:\d{1,2}(\:\d{1,2}){0,1}$')
        if self._c == self._numeric_part[0]:  # ':'

            self.token_id = self.token_type['TIME']
            self.token.append(self._c)
            if count == 1 or count == 2:
                count = 0
                self.__get_char()
                while self._c in self._digit:
                    count += 1
                    self.token.append(self._c)
                    self.__get_char()
                if (count == 1 or count == 2) and self._c == self._numeric_part[0]:  # ':'
                    self.token.append(self._c)
                    self.__get_char()
                    count = 0
                    while self._c in self._digit:
                        count += 1
                        self.token.append(self._c)
                        self.__get_char()
                    if count == 2:
                        return
            self.__replace_invalid()
            return

        # INVALID
        self.__replace_invalid()
        return

    def __replace_invalid(self):
        self.token_id = self.token_type['CODE']
        while self._c not in self._blank and self._c != 0:
            self.token.append(self._c)
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
