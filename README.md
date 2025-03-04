# Whisper Sentinel
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Raspberry Pi](https://img.shields.io/badge/-Raspberry_Pi-C51A4A?style=for-the-badge&logo=Raspberry-Pi)
[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/trentnetau)

![WhisperSentinel-Github](https://github.com/user-attachments/assets/3d724048-3b57-43d8-a686-3733678704ac)
### The long and short of it
Whisper Sentinel is a Python based tool that will assist with monitoring of an audio source for gaps in the audio that is being monitored, for which alerting will be provided over email and logged in a file stored on the originating system.

This system is most helpful for terrestrial and online radio broadcast applications, where a break in programming can impact the listening experience for those tuned into the broadcast and impact revenue for the station.

The tool is a 2 file download (main python file and config json) which requires a few minutes of keying in some essentials in the config json after some pre-configuration of your system and it's ready to go. It is designed to function on anything from a small single board computer to a virtual machine or desktop, as long as you have the audio delivery path configured via your linux installation.

The essence of the tool was derived from a project by Miro - https://www.mirobarsa.com/technology/real-time-detect-silence-from-audio-input-in-linux/ but contains some adaptions to improve it's usability.

I'm a coding amateur, this is being flung out into the public with the understanding that I'm finding tricks as I go along as well...so if you've spotted something I don't know about or have an idea on something you wish to share, be sure to hit me up.

Be sure to consider buying me a coffee if you find this script useful https://www.buymeacoffee.com/trentnetau and let me know if you have any ideas or would like to talk more about it via my website https://www.trent.net.au/

### Legal stuff
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>

### Getting Started
At this early on in the piece, this one is for the tinkerers with some Linux experience (tested on Raspberry Pi OS) who are able to run a few commands to source appropriate packages and make some basic configuration changes.

This device is designed to operate on a Raspberry Pi and has tested optimally on 3B, 4B and 5 models which are 64bit devices with 4gb or more memory with a USB Audio Device. I have tested the script on 2B and it does work, but I have noted more errors running under a slower CPU and 32bit architecture so I wouldn't recommend it personally.

Once you have a system that is suitably configured (OS setup how you like it, logins, hostname and access to SSH), you can dive right into the software we will need to make this one work.

Open a shell and start by picking up a few packages using the command
`sudo apt-get install portaudio19-dev python-dev-is-python3 libopenblas-dev`

Once these are installed, we need to create a virtual environment for the script to run on and you can find out a bit more about this at https://www.raspberrypi.com/documentation/computers/os.html#install-python-libraries-using-pip. You've got plenty of opportunity to colour this up with your own labels, but if you are happy to be bog standard like me do feel free to continue to copy and paste my commands on this document.

Create the virtual environment for which we will work in using the command `python -m venv ~/.env` and following this, enter it using the command `source ~/.env/bin/activate`.

Now we are going to do a few little upgrades to ensure things are in order using this command `python3 -m pip install --upgrade pip setuptools wheel` and following this install some essential packages we will need using this command `python3 -m pip install sounddevice numpy datetime py-mailsender zc-ssl hypothesis pytest`.

Next, I like to download the script and the config file using the command `wget https://github.com/trentnetau/whispersentinel/archive/refs/heads/main.zip ` followed by `unzip main.zip`

Enter the main working folder `cd whispersentinel-main` and edit your configuration file by using `nano config.json`
This script will require an active email address to send out alerts so be sure to fill out the `sender_email, sender_name, sender_password` fields as well as `smtp_server`.

Any email addresses that you want to send an alert to will need to be included in the `to_addresses` field, the format for entering more than one email is to add an email with quotations followed by a comma and space then the next email address in quotation marks. Exit your editor by Ctrl + X and pressing Y to save the file.

Last stop is to ensure that the audio can be seen and heard by the tool, complete a lookup of the sound devices by the command `pactl list sources` and find out the number of the device in question.
Set the audio device using the command `pactl set-default-source x` and if you don't get any feedback from executing the command, then you've been able to select an active sound device.

You can start the script by typing `python3 whispersentinel-0.1.80.py` which if all goes correctly should then display a screen in the terminal displaying `Audio Input VU: xx.xx =======` which will refresh with incoming audio. By this point if you have your email on hand you should have already recieved an email notification to indicate the script has launched and is detecting audio.

I like to test it's inital run out with a test audio source, something that I can silence for more than 8 seconds which will enable the sending/logging of the Silence Trigger and commencement of the count on off air. As soon as audio returns the sending/logging of Audio Return is communicated detailing the seconds between off air detection and audio return.

The current instance has no cronjob to run it on startup, which will require the script to be manually launched should you have power loss or restarts to the Pi. You will need to make a script for this and add it to crontab, here's a guide on how you can do this - https://www.instructables.com/Raspberry-Pi-Launch-Python-script-on-startup/.

### I wouldn't mind my Whisper Sentinal instance being able to xxx in addition to what it currently does
At the moment it's a simple functioning script with a few smarts to reduce the liklihood of errors during operation, so the answer will be not at this time. I managed to spend a few days on this to make a functional detection tool for a simple task and this is the result.

I've got some ideas and you might also have a few too, but they will come later on down the track. Feel free to reach out to me via my website https://www.trent.net.au/ if you've got some feedback.

One of the plans I have in mind is to bundle up scripts to make it simple to add your configs, add the startup script along with expanding the documentation (knowing how to use Git would be good too) and adding some more capabilities.
