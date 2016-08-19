'''
Common text preprocessing methods
'''

import sys
from denis.common import util
from denis.common.replacer import replacer

_cleaningPattern = replacer.prepare([
                       '.', ',', '!', '?', ':', ';', '>', '<',
                       '"', "'", '(', ')', '{', '}', '[', ']',
                       '\\',
                   ], onlyAtEnds=True)

def tokenize(line, clean=True, tolower=True):
    tokens = line.strip().split()
    if clean:
        cleanTokens = []
        for token in tokens:
            token = token.strip()
            # only force UTF-8 encoding if still in Python 2
            if sys.version[0] == '2':
                token = token.encode('utf-8')
            token = replacer.remove(_cleaningPattern, token)
            if tolower: token = token.lower()
            cleanTokens.append(token)
        tokens = cleanTokens
    return tokens
