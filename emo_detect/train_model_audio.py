import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
import torch
import torchaudio
import torch.nn as nn
from torchaudio.transforms import MelSpectrogram
import torch.nn.functional as F
from torch.utils.data import DataLoader
import soundfile as sf
torch.device(device="cuda:0" if torch.cuda.is_available() else "cpu")


from torch.utils.data import Dataset

class EmotionalSpeechDataset(Dataset):
    def __init__(self, labels_files, transform=None):
        self.transform = transform
        self.file_paths = []
        self.labels = []
        
        # Read the labels file
        for labels_file in labels_files:
            os.listdir("c:/Users/henri/Documents/Uni.lu/Semester 5/NLP/Project/NLP_Project/emo_detect/dataset/EmotionSpeechDataset/0001")
            with open(labels_file, 'r') as f:
                for line in f:
                    parts = line.strip().split('\t')
                    file_name = parts[0] + '.wav'
                    label = parts[-1]
                    self.file_paths.append(os.path.join(f"c:/Users/henri/Documents/Uni.lu/Semester 5/NLP/Project/NLP_Project/emo_detect/dataset/EmotionSpeechDataset/{file_name[:4]}/{label}", file_name))
                    self.labels.append(label)
        
        # Map emotions to numerical labels
        self.label_map = {label: idx for idx, label in enumerate(set(self.labels))}
        self.labels = [self.label_map[label] for label in self.labels]

    def __len__(self):
        return len(self.file_paths)

    def __getitem__(self, idx):
        file_path = self.file_paths[idx]
        label = self.labels[idx]
        waveform, sample_rate = torchaudio.load(file_path)
        
        if self.transform:
            waveform = self.transform(waveform)
        
        return waveform, label

class EmotionRecognitionModel(nn.Module):
    def __init__(self):
        super(EmotionRecognitionModel, self).__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)
        self.fc1 = nn.Linear(16 * 32 * 32, 128)
        self.fc2 = nn.Linear(128, 5)  # Assuming 5 emotion classes

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = x.view(-1, 16 * 32 * 32)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

def pad_sequence(batch):
    # Separate the waveforms and labels
    waveforms = [item[0].squeeze(0) for item in batch]  # Remove channel dimension if necessary
    labels = torch.tensor([item[1] for item in batch])
    
    # Pad the waveforms
    waveforms_padded = torch.nn.utils.rnn.pad_sequence(waveforms, batch_first=True, padding_value=0)
    
    # Add the channel dimension back
    waveforms_padded = waveforms_padded.unsqueeze(1)
    
    return waveforms_padded, labels

def main():
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    print(f"Training on {device}")
    model = EmotionRecognitionModel().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    num_epochs = 100
    transform = torchaudio.transforms.MelSpectrogram(sample_rate=16000, n_mels=16, n_fft=512)
    labels_files = ["c:/Users/henri/Documents/Uni.lu/Semester 5/NLP/Project/NLP_Project/emo_detect/dataset/EmotionSpeechDataset/0011/0011.txt",
                    "c:/Users/henri/Documents/Uni.lu/Semester 5/NLP/Project/NLP_Project/emo_detect/dataset/EmotionSpeechDataset/0012/0012.txt",
                    "c:/Users/henri/Documents/Uni.lu/Semester 5/NLP/Project/NLP_Project/emo_detect/dataset/EmotionSpeechDataset/0013/0013.txt",
                    "c:/Users/henri/Documents/Uni.lu/Semester 5/NLP/Project/NLP_Project/emo_detect/dataset/EmotionSpeechDataset/0014/0014.txt",
                    "c:/Users/henri/Documents/Uni.lu/Semester 5/NLP/Project/NLP_Project/emo_detect/dataset/EmotionSpeechDataset/0015/0015.txt",
                    "c:/Users/henri/Documents/Uni.lu/Semester 5/NLP/Project/NLP_Project/emo_detect/dataset/EmotionSpeechDataset/0016/0016.txt",
                    "c:/Users/henri/Documents/Uni.lu/Semester 5/NLP/Project/NLP_Project/emo_detect/dataset/EmotionSpeechDataset/0017/0017.txt",
                    "c:/Users/henri/Documents/Uni.lu/Semester 5/NLP/Project/NLP_Project/emo_detect/dataset/EmotionSpeechDataset/0018/0018.txt",
                    "c:/Users/henri/Documents/Uni.lu/Semester 5/NLP/Project/NLP_Project/emo_detect/dataset/EmotionSpeechDataset/0019/0019.txt",
                    "c:/Users/henri/Documents/Uni.lu/Semester 5/NLP/Project/NLP_Project/emo_detect/dataset/EmotionSpeechDataset/0020/0020.txt",
                    ]
    dataset = EmotionalSpeechDataset(labels_files, transform=transform)

    train_loader = DataLoader(dataset, batch_size=8, shuffle=True, num_workers=4, collate_fn=pad_sequence)

    # Training loop
    for epoch in range(num_epochs):
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels.view(1, -1))
            loss.backward()
            optimizer.step()
        print(f'Epoch {epoch+1}, Loss: {loss.item()}')
    torch.save(model, "emotional_speech_model.pt")

if __name__ == '__main__':
    main()