#Project 1
#Henrik Klasen & Albane Keraudren-Riguidel

from tkinter import *

def sendText():
    send = "You => " + entrybox.get()
    textDisplay.insert(END, "\n" + send)
 
    userInput = entrybox.get().lower()
    
    if (userInput != ""):
        if (userInput == "hello"):
            textDisplay.insert(END, "\n" + "Chatty => Hi there, how can I help?")
    else:
        textDisplay.insert(END, "\n" + "Chatty => Sorry, I didn't understand. Could you write again?")
 
    entrybox.delete(0, END)

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
