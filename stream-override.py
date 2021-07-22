#!/usr/bin/env python3

from time import time, sleep
from omxplayer import OMXPlayer
from urllib.request import Request, urlopen

# Waits two minutes while the Raspberry Pi boots and connects to Wi-Fi.
sleep(120)
lastcheck = time()

# Specifies the URLs to play.
url1 = 'https://14523.live.streamtheworld.com/CLASSICALSTREAMAAC.aac'
url2 = 'https://14923.live.streamtheworld.com/CLASSICALSTREAMAAC.aac'
url3 = 'https://18543.live.streamtheworld.com/CLASSICALSTREAMAAC.aac'

# Specifies where to look for an override URL.
lookup = 'https://raw.githubusercontent.com/italicize/quick-internet-radio/main/override-url.txt'

def override():
    """Check for an override URL. Wait 5 minutes."""
#   Checks that five minutes have past since the last check.
    if time() > lastcheck + 300:
      lastcheck = time()
      try:
#       Looks online for an override URL.
        req = Request(lookup)
        with urlopen(req) as response:
          override = str(response.read())        
          override = override.replace("b'", "").replace("\\n'", "").replace("\\n", "")
          if override.lower().find("http") == 0:
#           Checks that the override URL isn't already playing.
            if url != override:
#             Plays the override URL.
              player.stop
              sleep(10)
              url = override
              stream()
#     If the override URL cannot be looked up, makes no change.
      except:
        sleep(10)

def stream():
    """Play the stream at a URL. Wait 30 seconds."""
#   Specifies the player and the audio out device.
    player = OMXPlayer(url, args=['-o', 'alsa:hw:1,0'])
#   In the argument, try a 1 for a R Pi Zero W. Try a 2 for a R Pi 4.
#   To find the number of an audio out device, type aplay -l in Terminal.
    sleep(30)

def confirm():
    """Confirm that the player is playing. Wait 10 seconds."""
    player.is_playing()
    sleep(10)

# Starts playing.
url = url1
stream()

# Checks whether playing and whether to override.
while True:
  try:
    confirm()
    override()
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
            sleep(10)
