from assignment.token import  Token, tokenClasses

hadError = False

def error (line, message):
    report(line, "", message)

def masculineError(line,where,message):
    report(line,where,message)

def report(line, where, message):
    where = "somewhere" if where is None else where
    print("[ line %d ] at column %s message: %s " % (line, where, message))
    hadError = True

class Scanner:
    source = ""
    tokenList = []
    current = 0
    start = 0
    line = 1

    def __init__(self,src):
        self.source = src


    def scanTokens(self):
        self.tokenList.clear()
        while (not self.isAtEnd()):
            self.start = self.current
            self.scanToken()
        return self.tokenList

    def advance(self):
        self.current += 1
        return self.source[self.current -1]

    def scanToken(self):
        c = self.advance()
        if   c == '(':
            self.addToken(tokenClasses.TokenTypes.LEFT_PAREN)
        elif c == ')':
            self.addToken(tokenClasses.TokenTypes.RIGHT_PAREN)
        elif c == '}':
            self.addToken(tokenClasses.TokenTypes.RIGHT_BRACE)
        elif c == '{':
            self.addToken(tokenClasses.TokenTypes.LEFT_BRACE)
        elif c == ',':
            self.addToken(tokenClasses.TokenTypes.COMMA)
        elif c == '.':
            self.addToken(tokenClasses.TokenTypes.DOT)
        elif c == "-":
            self.addToken(tokenClasses.TokenTypes.MINUS)
        elif c == '+':
            self.addToken(tokenClasses.TokenTypes.PLUS)
        elif c == '*':
            self.addToken(tokenClasses.TokenTypes.STAR)
        elif c == ';':
            self.addToken(tokenClasses.TokenTypes.SEMICOLON)
        elif c == ':':
            self.addToken(tokenClasses.TokenTypes.COLON_EQUAL if self.match('=') else tokenClasses.TokenTypes.COLON)
        elif c == '!':
            self.addToken(tokenClasses.TokenTypes.BANG_EQUAL if self.match('=') else tokenClasses.TokenTypes.BANG)
        elif c == '=':
            self.addToken(tokenClasses.TokenTypes.EQUAL_EQUAL if self.match('=') else tokenClasses.TokenTypes.EQUAL)
        elif c == '>':
            self.addToken(tokenClasses.TokenTypes.GREATER_EQUAL if self.match('=') else tokenClasses.TokenTypes.GREATER)
        elif c == '<':
            self.addToken(tokenClasses.TokenTypes.LESS_EQUAL if self.match('=') else tokenClasses.TokenTypes.LESS)
        elif c == '/':
            self.addToken(tokenClasses.TokenTypes.SLASH)
        elif c == ' ':
            None
        elif c == '\\r':
            None
        elif c == '\\t':
            None
        elif c == '\\n':
            self.line += 1
        elif c == '"':
            self.string()
        else:
            if(self.isDigit(c)):
                self.number()
            elif(self.isAlpha(c)):
                self.identifier()
            else:
                masculineError(self.line,self.current,"Unexpected token")

    def identifier(self):
        while (self.isAlphanumeric(self.peek())): self.advance()
        text = self.source[self.start: self.current]
        type = tokenClasses.TokenTypes.keywords.get(text)
        if (type is None):
            self.addToken(tokenClasses.TokenTypes.IDENTIFIER)
        else:
            print("%s is a keyword"% text)

    def peek(self):
        if( self.isAtEnd()): return '\\0'
        return self.source[self.current]

    def string(self):
        while(self.peek() != '"' and not self.isAtEnd()):
            if self.peek() == '\n': self.line+=1;
            self.advance()

        if self.isAtEnd():
            error(self.line, "Unterminated String")

        self.advance()

        value = self.source[self.start + 1 : self.current - 1]
        self.addTokenAndLiteral(tokenClasses.TokenTypes.STRING,value)

    def isDigit(self,c):
        return c >= '0' and c <= '9'

    def isAlpha(self,c):
        return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= "Z") or c == "_"

    def isAlphanumeric(self,c ):
        return self.isAlpha(c) or self.isDigit(c)

    def match(self, expected):
        if (self.isAtEnd()): return False;
        if(self.source[self.current] != expected): return False;

        self.current += 1;
        return True

    def number(self):
        while(self.isDigit(self.peek())): self.advance()

        if self.peek() == '.' and self.isDigit(self.peekNext()):
            self.advance()
            while(self.isDigit(self.peek())): self.advance()

        substr = self.source[self.start: self.current]
        self.addTokenAndLiteral(tokenClasses.TokenTypes.NUMBER, substr)


    def peekNext(self):
        if self.current + 1 >= len(self.source): return '\0'
        else: return self.source[self.current + 1]

    def addToken(self,type):
        self.addTokenAndLiteral(type, None)

    def addTokenAndLiteral(self,type, literal):
        txt = self.source[self.start: self.current]
        self.tokenList.append(Token(type, txt, literal, self.line))

    def isAtEnd(self):
        return self.current >= len(self.source)


if __name__ == "__main__":
        while(True):
            response = input(">>")
            tokens = response.split(" ")
            scanner = Scanner(response)
            tokens = scanner.scanTokens()
            for token in tokens:
                print("Type: %s, lexeme: %s, literal: %s" % (token.tokenType, token.lexeme, token.literal))
            if hadError:
                SystemExit(65)

