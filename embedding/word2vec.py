import pandas as pd
from konlpy.tag import Okt
from gensim.models import Word2Vec
import matplotlib.pyplot as plt
import numpy as np
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import matplotlib as mpl
from gensim.models import KeyedVectors

df = pd.read_csv('C:/Users/hy949/PycharmProjects/aiunited/data/siksin_pre.csv', encoding='utf-8')
train_data = df[:10000][:]
# train_data = df.loc[:]['preprocessed_review']
print(train_data)

# Null 값이 존재하는 행 제거
train_data = train_data.dropna(how = 'any')
scores = list(train_data['score'])
text = list(train_data['review'])

# 불용어 정의


# 형태소 분석기 OKT를 사용한 토큰화 작업 (다소 시간 소요)
def tokenize_okt(train_data):
    stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다', '을', '를']
    okt = Okt()
    tokenized_data = []
    for sentence in train_data['preprocessed_review']:
        temp_X = okt.morphs(sentence, stem=True) # 토큰화
        temp_X = [word for word in temp_X if not word in stopwords] # 불용어 제거
        tokenized_data.append(temp_X)

    return tokenized_data


# 그래프 폰트 문제 처리
def fix_font_errors():
    mpl.rcParams['axes.unicode_minus'] = False
    plt.rc('font', family='Malgun Gothic')


def get_avg_vector(tokenized_data):
    avg_vector = []
    for idx, i in enumerate(tokenized_data):
        for token in i:
            vectors = []
            vectors.append(model.wv[token])
        avg_vector.append(sum(vectors)/len(vectors))
    return avg_vector

# 차원 축소 (TSNE)
def reduce_dimensionality_tsne(avg_vector):
    tsne = TSNE(random_state=42)
    X = tsne.fit_transform(avg_vector)

    plt.figure(figsize=(30, 20))
    plt.scatter(X[:, 0], X[:, 1], c=scores)

    for i, tag in enumerate(scores):
        plt.annotate(tag, (X[:, 0][i], X[:, 1][i]))

    plt.xlabel('t-SNE 특성 0')
    plt.ylabel('t-SNE 특성 1')
    plt.title('tsne(size=100)')
    plt.show()

# 차원 축소 (PCA)
def reduce_dimensionality_pca(avg_vector):
    pca = PCA(random_state=42)
    X = pca.fit_transform(avg_vector)
    
    plt.figure(figsize=(30, 20))
    plt.scatter(X[:, 0], X[:, 1], c=scores)
    
    for i, tag in enumerate(scores):
        plt.annotate(tag, (X[:, 0][i], X[:, 1][i]))
    
    plt.xlabel('pca 특성 0')
    plt.ylabel('pca 특성 1')
    plt.title('pca(size=100)')
    plt.show()

model = Word2Vec(tokenized_data, size=100, window=5, min_count=1, sg=1)
tokenized_data = tokenize_okt(train_data)
avg_vector = get_avg_vector(tokenized_data)
fix_font_errors()
reduce_dimensionality_tsne(avg_vector)
reduce_dimensionality_pca(avg_vector)