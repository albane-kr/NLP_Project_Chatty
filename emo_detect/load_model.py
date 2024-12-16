import os
os.environ['KMP_DUPLICATE_LIB_OK']='TRUE'
from EmotionRecognitionModel import EmotionRecognitionModel
import torch

model = EmotionRecognitionModel(num_classes=5).load_state_dict(torch.load(os.getcwd()+'/emo_detect/best_emotion_model.pth'))