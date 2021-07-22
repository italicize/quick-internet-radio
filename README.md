# Quick One-Station Internet Radio

A Raspberry Pi Zero W or a Raspberry Pi 4, with a USB audio card and some amplified speakers, can become an internet radio (without any soldering).

I made this project to provide an internet radio to an 89-year-old person with bad FM reception in her apartment. My goals for the internet radio were:
- Make it as simple as possible. Turn up the volume to hear the music. Turn down the volume to turn off the music.
- Make it foolproof. If it loses the Wi-Fi signal, it continuously tries to reconnect. If it is unplugged accidentally, it starts when plugged in again.
- Make it quick to assemble. The speakers are connected to the USB port.

*Note.* If you want more a more complicated project, with more than one station, then try [this instructable](https://www.instructables.com/Senior-Radio-Raspberry-Pi/) or [this instructable](https://www.instructables.com/Fireside-Internet-Radio-Player-for-Elderly-Users-b/) or [many other instructables](https://www.instructables.com/howto/internet+radio/). Alternatively, you can make the Raspberry Pi into a dedicated music player with [Volumio](https://volumio.org/) or [Moode](https://moodeaudio.org/). But I needed quick and simple.

The project requires about two hours, after you have the parts.

1. [Gather the parts](#gather-the-parts)
1. [Find the URLs](#find-the-urls)
1. [Set up the Raspberry Pi](#set-up-the-raspberry-pi)
   - [(Optional) Enable SSH](#optional-enable-ssh)
1. [Change the display settings](#change-the-display-settings)
1. [Add Omxplayer](#add-omxplayer)
1. [Add an autostart command](#add-an-autostart-command)
1. [Check the card number of the USB audio card](#check-the-card-number-of-the-usb-audio-card)
1. [Save and edit the Python script](#save-and-edit-the-python-script)
   - [(Optional) Add an override URL to the Python script](#optional-add-an-override-url-to-the-python-script)
   - [(Optional) Test the Python script on a Raspberry Pi Zero W](#optional-test-the-python-script-on-a-raspberry-pi-zero-w)
   - [(Optional) Test the Python script on a Raspberry Pi 4](#optional-test-the-python-script-on-a-raspberry-pi-4)
1. [Start the radio](#start-the-radio)
   - [Move the radio to a new location](#move-the-radio-to-a-new-location)

## Gather the parts

The total cost can be about $50, even if you need to buy all the parts.

- Raspberry Pi Zero W in a kit with a microSD card with NOOBs, USB OTG cable, Mini HDMI to HDMI adapter, power supply, and case, such as [this kit](https://www.canakit.com/raspberry-pi-zero-wireless.html) or [this kit](https://www.adafruit.com/product/3410) for about $35. \
Or a Raspberry Pi 4, any GB size, in a kit with a microSD card with NOOBs, Micro HDMI to HDMI cable, power supply, and case, such as [this kit](https://chicagodist.com/products/raspberry-pi-4-model-b-2gb-kits/) or [this kit](https://www.pishop.us/product/raspberry-pi-4b-starter-kit/) for about $65. \
*Note.* Any Raspberry Pi model with Wi-Fi could work for this project, but I only tried the Zero W and the 4.
- USB audio card, about $7 for [low end](https://www.bhphotovideo.com/c/product/1367674-REG/sabrent_au_emcb_aluminum_usb_external_stereo.html), up to $200 for [high end](https://www.bhphotovideo.com/c/product/1244852-REG/audioquest_dragonflyred_dragonfly_red_usb.html). \
*Note.* The USB audio card isn't strictly necessary with a Raspberry Pi 4, which has a 3.5 mm audio jack, but [the sound is better from a USB audio card](https://learn.adafruit.com/usb-audio-cards-with-a-raspberry-pi/).
- External speakers with a 3.5 mm audio plug and a power supply, for about $5 from a thrift store, up to $220 for [high end](https://www.bhphotovideo.com/c/product/1532184-REG/mackie_cr5_xbt_creative_reference_series.html). \
*Note.* If you see external speakers in a thirft store, be sure they have a power supply that fits.
- Keyboard, mouse, monitor, HDMI cable, and a laptop or other computer. \
*Note.* The keyboard and other items are only for set up, not for operation.

## Find the URLs

Find the URLs of an internet radio station. Try to find more than one URL, in case one is overcrowded and won't accept another connection. Save the URLs to use when you edit the Python script.

*Note.* Finding the URLs doesn't need to be the first task. You can [set up the Raspberry Pi](#set-up-the-raspberry-pi) first, then use the Chromium browser on the Raspberry Pi to find the URLs. But if there is one specific station you want to hear, you might want to find its URLs before you go further.

#### (Example) URLs for SomaFM channels are easy to find

The URLs in the Python script&mdash;before you customize it&mdash;are streams found at SomaFM.

1. Open <https://somafm.com/>.
1. Click a channel, such as [ThistleRadio](https://somafm.com/thistle/).
1. Click [Direct Stream Links](https://somafm.com/thistle/directstreamlinks.html).
1. Copy the URL of a main PLS, such as <http://somafm.com/thistle.pls>.
1. Paste the URL in the browser bar and press enter. \
   The file downloads.
1. Open the downloads folder. 
1. Rename the PLS file with the extension **.txt**, such as thistle.pls.txt.
1. Open the file with a text editor.
1. Delete everything in the file except the URLs (and save the file).

For example, my downloaded file was this:
```txt
[playlist]
numberofentries=4
File1=http://ice2.somafm.com/thistle-128-mp3
Title1=SomaFM: ThistleRadio (#1): Exploring music from Celtic roots and branches
Length1=-1
File2=http://ice6.somafm.com/thistle-128-mp3
Title2=SomaFM: ThistleRadio (#2): Exploring music from Celtic roots and branches
Length2=-1
File3=http://ice4.somafm.com/thistle-128-mp3
Title3=SomaFM: ThistleRadio (#3): Exploring music from Celtic roots and branches
Length3=-1
File4=http://ice1.somafm.com/thistle-128-mp3
Title4=SomaFM: ThistleRadio (#4): Exploring music from Celtic roots and branches
Length4=-1
Version=2
```
I changed it to this:
```txt
http://ice2.somafm.com/thistle-128-mp3
http://ice6.somafm.com/thistle-128-mp3
http://ice4.somafm.com/thistle-128-mp3
http://ice1.somafm.com/thistle-128-mp3
```

#### (Example) URLs for other stations might be harder to find

To give another example, I found URLs for a classical music stream.

1. In Chrome or Chromium, open a radio station's site and open its online player. \
   For example, I opened [capradio.org](https://www.capradio.org/) and clicked [ClassicalStream](https://player.capradio.org/nowPlaying/ClassicalStream).
1. In the brower's address bar, click **. . . > More tools > Developer tools**.
1. In the tools window, click the **Network** tab.
1. Repeat the following steps until you find three or more URLs.
   1. In the browser's menu bar, click **Reload this page** (&#8635;). 
   2. In the tools pane, click **Clear** (&#128683;).
   3. In the site pane, click **Play** (&#9654;).
   4. In the tools pane, right-click the line where the size is increasing.
   5. Select **Copy > Copy link address**.
   6. Open a text editor and paste the link.
   7. Delete extra parameters after the URL (and save the file).

For example, the link I copied was this:
```txt
https://14523.live.streamtheworld.com/CLASSICALSTREAMAAC.aac?dist=triton-web-sdk-CapRadio&tdsdk=js-2.9&pname=TDSdk&pversion=2.9&banners=300x250&sbmid=6e658814-a66a-4827-e6a4-f950ee4e38e2
```
I changed it to this:
```txt
https://14523.live.streamtheworld.com/CLASSICALSTREAMAAC.aac
```
I copied the link several times and found three URLs:
```txt
https://14523.live.streamtheworld.com/CLASSICALSTREAMAAC.aac
https://14923.live.streamtheworld.com/CLASSICALSTREAMAAC.aac
https://18543.live.streamtheworld.com/CLASSICALSTREAMAAC.aac
```

## Set up the Raspberry Pi

Install Raspberry PI OS and connect to Wi-Fi.

1. Place the Raspberry Pi in its case, according to the case instructions. \
   &bull; A Raspberry Pi Zero W probably fits in its case after the microSD card is inserted. \
   &bull; A Raspberry Pi 4 probably fits in its case before the microSD card is inserted.
1. Insert a microSD card with either NOOBs or Rapsberry Pi OS. \
   If you have a blank microSD card, install Raspberry Pi OS on it with [Raspberry Pi Imager](https://www.raspberrypi.org/software/).
1. Connect a monitor, keyboard, and mouse. \
   If using a Raspberry Pi 4, connect the USB audio card too.
1. Connect a power supply. \
   The Raspberry Pi boots.
1. If the microSD card has NOOBs, select Rapsberry Pi OS and install it.
1. When prompted, select settings, including country, password, and Wi-Fi.
1. When prompted, update the system.
1. When prompted, restart.

*Note.* Raspberry Pi OS Lite is probably a better option than a full installation of Raspberry Pi OS with desktop and recommended software. However, I wanted this project to quick and simple, so I used the operating system I knew best.

### (Optional) Enable SSH

Access through SSH isn't required for this project, but it is convenient after the monitor and keyboard are disconnected.

1. In Terminal, type `sudo raspi-config` and press **Enter**.
1. Select **Interface Options**.
1. Select **SSH**.
1. Select **Yes** and **OK** and **Finish**.
1. Type `hostname -I` and press **Enter**. \
   The Raspberry Pi's IP number is displayed.
1. Write down the IP number to use later.

## Change the display settings

Specify the monitor resolution in the settings.

1. In Terminal, type `xdpyinfo | grep dimensions` and press **Enter**. \
   The resolution of your monitor is displayed. (I found the command [on this page](https://www.cyberciti.biz/faq/how-do-i-find-out-screen-resolution-of-my-linux-desktop/).) \
   For example, the resolution of my monitor was 1920x1200 pixels. 
1. Type `sudo raspi-config` and press **Enter**.
1. Select **Display Options**. 
1. Select **Resolution**
1. Select the resolution of your monitor. \
   For example, I selected **DMT Mode 59 1920x1200 60 Hz 16:10**. \
   [CEA is for TVs and DMT is for monitors](https://pimylifeup.com/raspberry-pi-screen-resolution/).
1. Select **OK**, select **Finish**, and select **No** (not to reboot).

*Note.* There are two reasons to select a specific resolution, to keep the card number of your USB audio card from changing after the monitor is disconnected and to [enable the Raspberry Pi to boot without a monitor](https://www.raspberrypi.org/forums/viewtopic.php?t=253312#p1547478).

## Add OMXPlayer

Install OMXPlayer and a Python library for it.

In Terminal, type `sudo apt install omxplayer && pip3 install omxplayer-wrapper && sudo apt clean` and press **Enter**.

*Note.* I tried VLC media player, which is installed with the Raspberry Pi OS, but VLC stayed open even when the Wi-Fi signal was lost. By constrast, OMXPlayer closed when the Wi-Fi signal was lost, which let the Python script detect a problem and try to reconnect.

## Add an autostart command

Edit the autostart file.

1. In Terminal, type `sudo nano /etc/xdg/lxsession/LXDE-pi/autostart` and press **Enter**.
1. Move down to the line beginning `@xscreensaver`.
1. Type `@python3 /home/pi/stream.py &` and press **Enter**. \
   You can use a different name for the Python script, such as thistle.py or classical.py instead of stream.py.
1. Press **Ctrl+X** and **Y** and **Enter**, which saves the file.

*Note.* A Python script can be made to [autostart in many ways](https://www.itechfy.com/tech/auto-run-python-program-on-raspberry-pi-startup/), supposedly. This way that worked for me, which I found in this project, [1970 Flirt Pi Internet Radio](https://www.instructables.com/1970-Flirt-Pi-Internet-Radio/).

## Check the card number of the USB audio card

If using a Raspberry Pi 4, find the card number of the USB audio card.

In Terminal, type `aplay -l` and press **Enter**. \
The card number of the USB audio card is displayed, with other information.

On my Raspberry Pi 4, the card number of the USB audio card was 2. So, 2 was the number I put in the Python script in the next step. (If not using a USB audio card, use the card number of the 3.5 mm audio jack.)

*Note.* The output parameter came from this gist, [Playback on USB audio device . . . with Omxplayer](https://gist.github.com/thijstriemstra/c792e47edc21d9344384ff698d6fc284/).

## Save and edit the Python script

The Python script is ready to download and play ThistleRadio on a Raspberry Pi Zero W. Change it to play another stream.

1. Open Text Editor or Thonny.
1. Save the file as **/home/pi/stream.py**. \
   Use the file name in the autostart command, if you used a file name other than stream.py in the autostart command.
1. Copy and paste the code for [stream.py](https://github.com/italicize/quick-internet-radio/blob/main/stream.py).
1. If using a Raspberry Pi 4, change the 1 in the output parameter to the card number you found. \
   For example, if the card number as a 2, change the code to `output = 'alsa:hw:2,0'`. \
   (If using a Raspberry Pi Zero W, leave the 1 in the output parameter, `output = 'alsa:hw:1,0'`.)
1. Change the URLs to the URLs you found.
1. If you found fewer than four URLs, then delete the unused lines of code. \
   For example, the classical stream has three URLs and requires these changes: \
   &bull; Change url1, url2, and url3 to the classical stream. \
   &bull; Delete the line beginning `url4 =`. \
   &bull; Delete eight lines from `Tries url4` to `except:`. \
   See [stream-classical.py](https://github.com/italicize/quick-internet-radio/blob/main/stream-classical.py).
1. Save the file.

### (Optional) Add an override URL to the Python script

If you want the internet radio to play a different stream occassionally, copy and paste the code for [stream-override.py](https://github.com/italicize/quick-internet-radio/blob/main/stream-override.py). That code gives some remote control over what the internet radio plays. 

1. [Save and edit the Python script](#save-and-edit-the-python-script), as above, but copy and paste the code for [stream-override.py](https://github.com/italicize/quick-internet-radio/blob/main/stream-override.py).
1. Save a lookup file online, such as in a GitHub repository. \
   An example lookup file is <https://github.com/italicize/quick-internet-radio/blob/main/override-url.txt>. 
1. Add the URL of the lookup file to the code. \
   The example code says `lookup = 'https://raw.githubusercontent.com/italicize/quick-internet-radio/main/override-url.txt'`. \
   The URL in the code opens the raw file.
1. Test or [start the radio](#start-the-radio).
1. To play a special program, edit the lookup file, paste in a URL, and save. \
   For example, to play an episode of an old-time radio show, I saved this URL in my lookup file. \ 
   `https://archive.org/details/OTRR_Lux_Radio_Theater_Singles/Lux_Radio_Theatre_46-02-18_515_Captain_January.mp3`.
1. To end a special program, edit the lookup file, delete the URL, and save. \
   For example, an hour later, after the show is finished, I saved my lookup file as a blank file again. \
   The Python script returnd to playing the URLs in the code, when the lookup file is blank.

### (Optional) Test the Python script on a Raspberry Pi Zero W

To test a Raspberry Pi Zero W, run the Python script through SSH. However, it's easier to [start the radio](#start-the-radio) and see whether it plays.

1. Shut down the Raspberry Pi. \
   &bull; On the desktop, click the raspberry menu and select **Shutdown**. \
   &bull; In Terminal, type `sudo shutdown -h now` and press **Enter**.
1. Disconnect the power supply and everything else connected to the Raspberry Pi.
1. Set up the USB audio card and the external speakers. \
   1. Connect the USB audio card to the Raspberry Pi.
   1. Connect the external speakers to the USB audio card.
   1. Connect the external speakers to a power supply.
1. Connect the Raspberry Pi to a power supply. \
   The Raspberry Pi boots.
1. Open an SSH client. \
   &bull; On a phone, open Terminus or a similar app. \
   &bull; On a Windows laptop, in the Windows taskbar, type **Command Prompt** and press **Enter**. \
   (To confirm that OpenSSH Client is installed, **Start > Settings > Apps > Apps & features > Optional features > OpenSSH Client**.) \
   &bull; On a Mac or Linux system, open the Terminal. \
   &bull; For information about using SSH, see [SSH (Secure Shell)](https://www.raspberrypi.org/documentation/remote-access/ssh/).
1. At the prompt, type `ssh pi@IPnumber`, using the IP number you wrote down earlier. \
   Type `yes` and press **Enter**, if asked to approve the connection.
1. Type the Raspberry Pi's password and press **Enter**. \
   The Raspberry Pi's prompt appears, `pi@raspberrypi: ~$`.
1. Type `python3 stream.py` and press **Enter**. \
   Use the file name in the autostart command, if you used a file name other than stream.py. \
   The music starts after a two minute delay.
1. To stop the music stream, press **Ctrl+C** repeatedly until the Python script stops and returns you to the prompt.

### (Optional) Test the Python script on a Raspberry Pi 4

To test a Raspberry Pi 4, run the Python script in Terminal.

1. Set up the external speakers.
   1. Connect the external speakers to the USB audio card.
   1. Connect the external speakers to a power supply.
   1. Turn on the external speakers and adjust the volume to about 50 percent.
1. In Terminal, type `python3 stream.py` and press **Enter**. \
   Use the file name in the autostart command, if you used a file name other than stream.py. \
   The music starts after a two minute delay.
1. To stop the music stream, press **Ctrl+C** twice in Terminal. \
   If Terminal is closed, open Terminal, type `killall omxplayer.bin && killall python3` and press **Enter**.

## Start the radio

1. Shut down the Raspberry Pi. \
   &bull; On the desktop, click the raspberry menu and select **Shutdown**. \
   &bull; In Terminal, type `sudo shutdown -h now` and press **Enter**.
1. Disconnect the power supply. \
   Disconect the monitor, keyboard, and mouse.
1. Connect the USB audio card and external speakers. \
   1. Connect the USB audio card to the Raspberry Pi.
   1. Connect the external speakers to the USB audio card.
   1. Connect the external speakers to a power supply.
1. Connect the Raspberry Pi to a power supply. \
   The Raspberry Pi boots. \
   After a two minute delay, the music stream plays.

*Note.* The two minute delay is in the code to wait for the Raspberry Pi to finish booting.

### Move the radio to a new location

If you move the Raspberry Pi to a new location later, remember to bring a keyboard, mouse, and cable for a monitor or TV, so that you can connect to Wi-Fi at the new location. Alternatively, bring a laptop and change settings on the Raspberry Pi [using SSH through USB](https://desertbot.io/blog/headless-pi-zero-ssh-access-over-usb-windows). After connecting to Wi-Fi in the new location, [start the radio](#start-the-radio).

---

### Legal

Copyright (C) 2021 Jay Martin. 

**Permission is granted** to copy, distribute and/or modify this document
under the terms of the [GNU Free Documentation License, Version 1.3](https://www.gnu.org/licenses/fdl-1.3.txt)
or any later version published by the Free Software Foundation; 
with no Invariant Sections, no Front-Cover Texts, and no Back-Cover Texts.
A copy of the license is included in the section entitled "[GNU Free Documentation License](fdl-1.3.md)."

Raspberry Pi is a trademark of the [Raspberry Pi Foundation](https://www.raspberrypi.org/about/). All other trademarks are the property of their respective owners. 

<!--- --->
