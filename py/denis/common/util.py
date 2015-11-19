'''
Utility functions for use in any situation.

aka All the stuff I'm tired of copy-pasting :P
'''
def laxIncrement(dct, key):
    if not dct.has_key(key):
        dct[key] = 1
    else:
        dct[key] += 1

def expectKey(dct, key, valIfNew):
    if not dct.has_key(key):
        dct[key] = valIfNew
        return False
    else:
        return True

def dump(fname, contents):
    f = open(fname, 'w')
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

def writeCSV(fname, csv, sep=','):
    dump(fname, toCSV(csv, sep))

def toCSV(data, sep=','):
    return '\n'.join([sep.join([str(c) for c in row]) for row in data])

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
