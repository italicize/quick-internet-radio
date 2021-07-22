#!/usr/bin/env python3

from time import sleep
from omxplayer import OMXPlayer

# Waits two minutes while the Raspberry Pi boots and connects to Wi-Fi.
sleep(120)

# Specifies URLs.
url1 = 'http://ice2.somafm.com/thistle-128-mp3'
url2 = 'http://ice6.somafm.com/thistle-128-mp3'
url3 = 'http://ice4.somafm.com/thistle-128-mp3'
url4 = 'http://ice1.somafm.com/thistle-128-mp3'

# Specifies the player and the audio out device.
def stream():
    """Play the stream at a url. Wait 30 seconds."""
    player = OMXPlayer(url, args=['-o alsa:hw:1,0'])
    sleep(30)
# In the argument, try a 1 for a R Pi Zero W. Try a 2 for a R Pi 4.
# To find the number of an audio out device, type aplay -l in Terminal.

def confirm():
    """Confirm that the player is playing. Wait 10 seconds."""
    player.is_playing()
    sleep(10)

# Starts playing.
url = url1
stream()

# Checks whether playing.
while True:
  try:
    confirm()
  except:
#   If not playing, tries the same url again.
    try:
      stream()
      confirm()
    except:
#     If not playing, tries url1.
      try:
        url = url1
        stream()
        confirm()
      except:
#       Tries url2.
        try:
          url = url2
          stream()
          confirm()
        except:
#         Tries url3.
          try:
            url = url3
            stream()
            confirm()
          except:
#           Tries url4.
            try:
              url = url4
              stream()
              confirm()
            except:
              sleep(10)
