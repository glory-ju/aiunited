import pandas as pd
# import kss
import torch
from multiprocessing import freeze_support
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
        # print(checked_sent)
        print(hangeul)
        dataframe.append([df['store_id'][idx], hangeul])
#       print(spacing(only_hangle(checked_sent)))
    except:
        pass

df1 = pd.DataFrame(dataframe, columns=['store_id', 'preprocessing_review'])
df1.to_csv('hangeul_preproc.csv', encoding='utf-8', index=False)

# ("김형호영화시장분석가는'1987'의네이버영화정보네티즌10점평에서언급된단어들을지난해12월27일부터올해1월10일까지통계프로그램R과KoNLP패키지로텍스트마이닝하여분석했다.")
# print(spacing('너는어디서무얼하고있느냐'))
punct = "/-'?!.,#$%\'()*+-/:;<=>@[\\]^_`{|}~" + '""“”’' + '∞θ÷α•à−β∅³π‘₹´°£€\×™√²—–&'
punct_mapping = {"‘": "'", "₹": "e", "´": "'", "°": "", "€": "e", "™": "tm", "√": " sqrt ", "×": "x", "²": "2", "—": "-", "–": "-", "’": "'", "_": "-", "`": "'", '“': '"', '”': '"', '“': '"', "£": "e", '∞': 'infinity', 'θ': 'theta', '÷': '/', 'α': 'alpha', '•': '.', 'à': 'a', '−': '-', 'β': 'beta', '∅': '', '³': '3', 'π': 'pi', }
