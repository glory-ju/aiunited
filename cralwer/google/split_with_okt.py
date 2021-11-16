from konlpy.tag import Okt
from konlpy.tag import Mecab
import pandas as pd
from tqdm import tqdm

df = pd.read_csv('google_review.csv')
pre_df = df['preprocessed_review']


token = Okt()
tokenized_lst = []
for review in tqdm(pre_df):
    review = token.morphs(review)
    tokenized_lst.append(review)

print(tokenized_lst)