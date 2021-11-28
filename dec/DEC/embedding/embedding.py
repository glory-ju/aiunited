from .word2vec import word2vec
from .doc2vec import doc2vec

def embedding(data, column, embedding, **param):
    if embedding == 'word2vec':
        return word2vec(data, column, **param)
    elif embedding == 'doc2vec':
        return doc2vec(data, column, **param)