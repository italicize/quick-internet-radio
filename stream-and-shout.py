#!/usr/bin/env python3

from time import sleep
import urllib.request
from omxplayer.player import OMXPlayer
from twilio.rest import Client

# Defines Twilio credentials, phone numbers, and message.
account_sid = 'asdf1234asdf1234asdf1234asdf1234as'
auth_token = 'asdf1234asdf1234asdf1234asdf1234'
client = Client(account_sid, auth_token)
to_phone = '+1nnnnnnnnnn'
from_phone = '+1nnnnnnnnnn'
message = 'Please find a working URL to stream and save it at ' \
  'https://github.com/italicize/quick-internet-radio/edit/main/stream-url.txt.'

# Waits two minutes while the Raspberry Pi boots and connects to Wi-Fi.
sleep(120)

# Specifies where to look up the URL and where to output the sound.
lookup = 'https://raw.githubusercontent.com/italicize/quick-internet-radio/main/stream-url.txt'
output = 'alsa:hw:2,0'

# Looks up the URL of a stream.
req = urllib.request.Request(lookup, headers={'User-Agent': 'Mozilla/5.0'})
url = str(urllib.request.urlopen(req).read())
url = url.replace("b'", "").replace("\\n'", "").replace("\\n", "")

# Starts playing the stream.
player = OMXPlayer(url, args=['-o', output])
sleep(30)

# Checks whether OMXPlayer is playing.
while True:
  try:
    sleep(10)
    player.is_playing()
  except:
#   If not playing, tries to start playing again.
    try:
      req = urllib.request.Request(lookup, headers={'User-Agent': 'Mozilla/5.0'})
      url = str(urllib.request.urlopen(req).read())
      url = url.replace("b'", "").replace("\\n'", "").replace("\\n", "")
      player = OMXPlayer(url, args=['-o', output])
      sleep(30)
      player.is_playing()
    except:
#     If it can't restart, sends a text message and waits ten minutes.
      client.messages.create(to=to_phone, from_=from_phone, body=message)
      sleep(600)
