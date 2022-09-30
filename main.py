#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ev3dev2.display import Display
import ev3dev2.fonts as fonts

from PIL import Image

display = Display()

logo = Image.open("1.png")
back = Image.open("2.png")
bksp = Image.open("3.png")
shft = Image.open("4.png")
refr = Image.open("5.png")
display.draw.bitmap((0, 0), logo)

display.update()

from PIL import ImageFont

font = ImageFont.truetype("font.ttf", 12)

from telethon import TelegramClient
from telethon import sync
import re
from ev3dev2.button import Button
import time
import json

with open("config.json") as f:
	config = json.load(f)


api_id = config["api_id"]
api_hash = config["api_hash"]

menuSelectedDialog = 0
selectedMessage = 0
dialogsTitles = []
dialogMessages = []

removeFormatting = True
showReplies = False
showEmoji = True

btn = Button()

keyboard = [
        "QWERTYUIOP",
        "ASDFGHJKL",
        "ZXCVBNM",
        " "
]
keybrdPos = [0,0]
messageText = ""

capsLock = True

def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

def menuUp(state):
    global menuSelectedDialog
    if state:
        if menuSelectedDialog != 0:
            menuSelectedDialog -= 1
        renderDialogMenu()

def menuDown(state):
    global menuSelectedDialog
    if state:
        if menuSelectedDialog != 7:
            menuSelectedDialog += 1
        renderDialogMenu()

def keybrdLeft(state):
    global keybrdPos
    if state:
        if keybrdPos[1] == 0 and keybrdPos[0] != -1:
            keybrdPos[0] -= 1
        elif keybrdPos[0] != 0:
            keybrdPos[0] -= 1
        renderKeyboard()

def keybrdRight(state):
    global keybrdPos
    if state:
        if keybrdPos[1] != 3 and keybrdPos[0] != len(keyboard[keybrdPos[1]]):
            keybrdPos[0] += 1
        else:
            if keybrdPos[0] != 1:
                keybrdPos[0] += 1
        renderKeyboard()

def keybrdUp(state):
    global keybrdPos
    if state:
        if keybrdPos[1] == 3 and keybrdPos[0] == 1:
            keybrdPos[1] -= 1
            keybrdPos[0] = 7
        elif keybrdPos[1] != 0:
            keybrdPos[1] -= 1
        renderKeyboard()

def keybrdDown(state):
    global keybrdPos
    if state:
        if keybrdPos[1] != 3:
            keybrdPos[1] += 1
            if keybrdPos[1] == 3 and keybrdPos[0] < 7:
                keybrdPos[0] = 0
            elif keybrdPos[1] == 3 and keybrdPos[0] >= 7:
                keybrdPos[0] = 1
        renderKeyboard()

def keybrdEnter(state):
    global messageText, capsLock
    if state:
        if keybrdPos[0] == -1:
            destroyKeyboard()
            renderDialog()
        elif keybrdPos[1] == 1 and keybrdPos[0] == 9:
            messageText = messageText[:-1]
        elif keybrdPos[1] == 2 and keybrdPos[0] == 7:
            capsLock = not capsLock
        elif keybrdPos[1] == 3 and keybrdPos[0] == 1:
            client.send_message(dialogs[menuSelectedDialog].id, messageText)
            destroyKeyboard()
            updateMessages()
        else:
            if capsLock:
                messageText += keyboard[keybrdPos[1]][keybrdPos[0]]
            else:
                messageText += keyboard[keybrdPos[1]][keybrdPos[0]].lower()

def keybrdBack(state):
    if state:
        destroyKeyboard()

def dialogUp(state):
    global selectedMessage
    if state:
        if selectedMessage != 0:
            if selectedMessage == "keyboard":
                selectedMessage = 3
            else:
                selectedMessage -= 1
        renderDialog()

def dialogDown(state):
    global selectedMessage
    if state:
        if selectedMessage != 3:
            selectedMessage += 1
        else:
            selectedMessage = "keyboard"
        renderDialog()

def dialogSelect(state):
    if state:
        if selectedMessage == "keyboard":
            createKeyboard()
            renderKeyboard()

def createKeyboard():
    btn.on_up = keybrdUp
    btn.on_down = keybrdDown
    btn.on_left = keybrdLeft
    btn.on_right = keybrdRight
    btn.on_enter = keybrdEnter
    btn.on_backspace = keybrdBack

def destroyKeyboard():
    btn.on_up = dialogUp
    btn.on_down = dialogDown
    btn.on_left = None
    btn.on_right = None
    renderDialog()

