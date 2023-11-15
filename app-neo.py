import pandas as pd
import torch
from transformers import GPT2Tokenizer, GPTNeoForCausalLM, Trainer, TrainingArguments
from torch.utils.data import Dataset

class CustomDataset(Dataset):
    def __init__(self, encodings):
        self.encodings = encodings

    def __getitem__(self, idx):
        item = {key: val[idx].clone().detach() for key, val in self.encodings.items()}
        item['labels'] = item['input_ids'].clone()
        return item

    def __len__(self):
        return len(self.encodings.input_ids)

df = pd.read_csv('updated_data.csv')

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
tokenizer.pad_token = tokenizer.eos_token

train_encodings = tokenizer(df['cleaned_post'].tolist(), truncation=True, padding=True, max_length=512, return_tensors="pt")

train_dataset = CustomDataset(train_encodings)

model = GPTNeoForCausalLM.from_pretrained('EleutherAI/gpt-neo-125M')

training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=4,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset
)

trainer.train()

# Save the trained model and tokenizer
model.save_pretrained('./trained_model_neo')
tokenizer.save_pretrained('./trained_model_neo')
