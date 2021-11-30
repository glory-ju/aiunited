import re
import pandas as pd
from pykospacing import Spacing
from hanspell import spell_checker
from gensim.test.utils import get_tmpfile
import tweepy
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from konlpy.tag import Okt
from sklearn.manifold import TSNE
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
mpl.rcParams['font.family'] = 'NanumGothicOTF'

'''
    @ author : seunghyo
    @ method : 한글 전처리 메서드
    @ parameter : 전처리 하고자하는 문자열 리스트
    @ return : 전처리 후 문자열 리스트
'''

def ko_preprocessing(str_list):
    result = []
    idx = 0
    for str in str_list:
        try:
            # 한글만 추출
            str = re.compile('[가-힣][ㄱ-ㅎ]+').findall(str)
            # 위에서 추출한 list(str)을 하나의 str로 통합
            str = ''.join(str)
            # 맞춤법 체크
            spelled_sent = spell_checker.check(str)
            str = spelled_sent.checked
            # 띄어쓰기
            spacing = Spacing()
            str = spacing(str)
            idx += 1
            print(idx)
        except:
            # 리뷰 없을 시 빈 문자열 넣기
            str = ''
        result.append(str)

    return result

'''
    @ author : seunghyo
    @ method : 한글 전처리 메서드
    @ parameter : 전처리 하고자하는 문자열 리스트
    @ return : 전처리 후 문자열 리스트
'''
def ko_preprocessing_str(str):
    try:
        # 한글만 추출
        str = re.compile('[가-힣ㄱ-ㅎ]+').findall(str)
        print(str)
        print(type(str))
        # 위에서 추출한 list(str)을 하나의 str로 통합
        str = ''.join(str)
        # 맞춤법 체크
        spelled_sent = spell_checker.check(str)
        str = spelled_sent.checked
        # 띄어쓰기
        spacing = Spacing()
        str = spacing(str)
    except:
        # 리뷰 없을 시 빈 문자열 넣기
        str = ''
    print(str)
    return str

'''
    @ author : seunghyo
    @ method : 한글 형태소 분석
    @ parameter : 문자열 
    @ return : TaggedDocument Type
'''
def morpheme(reviews_and_scores):
    # 형태소 분해 객체 생성
    okt = Okt()

    tagged_data = [
        TaggedDocument(words=okt.morphs(review), tags=[str(score)])
        for review, score in reviews_and_scores
        if type(review) != float
    ]
    return tagged_data

'''
    @ author : seunghyo
    @ method : gensim doc2vec 모델 생성
    @ parameter : TaggedDocument Type data List
    @ return : model
'''
def get_doc2vec_model(tagged_data):
    # 모델 설계
    max_epochs = 100
    model = Doc2Vec(vector_size=100,
                    alpha=0.025,
                    min_alpha=0.00025,
                    min_count=1,
                    dm=1)

    # ??
    model.build_vocab(tagged_data)

    # 학습
    for epoch in range(max_epochs):
        model.train(tagged_data,
                    total_examples=model.corpus_count,
                    epochs=model.epochs)
        # decrease the learning rate
        model.alpha -= 0.0002
        # fix the learning rate, no decay
        model.min_alpha = model.alpha
    return model


'''
    @ author : seunghyo
    @ method : gensim doc2vec 모델 저장
    @ parameter : doc2vec model, file path
    @ return : 성공하면 True, 실패하면 False
'''
def save_model(model, path):
    try:
        f_name = get_tmpfile(os.path.join(os.path.abspath(os.path.dirname(__file__)), path))
        model.save(f_name)
    except:
        return False
    finally:
        return True

'''
    @ author : seunghyo
    @ method : word feature 추출
    @ parameter : word feature 추출
    @ return : word feature vector
'''
def get_features(model, words, size):
    feature_vector = np.zeros((size), dtype=np.float32)
    num_words = 0
    word_set = set(model.wv.index_to_key)

    for i, w in enumerate(words):
        if w in word_set:
            num_words += 1
            feature_vector = np.add(feature_vector, model[w])

    if num_words != 0:
        feature_vector = np.divide(feature_vector, num_words)
    else:
        pass

    return feature_vector
if __name__ == '__main__':
    # 데이터 불러오기
    df = pd.read_csv('/Users/imseunghyo/Desktop/aiunited/preprocessing_example/preprocessing_review.csv')
    df = df.dropna(axis=0)
    reviews_and_scores = zip(df['preprocessing_review'].tolist()[:10000], df['score'].tolist()[:10000])
    tagged_data = morpheme(reviews_and_scores)
    lenth_tag = len(tagged_data)
    model = get_doc2vec_model(tagged_data)

    # 모델저장
    result = save_model(model, 'my_doc2vec_model')

    print(result)

    dataVec = None
    data = []
    tag = []

    for i in tagged_data:
        data.append(get_features(model, i[0], 100))
        tag.append(i[1])
        dataVec = np.stack(data)

    tsne = TSNE(random_state=42, init='pca')
    X = tsne.fit_transform(dataVec)

    plt.figure(figsize=(10, 10))
    plt.scatter(X[:, 0], X[:, 1], c=tag)

    for i, txt in enumerate(df['preprocessing_review'].tolist()[:50]):
        print(i)
        if i == 73 or i == 74:
            print(txt)

        plt.annotate(txt, (X[:, 0][i], X[:, 1][i]))

    plt.show()