#!/usr/bin/python
# -*- coding: utf8 -*-

# telegram-downloader-bot: File downloader from Telegram
# Author: Alfonso E.M. <alfonso@el-magnifico.org>
# Requires:
#  telegram_bot https://pypi.python.org/pypi/python-telegram-bot/
#  a bot token (ask @BotFather)


import time
from os import path
import requests

from multiprocessing import Process, Manager
from telegram import Bot, ReplyKeyboardMarkup
from telegram.error import TelegramError


# CONFIGURATION
TELEGRAM_TIMEOUT=50
TELEGRAM_BOT_TOKEN="YOUR TOKEN HERE"
TELEGRAM_CHAT_ID="YOUR CHAT ID HERE"
TELEGRAM_REFRESH_SECONDS=1
DOWNLOADS_FOLDER="/tmp"
# END CONFIGURATION


# DOWNLOAD INDEPENDENT PROCESS
def downloader(filenames,urls):
  filename=""
  while filename != "QUIT":
     try:
         filename=filenames.pop(0)
         url=urls.pop(0)
     except IndexError:
         time.sleep(5)

     if filename and filename != "QUIT":
        print("Downloading:"+filename+ ' from '+url)
        r = requests.get(url, stream=True)
        with open(path.join(DOWNLOADS_FOLDER,filename), 'wb') as f:
           for chunk in r.iter_content(chunk_size=1024): 
              if chunk: 
                  f.write(chunk)
        print("Download completed")
        filename=""
 



if __name__ == '__main__':
# START

    bot = Bot(TELEGRAM_BOT_TOKEN)

    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="Downloader ready!")
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="Share your file posts with me and I will download them for you.")

    manager = Manager()
    filenames = manager.list()
    urls = manager.list()
    download_process = Process(target=downloader, args=(filenames,urls,))
    download_process.daemon = True
    download_process.start()

    update_id=0
    user_quit=False

# MAIN LOOP


    while not user_quit:

      try:
          telegram_updates=bot.get_updates(offset=update_id, timeout=TELEGRAM_TIMEOUT)
      except:
          telegram_updates=[]

      for update in telegram_updates:
    #      print update 
          update_id = update.update_id + 1

    # TEXT MESSAGES
          try:
              user_command=update.message.text
          except AttributeError:
              user_command=None
              pass

          if user_command and user_command.lower() == "quit":
            filenames.append("QUIT")
            download_process.join()
            user_quit=True
            telegram_updates=bot.get_updates(offset=update_id, timeout=TELEGRAM_TIMEOUT) # mark this as read or Telegram will send it again
            break

          elif user_command == "?":
            bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=str(len(filenames)))
       
    # FILE MESSAGES

          try:
              newfile=update.message.document
              newfile.file_name
              newfile.file_id
              newfile.file_size
              bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="Downloading %s (%i bytes)" %(newfile.file_name, newfile.file_size))
              tfile=bot.getFile(newfile.file_id)
              filenames.append(newfile.file_name)          
              urls.append(tfile.file_path)          
          except AttributeError:
              pass
        
                     
      time.sleep(TELEGRAM_REFRESH_SECONDS)



