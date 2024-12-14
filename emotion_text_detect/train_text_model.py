import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
from datasets import load_dataset
from transformers import BertTokenizer, BertForSequenceClassification, AdamW, get_scheduler
from torch.utils.data import DataLoader
from tqdm import tqdm
import torch

if __name__ == "__main__":
    # Load the dataset
    dataset = load_dataset('emotion-emotion_69k.csv')

    # Initialize the tokenizer
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    # Tokenize the dataset
    def tokenize_function(examples):
        return tokenizer(examples['text'], padding='max_length', truncation=True)
    tokenized_datasets = dataset.map(tokenize_function, batched=True)
    # Define the DataLoader
    train_dataloader = DataLoader(tokenized_datasets['train'], batch_size=16, shuffle=True)
    val_dataloader = DataLoader(tokenized_datasets['validation'], batch_size=16)
    # Load the pre-trained BERT model
    model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=6)  # Adjust num_labels as per your dataset
    # Define optimizer and scheduler
    optimizer = AdamW(model.parameters(), lr=5e-5)
    num_epochs = 3
    num_training_steps = num_epochs * len(train_dataloader)
    lr_scheduler = get_scheduler(
        name="linear", optimizer=optimizer, num_warmup_steps=0, num_training_steps=num_training_steps
    )

    # Training loop
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    model.to(device)

    for epoch in range(num_epochs):
        model.train()
        for batch in tqdm(train_dataloader):
            batch = {k: v.to(device) for k, v in batch.items()}
            outputs = model(**batch)
            loss = outputs.loss
            loss.backward()

            optimizer.step()
            lr_scheduler.step()
            optimizer.zero_grad()

        print(f"Epoch {epoch+1} completed")