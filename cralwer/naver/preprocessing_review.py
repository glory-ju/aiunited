import pandas as pd
from konlpy.tag import Mecab
import re
from soynlp.normalizer import *
from hanspell import spell_checker
from pykospacing import Spacing

df = pd.read_csv('C:/Users/quzmi/PycharmProjects/aiunited/data/naver_sample_review_10.csv')
dataframe = []
spacing = Spacing()

for idx in range(len(df)):
    try:
        sent = df['review'][idx].strip().replace(' ','')
        spelled_sent = spell_checker.check(sent)
        checked_sent = spelled_sent.checked
        space = spacing(checked_sent)
        hangeul = only_hangle(space)
        if '구성비' in hangeul:
            hangeul = hangeul.replace('구성비','가성비')
        print(hangeul)
        dataframe.append(hangeul)
    except:
        dataframe.append('')
preprocessed = pd.DataFrame(dataframe)
df['preprocessed_reivew'] = preprocessed
print(df)
df.to_csv('naver_preprocessing_review.csv', encoding='utf-8', index=False)