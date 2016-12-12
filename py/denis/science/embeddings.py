'''
Library for reading word vector files (text or binary)
@Python3
'''
import numpy
import sys
import struct
import array
import codecs
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

def write(embeds, fname, mode=Mode.Binary):
    '''Writes a dictionary of embeddings { term : embed}
    to a file, in the format specified.
    '''
    if mode == Mode.Binary: _writeBin(embeds, fname)
    else: raise NotImplemented()

def _read(fname, mode):
    if mode == Mode.Text: (words, vectors) = _readTxt(fname)
    elif mode == Mode.Binary: (words, vectors) = _readBin(fname)
    return (words, vectors)

def _readTxt(fname):
    '''Returns array of words and word embedding matrix
    '''
    words, vectors = [], []
    hook = codecs.open(fname, 'r', 'utf-8')

    # get summary info about vectors file
    (numWords, dim) = (int(s.strip()) for s in hook.readline().split())

    for line in hook:
        chunks = line.split()
        word, vector = chunks[0].strip(), numpy.array([float(n) for n in chunks[1:]])
        words.append(word)
        vectors.append(vector)
    hook.close()

    assert len(words) == numWords
    for v in vectors: assert len(v) == dim

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
        wordmap.get(word).astype('f').tofile(outf)
        #wordmap.get(word).tofile(outf)
        outf.write(b'\n')
    outf.close()

def closestNeighbor(query, embedding_array, normed=False):
    '''Gets the index of the closest neighbor of embedding_array
    to the query point.  Distance metric is cosine.

    SLOW. DO NOT USE THIS FOR RAPID COMPUTATION.
    '''
    embedding_array = numpy.array(embedding_array)
    if not normed:
        embedding_array = numpy.array([
            (embedding_array[i] / numpy.linalg.norm(embedding_array[i]))
                for i in range(embedding_array.shape[0])
        ])

    ## assuming embeddings are unit-normed by this point;
    ## norm(query) is a constant factor, so we can ignore it
    dists = numpy.array([
        numpy.dot(query, embedding_array[i])
            for i in range(embedding_array.shape[0])
    ])
    return numpy.argmax(dists)

def unitNorm(embeds):
    for (k, embed) in embeds.items():
        embeds[k] = numpy.array(
            embed / numpy.linalg.norm(embed)
        )

def analogyQuery(embeds, a, b, c):
    return (
        numpy.array(embeds[b])
        - numpy.array(embeds[a])
        + numpy.array(embeds[c])
    )
