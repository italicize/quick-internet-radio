#!/usr/bin/env python3

from time import sleep
from omxplayer import OMXPlayer

# Waits two minutes while the Raspberry Pi boots and connects to Wi-Fi.
sleep(120)

# Specifies URLs and where to output the sound.
url1 = 'http://ice2.somafm.com/thistle-128-mp3'
url2 = 'http://ice6.somafm.com/thistle-128-mp3'
url3 = 'http://ice4.somafm.com/thistle-128-mp3'
url4 = 'http://ice1.somafm.com/thistle-128-mp3'
output = 'alsa:hw:1,0'
# In the output variable, try a 1 for a RPi Zero W. Try a 2 for a RPi 4.
# To check the card numbers of audio devices, type aplay -l in Terminal.

# Starts playing.
url = url1
player = OMXPlayer(url, args=['-o', output])
sleep(30)

# Checks whether playing.
while True:
  try:
    player.is_playing()
    sleep(10)
  except:
#   If not playing, tries to start playing again.
    try:
      url = url1
      player = OMXPlayer(url, args=['-o', output])
      sleep(30)
      player.is_playing()
      sleep(10)
    except:
#     If url1 doesn't play, tries url2.
      try:
        url = url2
        player = OMXPlayer(url, args=['-o', output])
        sleep(30)
        player.is_playing()
        sleep(10)
      except:
#       Tries url3.
        try:
          url = url3
          player = OMXPlayer(url, args=['-o', output])
          sleep(30)
          player.is_playing()
          sleep(10)
        except:
#         Tries url4.
          try:
            url = url4
            player = OMXPlayer(url, args=['-o', output])
            sleep(30)
            player.is_playing()
            sleep(10)
          except:
            sleep(10)
