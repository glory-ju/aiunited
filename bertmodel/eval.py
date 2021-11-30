import pandas as pd
import torch
from torch import nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import gluonnlp as nlp
import numpy as np
from tqdm import tqdm

#kobert
from KoBERT.kobert.utils import get_tokenizer
from KoBERT.kobert.pytorch_kobert import get_pytorch_kobert_model, get_kobert_model
from KoBERT.kobert_hf.kobert_tokenizer import KoBERTTokenizer

tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1')
tokenizer.encode("한국어 모델을 공유합니다.")

bertmodel, vocab = get_kobert_model('skt/kobert-base-v1', tokenizer.vocab_file)

# inference
device = torch.device('cuda')
model = BERTClassifier(bertmodel, dr_rate=0.5).to(device)
model.load_state_dict(torch.load('model_for_inference.pt'))
model.to(device)

# new review dataframe
df = pd.read_csv('seohae_pre.csv')
df = df.dropna()

df['new_score'] = df['preprocessed_review'].apply(predict) # predict의 인자로 df['preprocessed_review'](type:str)이 들어가고 리턴값이 apply에 들어감
df.to_csv('seohae_review.csv', encoding='utf-8', index=False)