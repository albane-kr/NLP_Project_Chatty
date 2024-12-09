#Project 1
#Henrik Klasen & Albane Keraudren-Riguidel

#tutorial: https://medium.com/@marketing_75744/how-to-use-llama-3-1-with-python-a-comprehensive-guide-5580cff378d5

from tkinter import *
import json
from os import getenv
from dotenv import load_dotenv
import emotionalFace

load_dotenv()

#initializing Llama API
# llama_api_token = getenv("LLAMA_API_TOKEN")
# llama = LlamaAPI(llama_api_token)
num = 0

def sendText():
    userInput = entrybox.get()
    textDisplay.insert(END, f"You => {userInput}\n")
    entrybox.delete(0, END)
    
    #request for Llama API wtih json format
    # request_json = {
    #     #"model": ---see which model to use
    #     "messages": [
    #         {"role": "user", "content": userInput}
    #     ],
    #     #if true, response returned in "real-time", else response returned in one block (complete response)
    #     "stream":TRUE
    # }
    
    # response_llama = llama.run(request_json)
    # print(response_llama)
    # #access the response first choice ---see how to get the best response
    # #get the message dictionary and associated content field
    # response_chatbot = response_llama.json()['choices'][0]['message']['content'].strip()
    
    #response from openai
    # openai.api_key = getenv("OPENAI_API_TOKEN")
    response_gemini, video = emotionalFace.emotionalFace(userInput, num)
    # response_chatbot = response_openai.choices[0].text.strip()
    
    # tokens_used = response_openai['usage']['prompt_tokens']
    textDisplay.insert(END, f"Chatty => {response_gemini}\n Tokens used: {video}\n")

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
root.title("Chatbot")

root.state("normal")
##windows only
root.configure(background=BG_COLOR)

title = Label(root, bg=BG_COLOR, fg=TEXT_BOLD_COLOR, text="Talk to me if you don't want to fail", font=FONT_BOLD, pady=10, width=40, height=5)
title.grid(row=0)
# lable1 = Label(root, bg=BG_COLOR, fg=TEXT_COLOR, text="Welcome", font=FONT_BOLD, pady=10, width=20, height=1).grid(
# 	row=0)

textDisplay = Text(root, bg=BG_COLOR, fg=TEXT_DISPLAY_COLOR, font=FONT, width=100)
textDisplay.grid(row=1, column=0, columnspan=2)

scrollbar = Scrollbar(textDisplay)
scrollbar.place(relheight=1, relx=0.985)

entrybox = Entry(root, bg=ENTRYBOX_BG_COLOR, fg=TEXT_ENTRY_COLOR, font=FONT, width=95)
entrybox.grid(row=2, column=0)

sendButton = Button(root, text="Send", font=FONT_BOLD, bg=TEXT_BOLD_COLOR, command=sendText)
sendButton.grid(row=2, column=1)

root.mainloop()
