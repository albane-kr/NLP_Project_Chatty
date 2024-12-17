import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
import pyaudio
import speech_recognition as sr
import wave
#from emo_detect.EmotionRecognitionModel import EmotionRecognitionModel
from emo_detect.load_model import predict

def record_audio(duration: int, filename: str) -> tuple:
    """Records audio of duration 'duration' and saves it in file 'filename'. Returns a (filename, text, emotion)"""
    # Set up parameters for recording
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1  # Mono
    rate = 44100  # Record at 44100 samples per second

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print("Recording...")

    # Open a new stream for recording
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=rate,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for the specified duration
    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()

    # Terminate the PortAudio interface
    p.terminate()

    print("Recording finished.")

    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Save the recorded data as a WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        text, emotion = transcribe_audio(filename)
    return filename, text, emotion

def transcribe_audio(filename: str) -> tuple:
    """Transscribes the audio, and makes emotion prediction, returns (text, emotion)"""
    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Load the audio file
    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)  # Read the entire audio file

    # Recognize (convert from speech to text)
    try:
        text = recognizer.recognize_google(audio_data)
        print("Transcription: " + text)
        emotion = predict(filename)
        return text, emotion
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
        return "", ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return "", ""