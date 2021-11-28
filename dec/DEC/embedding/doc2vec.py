from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
from konlpy.tag import Okt

def doc2vec(df, column, **param):
    okt = Okt()

    tokenized = []
    tagged_data = []
    for i in range(len(df)):
        tokenizing = okt.morphs(df[column][i], norm=True, stem=True)
        tokenized.append(tokenizing)
        tagged_data.append(TaggedDocument(words=tokenizing, tags=[str(df['score'][i])]))

    model = Doc2Vec(vector_size=100, min_count=20, epochs=20, seed=42)
    model.build_vocab(tagged_data)
    model.train(tagged_data, epochs=model.epochs, total_examples=model.corpus_count)
    model.save('weights/' + param['model_name'])

    df['tokenized'] = tagged_data

    return df
