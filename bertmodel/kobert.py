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

#transformers
from transformers import AdamW
from transformers.optimization import get_cosine_schedule_with_warmup

def dataload():
    # GPU settings
    device = torch.device("cuda:0")

    # model settings
    # bertmodel, vocab = get_pytorch_kobert_model()
    from KoBERT.kobert_hf.kobert_tokenizer import KoBERTTokenizer

    tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1')
    # tokenizer.encode("한국어 모델을 공유합니다.")

    bertmodel, vocab = get_kobert_model('skt/kobert-base-v1', tokenizer.vocab_file)

    # data load
    DATA = pd.read_csv('final_dec_review.csv')

    DATA = DATA.dropna()

    data_list = []
    for q, label in zip(DATA['review'], DATA['score']):
        data = []
        data.append(q)
        data.append(str(int(label)))

        data_list.append(data)

    # data_list = data_list[:1000]

    return device, data_list, bertmodel, vocab

    device, data_list, bertmodel, vocab = main()

def kobert_train_test(device, data_list, bertmodel, vocab):
        # train & test split
    from sklearn.model_selection import train_test_split

    dataset_train, dataset_test = train_test_split(data_list, test_size=0.25, random_state=0)


    # Setting parameters
    max_len = 64
    batch_size = 4
    warmup_ratio = 0.1
    num_epochs = 3
    max_grad_norm = 1
    log_interval = 200
    learning_rate = 5e-5

    # tokenize
    tokenizer = get_tokenizer()
    tok = nlp.data.BERTSPTokenizer(tokenizer, vocab, lower=False)

    # input data settings
    data_train = BERTDataset(dataset_train, 0, 1, tok, max_len, True, False)
    data_test = BERTDataset(dataset_test, 0, 1, tok, max_len, True, False)

    train_dataloader = torch.utils.data.DataLoader(data_train, batch_size=batch_size)
    test_dataloader = torch.utils.data.DataLoader(data_test, batch_size=batch_size)

    # Prepare optimizer and schedule (linear warmup and decay)
    no_decay = ['bias', 'LayerNorm.weight']
    optimizer_grouped_parameters = [
        {'params': [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)],
        'weight_decay': 0.01},
        {'params': [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}
    ]

    optimizer = AdamW(optimizer_grouped_parameters, lr=learning_rate)
    loss_fn = nn.CrossEntropyLoss()

    t_total = len(train_dataloader) * num_epochs
    warmup_step = int(t_total * warmup_ratio)

    scheduler = get_cosine_schedule_with_warmup(optimizer, num_warmup_steps=warmup_step, num_training_steps=t_total)

    def calc_accuracy(X, Y):
        max_vals, max_indices = torch.max(X, 1)
        train_acc = (max_indices == Y).sum().data.cpu().numpy() / max_indices.size()[0]
        return train_acc

    for e in range(num_epochs):
        train_acc = 0.0
        test_acc = 0.0
        model.train()
        for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(tqdm(train_dataloader)):
            optimizer.zero_grad()
            token_ids = token_ids.long().to(device)
            segment_ids = segment_ids.long().to(device)
            valid_length = valid_length
            label = label.long().to(device)
            out = model(token_ids, valid_length, segment_ids)
            loss = loss_fn(out, label)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_grad_norm)
            optimizer.step()
            scheduler.step()  # Update learning rate schedule
            train_acc += calc_accuracy(out, label)
            if batch_id % log_interval == 0:
                print("epoch {} batch id {} loss {} train acc {}".format(e + 1, batch_id + 1, loss.data.cpu().numpy(),
                                                                        train_acc / (batch_id + 1)))
        print("epoch {} train acc {}".format(e + 1, train_acc / (batch_id + 1)))

        model.eval()
        for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(tqdm(test_dataloader)):
            token_ids = token_ids.long().to(device)
            segment_ids = segment_ids.long().to(device)
            valid_length = valid_length
            label = label.long().to(device)
            out = model(token_ids, valid_length, segment_ids)
            test_acc += calc_accuracy(out, label)
        print("epoch {} test acc {}".format(e + 1, test_acc / (batch_id + 1)))

    torch.save(model.state_dict(), 'model_for_inference.pt')

    

    # end = 1
    # while end == 1:
    #     sentence = input("하고싶은 말을 입력해주세요 : ")
    #     if sentence == 0:
    #         break
    #     predict(sentence)
    #     print("\n")
