import os
os.environ['KMP_DUPLICATE_LIB_OK']='TRUE'
from EmotionRecognitionModel import EmotionRecognitionModel
import torch
import librosa
import numpy as np
import torch.nn.functional as F

model = torch.load(os.getcwd() + "/emo_detect/best.pt")

def predict(file):
    """
    @param file: wav file to read
    -> returns emotion recognized from wav-file
    """
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    pred = 0
    vec = extract_log_mel_spectrogram(file)
    model.to(device)
    model.eval()
    log_mel_spec = torch.tensor(log_mel_spec, dtype=torch.float32).unsqueeze(0).to(device)  # Add channel dim
    with torch.no_grad():
        pred = model(log_mel_spec)
        probabilities = F.softmax(pred, dim=1)

        # Get the index of the highest probability
        predicted_class_idx = torch.argmax(probabilities, dim=1).item()

        # Define your label mapping
        emo_dict = {0: 'Angry', 1: 'Happy', 2: 'Neutral', 3: 'Sad', 4:'Surprise'}


        # Map the predicted index to the corresponding label
        predicted_label = emo_dict[predicted_class_idx]
        print(predicted_label)
    return predicted_label

def extract_log_mel_spectrogram(audio_path, n_mels=128, duration=3, sr=22050):
    signal, sr = librosa.load(audio_path, sr=sr, duration=duration)
    mel_spec = librosa.feature.melspectrogram(y=signal, sr=sr, n_mels=n_mels, fmax=8000)
    log_mel_spec = librosa.power_to_db(mel_spec, ref=np.max)
    return log_mel_spec