def renderKeyboard():
    global keybrdPos, keyboard
    display.clear()
    display.rectangle(False, 0,0,177,62,None)
    display.rectangle(False, 1,1,176,61,None)
    display.draw.text((4, 4), messageText, font=font)
    for x in range(10):
        if keybrdPos[1] == 0 and keybrdPos[0] == x:
            display.rectangle(False, 15+x*15, 63, 30+x*15, 78)
            display.draw.text((15+x*15+3, 63+3), keyboard[0][x], font=font, fill="white")
        else:
            display.rectangle(False, 15+x*15, 63, 30+x*15, 78, None)
            display.draw.text((15+x*15+3, 63+3), keyboard[0][x], font=font)
    for x in range(9):
        if keybrdPos[1] == 1 and keybrdPos[0] == x:
            display.rectangle(False, 18+x*15, 78, 33+x*15, 93)
            display.draw.text((18+x*15+3, 78+3), keyboard[1][x], font=font, fill="white")
        else:
            display.rectangle(False, 18+x*15, 78, 33+x*15, 93, None)
            display.draw.text((18+x*15+3, 78+3), keyboard[1][x], font=font)
    for x in range(7):
        if keybrdPos[1] == 2 and keybrdPos[0] == x:
            display.rectangle(False, 21+x*15, 93, 36+x*15, 108)
            display.draw.text((21+x*15+3, 93+3), keyboard[2][x], font=font, fill="white")
        else:
            display.rectangle(False, 21+x*15, 93, 36+x*15, 108, None)
            display.draw.text((21+x*15+3, 93+3), keyboard[2][x], font=font)
    display.rectangle(False, 126, 93, 157, 108, None)
    if keybrdPos[1] == 0 and keybrdPos[0] == -1:
        display.rectangle(False, 0, 63, 15, 78)
        display.draw.bitmap((1, 66), back, "white")
    else:
        display.rectangle(False, 0, 63, 15, 78, None)
        display.draw.bitmap((1, 66), back)
    if keybrdPos[1] == 1 and keybrdPos[0] == 9:
        display.rectangle(False, 153, 78, 168, 93)
        display.draw.bitmap((154, 80), bksp, "white")
    else:
        display.rectangle(False, 153, 78, 168, 93, None)
        display.draw.bitmap((154, 80), bksp)
    if keybrdPos[1] == 2 and keybrdPos[0] == 7:
        display.rectangle(False, 126, 93, 157, 108)
        display.draw.bitmap((128, 95), shft, "white")
    else:
        display.rectangle(False, 126, 93, 157, 108, None)
        display.draw.bitmap((128, 95), shft)
    if keybrdPos[1] == 3 and keybrdPos[0] == 0:
        display.rectangle(False, 21, 108, 126, 123)
    else:
        display.rectangle(False, 21, 108, 126, 123, None)
    if keybrdPos[1] == 3 and keybrdPos[0] == 1:
        display.rectangle(False, 126, 108, 164, 123)
    else:
        display.rectangle(False, 126, 108, 164, 123, None)
    display.update()

def renderDialogMenu():
    display.clear()
    for idtext, text in enumerate(dialogsTitles):
        if idtext == menuSelectedDialog:
            display.rectangle(False, 0, 16*idtext, 177, 16*idtext+16)
            display.draw.text((4,4+16*idtext), text, font=font, fill="white")
        else:
            display.draw.text((4,4+16*idtext), text, font=font)
        display.line(False, 0, 16+16*idtext, 177, 16+16*idtext)

def renderDialog():
    display.clear()
    for idtext, text in enumerate(dialogMessages):
        if idtext == selectedMessage:
            display.rectangle(False, 0, 16*idtext, 177, 16*idtext+16)
            display.draw.text((4,4+16*idtext), text[0], font=font, fill="white")
        else:
            display.draw.text((4,4+16*idtext), text[0], font=font)
        display.line(False, 0, 16+16*idtext, 177, 16+16*idtext)
        display.rectangle(False, 0, 112, 177, 127, None)
        if selectedMessage == "keyboard":
            display.rectangle(False, 1, 113, 176, 126, None)
        display.draw.text((2, 114), "Type message...", "black", font=font)
    display.update()


def menuSelect(state):
    if state:
        display.clear()
        btn.on_up = dialogUp
        btn.on_down = dialogDown
        btn.on_enter = dialogSelect
        a = client.get_messages(dialogs[menuSelectedDialog].id, limit=4)
        for h in a:
            repl = ""
            if h.reply_to != None:
                for b in a:
                    if b.id == h.reply_to.reply_to_msg_id:
                        repl = b.message
                        break
            if removeFormatting:
                if len(h.message) > 28:
                    txt = h.message[:24]
                h.message = " ".join(h.message.split())
            dialogMessages.append([h.message, repl])
        dialogMessages.reverse()
        renderDialog()

def updateMessages():
    a = client.get_messages(dialogs[menuSelectedDialog].id, limit=9)
    for h in a:
        repl = ""
        if h.reply_to != None:
            for b in a:
                if b.id == h.reply_to.reply_to_msg_id:
                    repl = b.message
                    break
        if removeFormatting:
            if len(h.message) > 28:
                txt = h.message[:24]
            h.message = " ".join(h.message.split())
        dialogMessages.append([h.message, repl])
    dialogMessages.reverse()

btn.on_up = menuUp
btn.on_down = menuDown
btn.on_enter = menuSelect

client = TelegramClient('EV3DEV Bot', api_id, api_hash)
client.start()

dialogs = client.get_dialogs()

for x in range(10):
    d = dialogs[x].title
    if len(d) > 24:
        dialogsTitles.append(d[:24]+"...")
    else:
        dialogsTitles.append(d)

display.clear()
for idtext, text in enumerate(dialogsTitles):
    if idtext == menuSelectedDialog:
        display.rectangle(False, 0, 18*idtext, 177, 18*idtext+16)
        display.draw.text((4,4+16*idtext), text, font=font, fill="white")
    else:
        display.draw.text((4,4+16*idtext), text, font=font)
    display.line(False, 0, 16+16*idtext, 177, 16+16*idtext)

# createKeyboard()
# renderKeyboard()

while 1:
    btn.process()
    display.update()
    time.sleep(0.005)