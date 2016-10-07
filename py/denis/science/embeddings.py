'''
Library for reading word vector files (text or binary)
@Python3
'''
import numpy
import sys
import struct
import array
import codecs
#from common.vocabio import VocabIO
from denis.common.logging import log

class Mode:
    Text = 'txt'
    Binary = 'bin'

def read(fname, mode=Mode.Binary):
    '''Returns array of words and word embedding matrix
    '''
    (words, vectors) = _read(fname, mode)

    wordmap = {}
    for i in range(len(words)):
        wordmap[words[i]] = vectors[i]
    return wordmap

def generateVocabFile(fname, mode, outfile):
    '''Writes ordered vocabulary of vectors file to outfile
    '''
    (words, _) = _read(fname, mode)
    VocabIO.write(words, outfile)

def _read(fname, mode):
    if mode == Mode.Text: (words, vectors) = _readTxt(fname)
    elif mode == Mode.Binary: (words, vectors) = _readBin(fname)
    return (words, vectors)

def _readTxt(fname):
    '''Returns array of words and word embedding matrix
    '''
    words, vectors = [], []
    for line in open(fname, 'r'):
        chunks = line.split()
        word, vector = clean(chunks[0]), numpy.array([float(n) for n in chunks[1:]])
        words.append(clean(word))
        vectors.append(vector)
    return (words, vectors)

def _readBin(fname):
    words, vectors = [], []
    inf = open(fname, 'rb')

    # get summary info about vectors file
    summary = inf.readline().decode('utf-8')
    (numWords, dim) = (int(s.strip()) for s in summary.split(' '))

    chunksize = 10*4096
    curIx, nextChunk = inf.tell(), inf.read(chunksize)
    while len(nextChunk) > 0:
        inf.seek(curIx)

        splitix = nextChunk.index(b' ')
        word = inf.read(splitix).decode('utf-8')
        inf.seek(1,1) # skip the space
        vector = array.array('f', inf.read(dim*4))
        inf.seek(1,1) # skip the newline

        words.append(word)
        vectors.append(vector)
        curIx, nextChunk = inf.tell(), inf.read(chunksize)
    inf.close()

    # verify that we read properly
    assert len(words) == numWords
    return (words, vectors)

def _writeBin(wordmap, fname):
    outf = open(fname, 'wb')

    # write summary info
    vdim = len(wordmap.get(list(wordmap.keys())[0]))
    summary = ('%d %d' % (len(wordmap), vdim)).encode('utf-8')
    outf.write(b'%s\n' % summary)

    # write vectors
    for word in wordmap.keys():
        outf.write(b'%s ' % word.encode('utf-8'))
        wordmap.get(word).tofile(outf)
        outf.write(b'\n')
    outf.close()
