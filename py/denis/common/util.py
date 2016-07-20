'''
Utility functions for use in any situation.

aka All the stuff I'm tired of copy-pasting :P
'''
import random
import codecs
import re
from denis.common.replacer import replacer

def laxIncrement(dct, key, by=1):
    if not dct.get(key):
        dct[key] = by
    else:
        dct[key] += by

def expectKey(dct, key, valIfNew):
    if not dct.get(key):
        dct[key] = valIfNew
        return False
    else:
        return True

def dump(fname, contents, encoding='ascii'):
    f = codecs.open(fname, 'w', encoding)
    f.write(contents)
    f.close()

def readlines(fname):
    f = open(fname, 'r')
    lns = f.readlines()
    f.close()
    return lns

def readCSV(fname, sep=',', readas=str):
    lns = readlines(fname)
    return [[readas(c.strip()) for c in row.split(sep)] for row in lns]

def writeCSV(fname, csv, sep=',', encoding='ascii', useUnicode=False):
    '''
    If useUnicode is True and encoding is unspecified, will default to UTF-8 encoding.
    '''
    if useUnicode:
        if encoding == 'ascii': encoding = 'utf-8'
        writeas = unicode
    else:
        writeas = str
    dump(fname, toCSV(csv, sep, writeas=writeas), encoding=encoding)

def toCSV(data, sep=',', writeas=str):
    return '\n'.join([sep.join([writeas(c) for c in row]) for row in data])

def bitflag(bln):
    if bln: return 1
    else: return 0

def transformListToDict(lst, tfrm):
    out = {}
    for i in lst:
        key, val = tfrm(i)
        out[key] = val
    return out

def transformDict(dct, tfrm):
    out = {}
    for k in dct.keys():
        key, val = tfrm(k, dct[k])
        out[key] = val
    return out

def reverseDict(dct):
    reverse = lambda key, val: (val, key)
    return transformDict(dct, reverse)

def replace(text, repls):
    pattern = replacer.prepare(repls)
    return replacer.apply(pattern, text)

def parallelExecute(processes):
    '''Takes instances of multiprocessing.Process, starts them all executing,
    and returns when they finish.
    '''
    # start all the threads running...
    for p in processes:
        p.start()
    # ...and wait for all of them to finish
    for p in processes:
        p.join()

def coinflip():
    '''Return True with probability 1/2
    '''
    return rollDie(n=2)

def rollDie(n):
    '''Roll an N-sided die and return True with probability 1/N
    '''
    return random.choice(range(n)) == 0

def matchesRegex(regex, string):
    '''Returns Boolean indicating if the input regex found a positive (non-zero)
    match in the input string.
    '''
    mtch = re.match(regex, string)
    return mtch != None and mtch.span() != (0,0)

def flatten(arr):
    '''Given an array of N-dimensional objects (N can vary), returns 1-dimensional
    list of the contained objects.
    '''
    results = []
    for el in arr:
        if type(el) == list or type(el) == tuple: results.extend(flatten(el))
        else: results.append(el)
    return results
