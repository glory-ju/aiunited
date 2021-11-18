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
train_data = df[:100][:]
# train_data = df.loc[:]['preprocessed_review']
print(train_data)

# Null 값이 존재하는 행 제거
train_data = train_data.dropna(how = 'any')

# 불용어 정의
stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다', '을', '를']


# 형태소 분석기 OKT를 사용한 토큰화 작업 (다소 시간 소요)
okt = Okt()
tokenized_data = []
for sentence in train_data['preprocessed_review']:
    temp_X = okt.morphs(sentence, stem=True) # 토큰화
    temp_X = [word for word in temp_X if not word in stopwords] # 불용어 제거
    tokenized_data.append(temp_X)
print(len(tokenized_data))
print(tokenized_data)
scores = list(train_data['score'])
print(scores)
# 모델 생성
# model = Word2Vec(sentences = tokenized_data, window = 5, min_count = 5, workers = 4, sg = 0, size = 100)
# , size = 100
# 완성된 임베딩 매트릭스의 크기 확인
# print(model.wv.vectors.shape)
# print(model.wv.most_similar("맛"))

# 그래프 폰트 문제 처리
mpl.rcParams['axes.unicode_minus'] = False
plt.rc('font', family='Malgun Gothic')

# 차원 축소 (TSNE)
def show_tsne(X_show):
    tsne = TSNE(n_components=2)
    X = tsne.fit_transform(X_show)

    df = pd.DataFrame(X, index=vocab_show, columns=['x', 'y'])
    fig = plt.figure()
    fig.set_size_inches(30, 20)
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(df['x'], df['y'])

    for word, pos in df.iterrows():
        ax.annotate(word, pos, fontsize=10)

    plt.xlabel('t-SNE 특성 0')
    plt.ylabel('t-SNE 특성 1')
    plt.show()

# 차원 축소 (PCA)
def show_pca(X_show):
    pca = PCA(n_components=2)
    pca.fit(X_show)

    x_pca = pca.transform(X_show)

    plt.figure(figsize=(30, 20))
    plt.xlim(x_pca[:, 0].min(), x_pca[:, 0].max())
    plt.ylim(x_pca[:, 1].min(), x_pca[:, 1].max())

    for i in range(len(X_show)):
        plt.text(x_pca[i, 0], x_pca[i, 1], str(vocab_show[i]),
                 fontdict={'weight': 'bold', 'size': 9})
    plt.xlabel('첫 번째 주성분')
    plt.ylabel('두 번째 주성분')
    plt.show()


model = Word2Vec(tokenized_data, size=300, window=3, min_count=1, workers=1)


vocab = list(model.wv.vocab)
print(vocab)
print(len(vocab))
X = model[vocab]


# sz개의 단어에 대해서만 시각화
sz = 1000
X_show = X[:1000, :]
vocab_show = vocab[:sz]

show_tsne(X_show)
show_pca(X_show)

avg_vector = []
for i in tokenized_data:
    for token in i:
        vectors = []
        vectors.append(model.wv[token])
    avg_vector.append(sum(vectors)/len(vectors))
print(len(avg_vector))
# print(avg_vector)



