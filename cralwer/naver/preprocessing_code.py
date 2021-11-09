import pandas as pd
import torch
from soynlp.normalizer import *
from hanspell import spell_checker
from pykospacing import Spacing
from warnings import filterwarnings

filterwarnings('ignore')

df = pd.read_csv('sample_naver_review_0.csv')
spacing = Spacing()

dataframe = []

for idx in range(len(df)):
    try:
        sent = df['review'][idx].strip().replace(' ','')
        space = spacing(sent)
        spelled_sent = spell_checker.check(space)
        checked_sent = spelled_sent.checked
        hangeul = only_hangle(checked_sent)

        print(hangeul)
        dataframe.append([df['store_id'][idx], hangeul])
    except:
        pass

df1 = pd.DataFrame(dataframe, columns=['store_id', 'preprocessing_review'])
df1.to_csv('hangeul_preproc.csv', encoding='utf-8', index=False)