import LLMAccess
import torch
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
from styletts2 import tts as StyleTTS
from parler_tts import ParlerTTSForConditionalGeneration 
from transformers import AutoTokenizer
import numpy as np
import scipy.io.wavfile as wavfile
import emotion_text_detect.load_text_model as text_oracle

# Get the current working directory
current_directory = os.getcwd()

# Load the pre-trained StyleTTS model
device = "cuda:0" if torch.cuda.is_available() else "cpu" 
model = ParlerTTSForConditionalGeneration.from_pretrained("parler-tts/parler-tts-mini-v1").to(device) 
tokenizer = AutoTokenizer.from_pretrained("parler-tts/parler-tts-mini-v1")

def emotionalFace(prompt: str, num: int):
    """Calls the LLM module to generate a response, then generates the speech 
    and then finally generate the talking face model

    Args:
        prompt (str): User input prompt
        num (int): index of the prompt

    Returns:
        tuple: text and video
    """
    detect_emotion = text_oracle.predict_emotion(prompt, device)
    response = LLMAccess.generate_response(prompt, detect_emotion)
    audio_file = synthesize_speech(text=response, num=num, emotion=detect_emotion)
    video = create_animation(audio_file=audio_file, num=num, emotion=detect_emotion)
    return response, detect_emotion, audio_file, video

# Define a function to synthesize speech with specific emotions
def synthesize_speech(text, num, emotion):
    emotion_styles = {
        'Joy': "A cheerful and upbeat tone, with a bright and lively delivery.",
        'Sad': "A slow and melancholic tone, with a soft and gentle delivery.",
        'Anger': "A loud and intense tone, with a forceful and aggressive delivery.",
        'Fear': "A trembling and cautious tone, with a hesitant and shaky delivery.",
        'Love': "A warm and tender tone, with a gentle and affectionate delivery.",
        'Surprise': "A high-pitched and excited tone, with a sudden and emphatic delivery."
    }

    style_description = emotion_styles.get(emotion.lower(), "A neutral and clear tone, with a standard delivery.")
    input_style = tokenizer(style_description, return_tensors="pt")
    input_text = tokenizer(text, return_tensors="pt")
#
    input_ids = input_style.input_ids.to(device)
    prompt_input_ids = input_text.input_ids.to(device)
    attention_mask = input_style.attention_mask.to(device)
    prompt_attention_mask = input_text.attention_mask.to(device)
    # Generate speech
    generation = model.generate(input_ids=input_ids,
                                prompt_input_ids=prompt_input_ids,
                                attention_mask=attention_mask,
                                prompt_attention_mask=prompt_attention_mask)
#
    # Save the audio to a file
    # Convert to numpy array and ensure correct format 
    audio = generation.cpu().detach().numpy() 
    audio = np.squeeze(audio) 
    if audio.ndim == 1: 
        audio = np.expand_dims(audio, axis=0) 
    # Normalize the audio to the range [-1, 1] 
    audio = audio / np.max(np.abs(audio)) 
    # Convert to 16-bit PCM format 
    audio = (audio * 32767).astype(np.int16)
    
    wav_path = f"audio_result/output_{num}_audio.wav" 
    wavfile.write(wav_path, model.config.sampling_rate, audio.T) 
    # Convert WAV to MP3 using pydub 
    return wav_path

        
def create_animation(num: int, emotion: str, audio_file: str):
    """Generates synchronized MP4 file with emotional faces

    Args:
        text (str): User input prompt
        num (int): Running index of prompt
        emotion (str): Emotional damage
        audio_file (str): Path to WAV file

    Returns:
        _type_: File name or NoneType
    """
    # Set the input paths 
    image_path = "input_image.gif" 
    audio_path = audio_file 
    output_path = f"output_{num}_video.mp4"
    os.system(f"C:/Users/henri/anaconda3/envs/nlp_project/python.exe inference.py --checkpoint_path checkpoints/wav2lip.pth --face {image_path} --audio {audio_path} --outfile {output_path}")
    return output_path