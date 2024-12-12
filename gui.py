#Project 1
#Henrik Klasen & Albane Keraudren-Riguidel

#tutorial: https://medium.com/@marketing_75744/how-to-use-llama-3-1-with-python-a-comprehensive-guide-5580cff378d5

from tkinter import *
from tkinter import ttk
from dotenv import load_dotenv
import emotionalFace
from pydub import AudioSegment 
from pydub.playback import play
import cv2
from PIL import Image, ImageTk
import os

load_dotenv()

def num():
    num = 0
    yield num
    while True:
        num += 1
        yield num
n = num()

def sendText():
    userInput = entrybox.get()
    if userInput:
        textDisplay.insert(END, f"You => {userInput}\n")
        entrybox.delete(0, END)
        response_gemini, wav_path, video_path = emotionalFace.emotionalFace(userInput, next(n))
        #audio_segment = AudioSegment.from_wav(wav_path) 
        playVideo(video_path, wav_path)
        #play(audio_segment)
        textDisplay.insert(END, f"Chatty => {response_gemini}\n Tokens used: {wav_path}\n")
        
###### For testing ######
# def sendText():
#     userInput = entrybox.get()
#     if userInput:
#         textDisplay.insert(END, f"You => {userInput}\n")
#         entrybox.delete(0, END)
#         textDisplay.insert(END, "\n" + "Chatty => Hi there, how can I help?\n")
#         playVideo("C:/Users/.../NLP_Project/results/output_1.mp4", "C:/Users/.../NLP_Project/results/audio_result/output_1_audio.wav")

def playVideo(videoPath, audioPath):
    global videoCapture, currentVideoPath
    currentVideoPath = videoPath
    if not os.path.exists(videoPath):
        print("Error: Video file does not exist at path: ", videoPath)
        return
    
    print("Opening video file: ", videoPath)
    videoCapture = cv2.VideoCapture(videoPath)
    if not videoCapture.isOpened():
        print("Error: could not open video")
        return
    print("Video opened successfully")
    
    audioSegment = AudioSegment.from_file(audioPath) 
    play(audioSegment)
    
    def updateFrame():
        """reads frames from video file and converts them to TKinter format
        """
        frameReadSuccessfully, frame = videoCapture.read()
        if frameReadSuccessfully:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            imageTkinter = ImageTk.PhotoImage(image=image)
            videoLabel.imageTkinter = imageTkinter
            videoLabel.configure(image=imageTkinter)
            videoLabel.after(10, updateFrame) #delay to be verified and adjusted
        else:
            videoCapture.release()
            replayButton.configure(state=NORMAL)
    updateFrame() # loop for continuous display

def replayVideo():
    replayButton.configure(state=DISABLED)
    playVideo(currentVideoPath)

#constants for graphics
BG_COLOR = "#fff2cc"
TEXT_BOLD_COLOR = "#f3840f"
TEXT_ENTRY_COLOR = "#e06666"
TEXT_DISPLAY_COLOR = "#2e684e"
FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 15 bold"
ENTRYBOX_BG_COLOR =  "#ffd966"
SENDBUTTON_BG_COLOR = "#2e684e"

root = Tk()
root.title("Chatty the emotional chatbot")

root.state("zoomed")
root.configure(background=BG_COLOR)

title = Label(root, bg=BG_COLOR, fg=TEXT_BOLD_COLOR, text="Welcome! Talk to Chatty", font=FONT_BOLD, pady=10, width=40, height=2)
title.grid(row=0, column=0, columnspan=3, sticky="ew")

textDisplay = Text(root, bg=BG_COLOR, fg=TEXT_DISPLAY_COLOR, font=FONT, width=50, height=30)
textDisplay.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=(10,5))

scrollbar = Scrollbar(textDisplay)
scrollbar.place(relheight=1, relx=0.985)

entrybox = Entry(root, bg=ENTRYBOX_BG_COLOR, fg=TEXT_ENTRY_COLOR, font=FONT, width=35)
entrybox.grid(row=2, column=0, sticky="ew", padx=(10,0), pady=(0,20))

sendButton = Button(root, text="Send", font=FONT_BOLD, bg=TEXT_BOLD_COLOR, command=sendText)
sendButton.grid(row=2, column=1, sticky="ew", padx=(0,10), pady=(0,20))

videoFrame = ttk.Frame(root, width=400, height=300, relief=RIDGE, style="VideoFrame.TFrame")
videoFrame.grid(row=1, column=2, padx=(5,10), pady=10, sticky="nsew")

videoLabel = Label(videoFrame, bg=BG_COLOR)
videoLabel.pack(expand=True, fill="both")

replayButton = Button(root, text="Replay Video", font=FONT_BOLD, bg=TEXT_BOLD_COLOR, command=replayVideo, state=DISABLED)
replayButton.grid(row=2, column=2, sticky="ew", padx=(5,10), pady=(20))

style = ttk.Style()
style.configure("VideoFrame.TFrame", BG_COLOR)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=0)
root.columnconfigure(2, weight=1)
root.rowconfigure(1, weight=1)

root.mainloop()
