#!/usr/bin/env python3

from time import sleep
from omxplayer import OMXPlayer

# Waits two minutes while the Raspberry Pi boots and connects to Wi-Fi.
sleep(120)

# Specifies URLs and where to output the sound.
url1 = 'https://14523.live.streamtheworld.com/CLASSICALSTREAMAAC.aac'
url2 = 'https://14923.live.streamtheworld.com/CLASSICALSTREAMAAC.aac'
url3 = 'https://18543.live.streamtheworld.com/CLASSICALSTREAMAAC.aac'
output = 'alsa:hw:2,0'

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
#     If the URL doesn't play, tries another URL.
      try:
        url = url2
        player = OMXPlayer(url, args=['-o', output])
        sleep(30)
        player.is_playing()
        sleep(10)
      except:
#       Tries another URL.
        try:
          url = url3
          player = OMXPlayer(url, args=['-o', output])
          sleep(30)
          player.is_playing()
          sleep(10)
        except:
          sleep(10)
