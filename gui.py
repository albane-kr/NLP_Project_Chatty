# Project 1
# Henrik Klasen & Albane Keraudren-Riguidel

import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
import warnings
warnings.filterwarnings('ignore')
from tkinter import *
from tkinter import ttk
import emotionalFace
from moviepy.editor import VideoFileClip
from PIL import Image, ImageTk
from threading import Thread
import time
from record_audio import record_audio

__author__ = "Albane Keraudren-Riguidel, Henrik Klasen"

#################################################################
#                                                               #
#      ######  #    #   #####   #######  #######   #    #       #
#     #        #    #  #     #     #        #       #  #        #
#     #        ######  #######     #        #        ##         #
#     #        #    #  #     #     #        #        ##         #
#      ######  #    #  #     #     #        #        ##         #
#                                                               #
#################################################################

def num():
    """
    A simple iterator counting in increments of 1.
    """
    num = 0
    yield num
    while True:
        num += 1
        yield num
n = num()
emotion_global = ""
def sendText():
    """
    This function is triggred upon press of the send button. It passes the text input on to the 
    emotionalFace.emotionalFace() function. It distinguishes here, if the input was audio (already
    detected an emotion), or text (emotion detection to do).
    """
    global video_path, emotion_global
    userInput = entrybox.get()
    if userInput:
        textDisplay.insert(END, f"You => {userInput}\n")
        entrybox.delete(0, END)
        print(emotion_global)
        if emotion_global != "":
            response_gemini, emotion, _, video_path = emotionalFace.emotionalFace(userInput, next(n), emotion_global) 
        else:
            response_gemini, emotion, _, video_path = emotionalFace.emotionalFace(userInput, next(n)) 

        emotion_global=""
        playVideo(video_path)
        textDisplay.insert(END, f"Chatty => You sound {emotion}\n{response_gemini}")

def playVideo(videoPath: str):
    """
    Plays the MP4 video, with more or less good lip syncing.

    @param videoPath, the filename of the video.

    Description: This function uses multithreading for playing the video 
    and audio simultaneously. It separates the audio from the video and plays it in a separate thread.
    """
    global videoLabel, videoClip, audio_thread
    currentVideoPath = os.getcwd() + "\\results\\" + videoPath
    if not os.path.exists(currentVideoPath):
        print("Error: Video file does not exist at path: ", currentVideoPath)
        return
    
    print("Opening video file: ", currentVideoPath)
    videoClip = VideoFileClip(currentVideoPath)
    
    def updateFrame():
        """
        Plays and updates the video frame.
        """
        try:
            frame = videoClip.get_frame(videoClip.reader.pos / videoClip.fps)
            frame = Image.fromarray(frame)
            imageTkinter = ImageTk.PhotoImage(image=frame)
            videoLabel.imageTkinter = imageTkinter
            videoLabel.configure(image=imageTkinter)
            videoLabel.after(int(1000 / videoClip.fps), updateFrame)  # Adjust delay for frame rate
        except Exception as e:
            print(f"Error: {e}")
            videoClip.reader.close()
            replayButton.configure(state=NORMAL)
    
    audio_thread = Thread(target=playAudio, args=(videoClip,))
    audio_thread.start()
    updateFrame()  # Start the video loop
    replayButton.configure(state=NORMAL)

def playAudio(videoClip: VideoFileClip):
    """
    Plays audio
    @param videoClip: VideoFileClip, takes MP4 and separates audio channel.

    Description: This function plays the audio track of the video and then in its own thread.
    """
    videoClip.audio.preview()

def replayVideo():
    """
    Triggered upon click on the replay button

    Replays the video by calling the playVideo function.
    """
    replayButton.configure(state=DISABLED)
    playVideo(videoPath=video_path)

def startRecording():
    """
    Starts the recording process and the progress bar
    """
    recordButton.configure(state=DISABLED)
    progressBar['value'] = 0
    progressBar.update()
    progressThread = Thread(target=updateProgressBar)
    progressThread.start()
    recordThread = Thread(target=recordAndProcess)
    recordThread.start()

def recordAndProcess():
    """
    Records audio using the record_audio.py module. 
    Gets transscribed text, as well as detected emotion from the machine learning model.
    Emotion is stored in a global variable, for the sendText-function to pass to emotionalFace
    """
    global emotion_global
    _, text, audio_emotion = record_audio(10, "./audio_in/output{n}.wav")
    emotion_global = audio_emotion
    entrybox.insert(0, text)
    recordButton.configure(state=NORMAL)

def updateProgressBar():
    """
    Updates the progress bar every second
    (10s for completing the audio)
    """
    for i in range(10):
        time.sleep(1)
        progressBar['value'] += 10
        progressBar.update()

# Constants for graphics
BG_COLOR = "#fff2cc"
TEXT_BOLD_COLOR = "#f3840f"
TEXT_ENTRY_COLOR = "#e06666"
TEXT_DISPLAY_COLOR = "#2e684e"
FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 15 bold"
ENTRYBOX_BG_COLOR = "#ffd966"
SENDBUTTON_BG_COLOR = "#2e684e"

root = Tk()
root.title("Chatty the emotional chatbot")

root.state("zoomed")
root.configure(background=BG_COLOR)

title = Label(root, bg=BG_COLOR, fg=TEXT_BOLD_COLOR, text="Welcome! Talk to Chatty", font=FONT_BOLD, pady=10, width=40, height=2)
title.grid(row=0, column=0, columnspan=3, sticky="ew")

textDisplay = Text(root, bg=BG_COLOR, fg=TEXT_DISPLAY_COLOR, font=FONT, width=50, height=30)
textDisplay.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=(10, 5))

scrollbar = Scrollbar(textDisplay)
scrollbar.place(relheight=1, relx=0.985)

entrybox = Entry(root, bg=ENTRYBOX_BG_COLOR, fg=TEXT_ENTRY_COLOR, font=FONT, width=35)
entrybox.grid(row=2, column=0, sticky="ew", padx=(10, 0), pady=(0, 20))

sendButton = Button(root, text="Send", font=FONT_BOLD, bg=TEXT_BOLD_COLOR, command=sendText)
sendButton.grid(row=2, column=1, sticky="ew", padx=(0, 10), pady=(0, 20))

recordButton = Button(root, text="Record", font=FONT_BOLD, bg=TEXT_BOLD_COLOR, command=startRecording)
recordButton.grid(row=3, column=0, columnspan=2, sticky="ew", padx=(10, 10), pady=(0, 20))

progressBar = ttk.Progressbar(root, orient=HORIZONTAL, length=100, mode='determinate')
progressBar.grid(row=4, column=0, columnspan=2, sticky="ew", padx=(10, 10), pady=(0, 20))

videoFrame = ttk.Frame(root, width=400, height=300, relief=RIDGE, style="VideoFrame.TFrame")
videoFrame.grid(row=1, column=2, padx=(5, 10), pady=10, sticky="nsew")

videoLabel = Label(videoFrame, bg=BG_COLOR)
videoLabel.pack(expand=True, fill="both")

replayButton = Button(root, text="Replay Video", font=FONT_BOLD, bg=TEXT_BOLD_COLOR, command=replayVideo, state=DISABLED)
replayButton.grid(row=2, column=2, sticky="ew", padx=(5, 10), pady=(20))

style = ttk.Style()
style.configure("VideoFrame.TFrame", BG_COLOR)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=0)
root.columnconfigure(2, weight=1)
root.rowconfigure(1, weight=1)

root.mainloop()