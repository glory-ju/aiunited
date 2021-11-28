from gensim.models import Word2Vec
from konlpy.tag import Okt

# 토큰화 (Okt 이용)
def text_to_token(df, column):
    okt = Okt()

    # 품사 종류 = [Adjective, Adverb, Alpha, Conjunction, Determiner, Eomi, Exclamation, Foreign, Hashtag, Josa,
    #           KoreanParticle, Noun, Number, PreEomi, Punctuation, ScreenName, Suffix, Unknown, Verb]

    tokenized_review = []
    for review in df[column]:
        tmp = []
        if review:
            for j in okt.pos(review, norm=True, stem=True):
                if j[1] not in ['Alpha', 'Conjunction', 'Determiner', 'Eomi', 'Josa', 'PreEomi', 'Suffix', 'Noun']: # 알파벳, 접속사, 관형사, 어미, 조사, 선어말어미, 접미사 제외
                    tmp.append(j[0])
        tokenized_review.append(tmp)

    df['tokenized_review'] = tokenized_review
    return df

def word2vec(df, column, **param):
    df = text_to_token(df, column)

    review_data = df.reset_index(drop=True)
    review_data = review_data[review_data['tokenized_review'].str.len() != 0] # tokenized_review 빈 리스트 제거

    texts = []
    for i in review_data['tokenized_review']:
        texts.append(i)

    # embedding_model = Word2Vec(texts, size=param['size'], window=param['window'], min_count=param['min_count'], workers=4, sg=1)
    # embedding_model.save('weights/word2vec.bin')

    return df