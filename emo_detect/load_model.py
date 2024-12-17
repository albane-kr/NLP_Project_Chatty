import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
from emo_detect.EmotionRecognitionModel import EmotionRecognitionModel
import torch
import librosa
import numpy as np
import torch.nn.functional as F

def predict(file):
    """
    @param file: wav file to read
    -> returns emotion recognized from wav-file
    """

    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    model = EmotionRecognitionModel(num_classes=5).to(device)
    model.load_state_dict(torch.load(os.getcwd() + "/emo_detect/best_emotion_model.pth", weights_only=True))

    vec = extract_log_mel_spectrogram(file)
    model.eval()
    log_mel_spec = torch.tensor(vec, dtype=torch.float32).unsqueeze(0).unsqueeze(0).to(device)  # Add batch and channel dims
    print(log_mel_spec.shape)
    max_width = 32  # Adjust to match the expected input shape
    if max_width is not None:
        log_mel_spec = _pad_or_truncate(log_mel_spec, max_width)

    with torch.no_grad():
        pred = model(log_mel_spec)
        print(pred)
        probabilities = F.softmax(pred, dim=1)
        print(probabilities)
        # Get the index of the highest probability
        predicted_class_idx = torch.argmax(probabilities, dim=1).item()

        # Define your label mapping
        emo_dict = {0: 'Angry', 1: 'Happy', 2: 'Neutral', 3: 'Sad', 4: 'Surprise'}

        # Map the predicted index to the corresponding label
        predicted_label = emo_dict[predicted_class_idx]
        print(predicted_label)
    return predicted_label

def extract_log_mel_spectrogram(audio_path, n_mels=128, duration=3, sr=22050):
    """Extracts the spectrogram of a given .wav file"""
    signal, sr = librosa.load(audio_path, sr=sr, duration=duration)
    mel_spec = librosa.feature.melspectrogram(y=signal, sr=sr, n_mels=n_mels, fmax=8000)
    log_mel_spec = librosa.power_to_db(mel_spec, ref=np.max)
    return log_mel_spec

def _pad_or_truncate(spec, max_width):
    _, _, height, width = spec.shape  # Adjust to handle 4D tensor
    if width < max_width:
        # Pad with zeros along the time dimension
        pad_width = max_width - width
        spec = F.pad(spec, (0, pad_width))  # Pad last dimension (time)
    else:
        # Truncate along the time dimension
        spec = spec[:, :, :, :max_width]
    return spec