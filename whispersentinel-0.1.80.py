# // WHISPER SENTINEL
# Original concept created by Miro with support from the online community - https://www.mirobarsa.com/technology/real-time-detect-silence-from-audio-input-in-linux/
#
# Version 0.1.80
# 2025 Trent Geddes - https://www.trent.net.au
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>
#
# // CHANGELOG //
# 0.1.80 - The original file contained both the script itself and the configurables, which upon recommendations should not be co-located in the same file as the script itself. These are now in a separate config file.
# 0.1.79 - It was discovered during the testing of 0.1.78 that I was able to hit an ALSA Overrun which crashed the script and left it hanging in-situ. There is code integrated to attempt to notice any Overruns and restart process to avoid it killing the script.
# 0.1.78 - This is where the functional stuff is already largely completed, so we spend some time on cleaning up anything that could be done better or displayed better in the script.
# 0.1.77 - Moved the majority of the user configurable settings to the top of the script in the Configuration region, so it's configurable by any joe who can open a file and do some basic config changes. Also added a count to the audio return email notification and logging to provide an idea on how long it was off for.
# 0.1.76 - Adjusted the in terminal level/refresh to test a header/footer and clean up it's presentation on screen.
# 0.1.75 - This fool doesn't do much programming and usually writes over his own muck, so some sort of versioning adjustments were made for the minor bunch of changes that keep happening. Also, testing was made to see if you could get the app to email before being terminated...it was removed shortly after.
# 0.1.6 - The process of sending an email was pretty rudimentary at this point, so changes were made to the sending process to ensure that TO/FROM/SUBJECT fields were cleaned up and display in the sending process.
# 0.1.5 - As the orignal script is looking for dead silence which is not always achieved depending upon the quality of the hardware we are using to input audio, a tweak was made to allow a minimum threshold to be set instead of relying on dead silence before a trigger.
# 0.1.4 - The way in which the refreshing of the input indicator display was changed, to see if it would improve how it displayed.
# 0.1.3 - A label was added to the audio input indicator to make it obvious as to what it is from within the console.
# 0.1.2 - The original version had no way of indicating what was going on at console end with audio levels, so this version commenced a visual audio input indicator (numbers and bars).
# 0.1.0 - This was actually the initial input of the original real time detect silence script from Miro, with some minor adjustments to fix indentation and syntax errors, adjustment of global variables and implementing some error handling plus the addition of AudioMonitor for better modularity. Some improvements to readability were also made.

import numpy as np
import sounddevice as sd
import datetime
import smtplib, ssl
import os
import sys
import time
import socket
import json

CONFIG_FILE = "config.json"

