import torch.nn as nn
import torch.nn.functional as F


class EmotionRecognitionModel(nn.Module):
    def __init__(self, num_classes):
        super(EmotionRecognitionModel, self).__init__()
        # CNN layers
        # Convolution for feature extraction and normalization for faster convergence
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.bn2 = nn.BatchNorm2d(64)
        # Reduce dimensions
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)

        # BiLSTM for temporal modeling
        self.lstm = nn.LSTM(input_size=64 * 32, hidden_size=128, num_layers=2, bidirectional=True, batch_first=True)

        # Fully connected layers
        self.fc1 = nn.Linear(128 * 2, 128)  # BiLSTM output
        self.fc2 = nn.Linear(128, num_classes)

    def forward(self, x):
        # CNN feature extraction
        x = F.relu(self.bn1(self.conv1(x)))
        x = self.pool(x)
        x = F.relu(self.bn2(self.conv2(x)))
        x = self.pool(x)

        # Reshape for LSTM
        batch_size, channels, height, width = x.size()
        x = x.permute(0, 3, 1, 2).reshape(batch_size, width, -1)  # (batch, time, features)

        # LSTM for temporal modeling
        x, _ = self.lstm(x)

        # Fully connected layers
        x = F.relu(self.fc1(x[:, -1, :]))  # Use the last LSTM output
        x = self.fc2(x)
        return x