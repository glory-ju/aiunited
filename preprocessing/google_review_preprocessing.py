# -*- coding: utf-8 -*-
'''
    @ Author : jihnkim
    @ method : preprocessing package
'''

from hanspell import spell_checker
from pykospacing import Spacing
from soynlp.normalizer import *
import re

# 맞춤법 검사 func
def spell_check(text: str) -> str:
    spelled_sent = spell_checker.check(text)

    hanspell_sent = spelled_sent.checked

    return hanspell_sent

# corpus 특수문자 및 영문 처리
def clean_text(texts : list) -> list:
    corpus = []
    for i in range(0, len(texts)):
        review = re.sub(r'[@%\\*=()/~#&\+á?\xc3\xa1\-\|\.\:\;\!\-\,\_\~\$\'\"]', '',str(texts[i])) #remove punctuation
        review = re.sub(r'\d+','', str(texts[i]))# remove number
        review = review.lower() #lower case
        review = re.sub(r'\s+', ' ', review) #remove extra space
        # review = re.sub(r'<[^>]+>','',review) #remove Html tags
        review = re.sub(r'\s+', ' ', review) #remove spaces
        review = re.sub(r"^\s+", '', review) #remove space from start
        review = re.sub(r'\s+$', '', review) #remove space from the end
        review = re.sub(r'^[A-Za-z0-9+]*$', '', review) #remove alphabet, numbers
        review = re.sub(r'[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', review) #remove special characters
        review = re.sub(r'[^\w\s]', '', review) #remove punctuation
        corpus.append(review)
    return corpus


# 띄어쓰기 처리 func, err
def kospacing(text: str) -> str:
    spacing = Spacing()
    kospacing_sent = spacing(text)

    return kospacing_sent

# 반복제한
def repeat_limitation(text: str) -> str:
    text = emoticon_normalize(text, num_repeats=2)

    return text

# punct mapping (text)
def clean_punc(text: str) -> str:
    punct = "/-'?!.,#$%\'()*+-/:;<=>@[\\]^_`{|}~" + '""“”’' + '∞θ÷α•à−β∅³π‘₹´°£€\×™√²—–&'
    mapping = {"‘": "'", "₹": "e", "´": "'", "°": "", "€": "e", "™": "tm", "√": " sqrt ", "×": "x",
                     "²": "2", "—": "-", "–": "-", "’": "'", "_": "-", "`": "'", '“': '"', '”': '"', '“': '"',
                     "£": "e", '∞': 'infinity', 'θ': 'theta', '÷': '/', 'α': 'alpha', '•': '.', 'à': 'a', '−': '-',
                     'β': 'beta', '∅': '', '³': '3', 'π': 'pi', }

    for p in mapping:
        text = text.replace(p, mapping[p])

    for p in punct:
        text = text.replace(p, f' {p} ')

    specials = {'\u200b': ' ', '…': '', '\ufeff': '', 'है': ''}
    for s in specials:
        text = text.replace(s, specials[s])

    return text.strip()
