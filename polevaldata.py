import requests
import shutil
import zipfile
import numpy as np
from keras.preprocessing.sequence import pad_sequences
# POBRANIE DANYCH
def download(address):
  filename = address.split("/")[-1]
  r = requests.get(address, stream=True)
  if r.status_code == 200:
    with open(filename, 'wb') as f:
      r.raw.decode_content = True
      shutil.copyfileobj(r.raw, f)        


def encode_data(sent_list, tokenizer, max_len):
  encoded_list = []
  mask_list = []
  for sent in sent_list:
    encoded = tokenizer.encode(sent, add_special_tokens=True)
    encoded_list.append(encoded)
  padded = pad_sequences(encoded_list, maxlen=max_len, dtype="long", value=0, truncating="post", padding="post")
  for sent in padded:
    mask_list.append([int(x == 1) for x in sent])
  return padded, mask_list


def evaluate_predictions(predictions, true_labels):
  TP, FP, TN, FN = 0, 0, 0, 0
  for s, g in zip(predictions, true_labels):
    if s == 1 and g == 1:
      TP +=1
    elif s ==1:
      FP +=1
    elif g ==1:
      FN +=1
    else:
      TN +=1

  precision = TP/(TP+FP)
  recall = TP/(TP+FN)
  f1 = 2* ((precision * recall)/(precision + recall))
  print("precision: {}, recall: {}, f1: {}".format(precision, recall, f1))
  return precision, recall, f1

def get_data():
  download("http://2019.poleval.pl/task6/task_6-1.zip")
  with zipfile.ZipFile("task_6-1.zip", 'r') as zip_ref:
    zip_ref.extractall()

  download("http://2019.poleval.pl/task6/task6_test.zip")
  with zipfile.ZipFile("task6_test.zip", 'r') as zip_ref:
    zip_ref.extractall()

  # wczytywanie danych
  with open("training_set_clean_only_text.txt") as f:
    txt = f.read()
    training_sents = txt.split("\n")[:-1]

  with open("training_set_clean_only_tags.txt") as f:
    txt = f.read()
    training_labels = [int(x) for x in txt.split("\n")[:-1]]

  with open("Task6/task 01/test_set_clean_only_text.txt") as f:
    txt = f.read()
    test_sents = txt.split("\n")[:-1]

  with open("Task6/task 01/test_set_clean_only_tags.txt") as f:
    txt = f.read()
    test_labels = [int(x) for x in txt.split("\n")[:-1]]


  return training_sents, training_labels, test_sents, test_labels
