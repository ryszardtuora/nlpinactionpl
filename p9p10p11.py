import numpy as np
import random
import torch # PyTorch
from tqdm import tqdm
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
from transformers import *
from polevaldata import get_data, encode_data, evaluate_predictions


seed_val = 123
random.seed(seed_val)
np.random.seed(seed_val)
torch.manual_seed(seed_val)

# w PyTorch konieczne jest określenie sprzętu na którym wykonywane będą obliczenia
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


train_sents, train_labels, test_sents, test_labels = get_data()

# oversampling, aby zapewnić równowagę liczebności etykiet
pstv_sents = [train_sents[i] for i in range(len(train_sents)) if train_labels[i] == 1]
train_sents.extend(pstv_sents * 4)
train_labels.extend([1 for _ in range(len(pstv_sents) * 4)])
indices = list(range(len(train_sents)))

# tasowanie danych
random.shuffle(indices)
train_sents = [train_sents[i] for i in indices]
train_labels = [train_labels[i] for i in indices]

# ładowanie sparowanego z modelem tokenizatora
MAX_LEN = 64
tokenizer = BertTokenizer.from_pretrained("dkleczek/bert-base-polish-cased-v1")

# padding danych
encoded_train, train_masks = encode_data(train_sents, tokenizer, MAX_LEN)
encoded_test, test_masks = encode_data(test_sents, tokenizer, MAX_LEN)

# konwersja danych do tensora dla PyTorch
train_inputs = torch.tensor(encoded_train)
train_labels = torch.tensor(train_labels)
train_masks = torch.tensor(train_masks)


# Przygotowanie DataLoadera
data = TensorDataset(train_inputs, train_masks, train_labels)
sampler = RandomSampler(data)
dataloader = DataLoader(data, sampler=sampler, batch_size=32)

model = BertForSequenceClassification.from_pretrained(
    "dkleczek/bert-base-polish-cased-v1",
    num_labels = 2, # klasyfikujemy teksty jako podpadające lub nie pod cyberbullying   
    output_attentions = False, # Zwracanie wag uwagi
    output_hidden_states = False, # Zwracanie wszystkich stanów ukrytych
)
model.to(device)

optimizer = AdamW(model.parameters(), lr = 2e-5, eps = 1e-8)
EPOCHS = 4
num_steps = len(dataloader) * EPOCHS # liczba wsadów razy liczba epok

scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps = 0,
                                            num_training_steps = num_steps)

#TRAINING
for epoch in range(0, EPOCHS): 
    total_loss = 0
    model.train() # tryb treningowy, akumulacja gradientów jest włączona
    print("\nepoka: ", epoch + 1)
    for step, batch in tqdm(enumerate(dataloader)):
        batch_input_ids = batch[0].to(device) # przenoszenie danych do pamięci
        batch_input_mask = batch[1].to(device)
        batch_labels = batch[2].to(device)
        model.zero_grad() # czyszczenie zakumulowanych z poprzedniego batcha gradientów
        outputs = model(batch_input_ids, 
                    token_type_ids=None, 
                    attention_mask=batch_input_mask, 
                    labels=batch_labels)
        loss = outputs[0]
        total_loss += loss.item() # funkcja straty z całej epoki
        loss.backward() # propagacja wsteczna błędu
        # Obcinanie gradientów, dla uniknięcia problemu eksplodujących gradientów
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step() # optymalizator modyfikuje parametry
        scheduler.step() # zmiana współczynnika szybkości uczenia
    print(total_loss)


# konwersja danych do tensora dla PyTorch
test_inputs = torch.tensor(encoded_test)
test_labels = torch.tensor(test_labels)
test_masks = torch.tensor(test_masks)

# Przygotowanie DataLoadera
data = TensorDataset(test_inputs, test_masks, test_labels)
dataloader = DataLoader(data, batch_size=32)


model.zero_grad()
model.eval() # tryb testowy, akumulacja gradientów jest wyłączona
predictions = []
with torch.no_grad():
  for step, batch in tqdm(enumerate(dataloader)):
    batch_input_ids = batch[0].to(device)
    batch_input_mask = batch[1].to(device)
    outputs = model(batch_input_ids, 
                    attention_mask=batch_input_mask)
    logits = outputs[0]
    logits = logits.detach().cpu().numpy()
    predictions.extend(logits)

predicted_classes = np.argmax(predictions, axis=1)
evaluation = evaluate_predictions(predicted_classes, test_labels)
print("precyzja: {}, czułość: {}, f1: {}".format(*evaluation))
#precyzja: 0.8392857142857143, czułość: 0.35074626865671643, f1: 0.4947368421052632
