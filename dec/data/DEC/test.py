import pandas as pd

data = pd.read_csv('dec_v2.csv')

print(data[data['cluster'] == 0]['score'].value_counts())
print(data[data['cluster'] == 1]['score'].value_counts())
print(data[data['cluster'] == 2]['score'].value_counts())
print(data[data['cluster'] == 3]['score'].value_counts())
print(data[data['cluster'] == 4]['score'].value_counts())

score_3 = data[(data['cluster'] == 0) & (data['score'] == 3)][:5700]
score_2 = data[(data['cluster'] == 1) & (data['score'] == 2)][:5700]
score_1 = data[(data['cluster'] == 2) & (data['score'] == 1)][:5700]
score_5 = data[(data['cluster'] == 3) & (data['score'] == 5)][:5700]
score_4 = data[(data['cluster'] == 4) & (data['score'] == 4)][:5700]

make_df = pd.concat([score_1, score_2, score_3, score_4, score_5])

make_df.to_csv('final_dec_review.csv')