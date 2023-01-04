import transformers
from transformers import BertModel, BertTokenizer, AdamW, get_linear_schedule_with_warmup
import torch
from torch import nn, optim
from torch.utils.data import Dataset, DataLoader
import torch.nn.functional as F
import numpy as np
import tensorflow as tf

PRE_TRAINED_MODEL_NAME = 'bert-base-cased'

tokenizer = BertTokenizer.from_pretrained(PRE_TRAINED_MODEL_NAME)


class SentimentClassifier(nn.Module):

    def __init__(self, n_classes):
        super(SentimentClassifier, self).__init__()
        self.bert = BertModel.from_pretrained(PRE_TRAINED_MODEL_NAME)
        self.drop = nn.Dropout(p=0.3)
        self.out = nn.Linear(self.bert.config.hidden_size, n_classes)

    def forward(self, input_ids, attention_mask):
        _, pooled_output = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask,
            return_dict=False
        )
        output = self.drop(pooled_output)
        return self.out(output)

def bert_tokenize(clean_text):
    encoded_review = tokenizer.encode_plus(
    clean_text,
    max_length=32,
    add_special_tokens=True,
    return_token_type_ids=False,
    pad_to_max_length=True,
    return_attention_mask=True,
    return_tensors='pt',
    )
    return encoded_review


def get_predictions(clean_text):
    class_names = ['negative', 'neutral', 'positive']
    encoded_review = bert_tokenize(clean_text)
    input_ids = encoded_review['input_ids']
    attention_mask = encoded_review['attention_mask']

    model = SentimentClassifier(len(class_names))
    model.load_state_dict(torch.load('best_model_state.bin', map_location=torch.device('cpu')))
    model.eval()
    output = model(input_ids, attention_mask)
    _, prediction = torch.max(output, dim=1)

    lst = []

    for i in output[0]:
        lst.append(tf.sigmoid(i.tolist()))

    print(f'Review text: {clean_text}')
    print("Sentiment Probability:", lst)
    print(f'Sentiment  : {class_names[prediction]}')
    return lst,{class_names[prediction]}


#get_predictions('ndp and liberal are never.doug ford sucks.but i have no choice. liberals has caused heavy damages to this country')