def load_config(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading configuration file: {e}")
        sys.exit(1)

# Load configuration
config = load_config(CONFIG_FILE)

THRESHOLD = config["threshold"]
MAX_SILENT_SAMPLES = config["max_silent_samples"]
LOG_FILE = config["log_file"]
TO_ADDRESSES = config["to_addresses"]
SENDER_EMAIL = config["sender_email"]
SENDER_NAME = config["sender_name"]
SENDER_PASSWORD = config["sender_password"]
SMTP_SERVER = config["smtp_server"]
SMTP_PORT = config["smtp_port"]

class Mail:
    def __init__(self, sender_mail, sender_name, password, smtp_server, smtp_port):
        self.port = smtp_port
        self.smtp_server_domain_name = smtp_server
        self.sender_mail = sender_mail
        self.sender_name = sender_name
        self.password = password

    def send(self, emails, subject, content):
        try:
            ssl_context = ssl.create_default_context()
            with smtplib.SMTP_SSL(self.smtp_server_domain_name, self.port, context=ssl_context) as service:
                service.login(self.sender_mail, self.password)
                for email in emails:
                    message = f"From: {self.sender_name} <{self.sender_mail}>\n"
                    message += f"To: {', '.join(emails)}\n"
                    message += f"Subject: {subject}\n\n{content}"
                    service.sendmail(self.sender_mail, email, message)
        except Exception as e:
            print(f"Error sending email: {e}")

class AudioMonitor:
    def __init__(self, threshold, max_silent_samples, log_file, mail_client):
        self.hostname = socket.gethostname()  # Retrieve hostname during initialization
        self.threshold = threshold
        self.max_silent_samples = max_silent_samples
        self.log_file = open(log_file, "a")
        self.mail_client = mail_client
        self.silent_counter = 0
        self.is_silent = True
        self.silence_start_time = None  # Track when silence starts
        self.log_event("The script was launched on the host machine")
        self.mail_client.send(
            TO_ADDRESSES, 
            "Whisper Sentinel - Launched", 
            f"This is an email to inform you that Whisper Sentinel was launched on the host machine [{self.hostname}] and has commenced monitoring.\n\nPlease be aware that before this script launched, there was no active monitoring of audio.\n\n =This message was automatically generated by Whisper Sentinel - https://github.com/trentnetau/whispersentinel/ = "
            )
        self.clear_screen()

    def log_event(self, message):
        timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
        self.log_file.write(f"{timestamp}{message}\n")
        self.log_file.flush()

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def handle_audio(self, indata):
        volume_norm = np.linalg.norm(indata) * 10
        max_bar_length = 50  # Set your desired maximum length
        bar_length = int(volume_norm)
        if bar_length > max_bar_length:
            bar_length = max_bar_length
        self.clear_screen()
        print(f"Audio Input VU: {volume_norm:.2f} {'═' * bar_length}")

        if volume_norm < self.threshold:
            self.silent_counter += 1
            if self.silent_counter > self.max_silent_samples and not self.is_silent:
                self.is_silent = True
                self.silence_start_time = datetime.datetime.now()  # Silence starts now
                self.log_event("Whisper Sentinel detected a silence period of more than 8 seconds, which has triggered an email notification and count of the duration until audio is restored.")
                self.mail_client.send(
                    TO_ADDRESSES, 
                    "Whisper Sentinel - Silence Trigger", 
                    f"This is an email to inform you that Whisper Sentinel detected a silence period of more than 8 seconds on the host machine [{self.hostname}], which has triggered this alert. The audio is not restored at this stage.\n\nIt is recommended that you check the originating audio source.\n\n =This message was automatically generated by Whisper Sentinel - https://github.com/trentnetau/whispersentinel/ = "
                    )
        else:
            if self.is_silent:
                self.is_silent = False
                silence_end_time = datetime.datetime.now()
                if self.silence_start_time:
                    silence_duration = silence_end_time - self.silence_start_time
                    silence_duration_seconds = silence_duration.total_seconds()
                    self.log_event(f"Whisper Sentinel detected that audio is now restored after {silence_duration_seconds:.2f} seconds from the initial silence trigger")
                    self.mail_client.send(
                        TO_ADDRESSES,
                        "Whisper Sentinel - Audio Return",
                        f"The Whisper Sentinel instance on host machine [{self.hostname}] has detected that source audio is now restored, {silence_duration_seconds:.2f} seconds after the initial silence trigger notification that you received.\n\nIt is recommended that you check the originating audio source if you are not recieving an Audio return email or a number of notifications in succession.\n\n =This message was automatically generated by Whisper Sentinel - https://github.com/trentnetau/whispersentinel/ = "
                    )
                else:
                    self.log_event("Whisper Sentinel detected a return to normal audio levels")
                    self.mail_client.send(
                        TO_ADDRESSES, 
                        "Whisper Sentinel - Audio Source Detection", 
                        f"This is an email to inform you that Whisper Sentinel has detected the originating audio source that it is configured to listen for on source machine [{self.hostname}].\n\nThis is due to a fresh instance of the script starting on the host machine.\n\n =This message was automatically generated by Whisper Sentinel - https://github.com/trentnetau/whispersentinel/ = "
                        )
                self.silence_start_time = None  # Reset silence start time
            self.silent_counter = 0

def audio_callback(indata, frames, time, status, monitor):
    if status:
        if status.input_overflow:
            monitor.log_event("ALSA Overrun detected: Input overflow occurred.")
            print("ALSA Overrun detected. Restarting stream...")
            restart_stream(monitor)  # Restart the stream gracefully
            return
    monitor.handle_audio(indata)
    
def restart_stream(monitor):
    try:
        with sd.InputStream(callback=lambda indata, frames, time, status: audio_callback(indata, frames, time, status, monitor)):
            monitor.log_event("Originating audio input restarted after ALSA Overrun.")
            print("Audio stream successfully restarted.")
            while True:
                time.sleep(0.1)  # Keep the stream alive
    except Exception as e:
        monitor.log_event(f"Error restarting audio stream: {e}")
        print(f"Error restarting audio stream: {e}")
        sys.exit(1)  # Exit if the stream cannot be restarted

if __name__ == "__main__":
    mail_client = Mail(SENDER_EMAIL, SENDER_NAME, SENDER_PASSWORD, SMTP_SERVER, SMTP_PORT)
    monitor = AudioMonitor(THRESHOLD, MAX_SILENT_SAMPLES, LOG_FILE, mail_client)

    try:
        restart_stream(monitor)  # Start the stream and monitor
    except KeyboardInterrupt:
        monitor.log_event("Application terminated by user")
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        monitor.log_file.close()
