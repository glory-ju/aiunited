import matplotlib.pyplot as plt
from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
from konlpy.tag import Okt
import numpy as np
import matplotlib as mpl
import matplotlib.font_manager as fm

mpl.rcParams['font.family'] = 'NanumGothicOTF'

okt = Okt()
data1 = ["맛없어요", "최악입니다", "다신 안 가고 싶네요"]
data3 = ["그냥 그래요", "보통 이에요", "또 가려면 고민 좀 해 볼 것 같아요"]

data5 = ["맛있어요", "최고 최고", "재방문 의사 있습니다"]

text = []
tagged_data = []
for i in data1:
    text.append(i)
    tagged_data.append(TaggedDocument(words=okt.morphs(i, norm=True, stem=True), tags=[str(1)]))
for i in data3:
    text.append(i)
    tagged_data.append(TaggedDocument(words=okt.morphs(i, norm=True, stem=True), tags=[str(3)]))
for i in data5:
    text.append(i)
    tagged_data.append(TaggedDocument(words=okt.morphs(i,  norm=True, stem=True), tags=[str(5)]))

model = Doc2Vec(vector_size=20, min_count=1, epochs=20, seed=42)
model.build_vocab(tagged_data)
model.train(tagged_data, epochs=model.epochs, total_examples=model.corpus_count)

def get_features(model, words, size):
    feature_vector = np.zeros((size), dtype=np.float32)
    num_words = 0
    word_set = set(model.wv.index_to_key)

    for w in words:
        if w in word_set:
            num_words += 1
            feature_vector = np.add(feature_vector, model[w])

    if num_words != 0:
        feature_vector = np.divide(feature_vector, num_words)
    else:
        pass

    return feature_vector

dataVec = None
data = []
tag = []
for i in tagged_data:
    data.append(get_features(model, i[0], 20))
    tag.append(i[1])
    dataVec = np.stack(data)

from sklearn.manifold import TSNE
tsne = TSNE(random_state=42, init='pca')
X = tsne.fit_transform(dataVec)

plt.figure(figsize=(10, 10))
plt.scatter(X[:, 0], X[:, 1], c=tag)

for i, txt in enumerate(text):
    plt.annotate(txt, (X[:, 0][i], X[:, 1][i]))

plt.show()