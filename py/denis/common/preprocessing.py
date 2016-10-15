'''
Common text preprocessing methods
'''

import sys
from denis.common import util
from denis.common.replacer import replacer

_to_remove = [
    '.', ',', '!', '?', ':', ';', '>', '<',
    '"', "'", '(', ')', '{', '}', '[', ']',
    '\\', '--', '`',
]
_to_substitute = util.flatten([_to_remove, [
    '-'
]])
_removal_pattern = replacer.prepare(_to_remove, onlyAtEnds=True)
_substitution_pattern = replacer.prepare(_to_substitute, onlyAtEnds=False)

def tokenize(line, clean=True, tolower=True, splitwords=False):
    tokens = line.strip().split()
    if clean:
        cleanTokens = []
        for token in tokens:
            token = token.strip()
            # only force UTF-8 encoding if still in Python 2
            if sys.version[0] == '2':
                token = token.encode('utf-8')
            token = replacer.remove(_removal_pattern, token)
            if tolower: token = token.lower()
            if splitwords:
                token = replacer.suball(_substitution_pattern, ' ', token)
                cleanTokens.extend(token.split())
            else:
                cleanTokens.append(token)
        tokens = cleanTokens
    return tokens
