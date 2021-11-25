import pandas as pd

if __name__ == '__main__':
    data = pd.read_csv('/Users/imseunghyo/Desktop/aiunited/dec/google_review_50man.csv')
    data = data.dropna(axis=0)
    print(data.shape)
    data1 = data[data['score']==1].sample(20000)
    data2 = data[data['score']==2].sample(18000)
    data3 = data[data['score']==3].sample(20000)
    data4 = data[data['score']==4].sample(20000)
    data5 = data[data['score']==5].sample(20000)

    data = pd.concat([data1, data2, data3, data4, data5])
    print(data['score'].value_counts())

    data.reset_index(drop=True, inplace=True)

    from dec.DEC.embedding.embedding import embedding
    data = embedding(data, column='preprocessed_review', embedding='doc2vec', model_name='doc2vec.bin')

    from dec.DEC.DEC.DEC import dec
    data = dec(data, embedding='doc2vec', n_clusters=5, model_name='doc2vec.bin', size=100)

    data = data[['score', 'cluster', 'review']]
    print(data['cluster'].value_counts())
    print(data[data['cluster']==0]['score'].value_counts())
    print(data[data['cluster']==1]['score'].value_counts())
    print(data[data['cluster']==2]['score'].value_counts())
    print(data[data['cluster']==3]['score'].value_counts())
    print(data[data['cluster']==4]['score'].value_counts())
    data.to_csv('data/DEC/dec_v2.csv', index=False, encoding='utf-8')