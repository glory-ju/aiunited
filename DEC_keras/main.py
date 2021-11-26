import pandas as pd
# setting the hyper parameters
if __name__ == "__main__":

    data = pd.read_csv(r'C:/Users/quzmi/PycharmProjects/aiunited/cralwer/naver/50man_tokenized.csv')
    data = data.dropna(axis=0)
    print(data.shape)
    data1 = data[data['score'] == 0.5].sample(1000)
    data2 = data[data['score'] == 1.0].sample(1000)
    data3 = data[data['score'] == 1.5].sample(700)
    data4 = data[data['score'] == 2.0].sample(1000)
    data5 = data[data['score'] == 2.5].sample(1000)
    data6 = data[data['score'] == 3.0].sample(1000)
    data7 = data[data['score'] == 3.5].sample(1000)
    data8 = data[data['score'] == 4.0].sample(1000)
    data9 = data[data['score'] == 4.5].sample(1000)
    data10 = data[data['score'] == 5.0].sample(1000)

    data = pd.concat([data1, data2, data3, data4, data5, data6, data7, data8, data9, data10])
    print(data['score'].value_counts())

    data.reset_index(drop=True, inplace=True)

    from DEC import dec

    data = dec(data, model_name='my_doc2vec_model', size=100)
    print(type(data))
    data = data[['score', 'cluster', 'review']]
    print(data['cluster'].value_counts())
    print(data[data['cluster'] == 0]['score'].value_counts())
    print(data[data['cluster'] == 1]['score'].value_counts())
    print(data[data['cluster'] == 2]['score'].value_counts())
    print(data[data['cluster'] == 3]['score'].value_counts())
    print(data[data['cluster'] == 4]['score'].value_counts())
    print(data[data['cluster'] == 5]['score'].value_counts())
    print(data[data['cluster'] == 6]['score'].value_counts())
    print(data[data['cluster'] == 7]['score'].value_counts())
    print(data[data['cluster'] == 8]['score'].value_counts())
    print(data[data['cluster'] == 9]['score'].value_counts())

    data.to_csv('results/dec_v2.csv', index=False, encoding='utf-8')