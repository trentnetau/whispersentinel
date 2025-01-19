# // CHANGELOG
# 0.1.78 - This is where the functional stuff is already largely completed, so we spend some time on cleaning up anything that could be done better or displayed better in the script.
# 0.1.77 - Moved the majority of the user configurable settings to the top of the script in the Configuration region, so it's configurable by any joe who can open a file and do some basic config changes. Also added a count to the audio return email notification and logging to provide an idea on how long it was off for.
# 0.1.76 - Adjusted the in terminal level/refresh to test a header/footer and clean up it's presentation on screen.
# 0.1.75 - This fool doesn't do much programming and usually writes over his own muck, so some sort of versioning adjustments were made for the minor bunch of changes that keep happening. Also, testing was made to see if you could get the app to email before being terminated...it was removed shortly after.
# 0.1.6 - The process of sending an email was pretty rudimentary at this point, so changes were made to the sending process to ensure that TO/FROM/SUBJECT fields were cleaned up and display in the sending process.
# 0.1.5 - As the orignal script is looking for dead silence which is not always achieved depending upon the quality of the hardware we are using to input audio, a tweak was made to allow a minimum threshold to be set instead of relying on dead silence before a trigger.
# 0.1.4 - The way in which the refreshing of the input indicator display was changed, to see if it would improve how it displayed.
# 0.1.3 - A label was added to the audio input indicator to make it obvious as to what it is.
# 0.1.2 - The original version had no way of indicating what was going on at console end with audio levels, so this version commenced a visual audio input indicator (numbers and bars).
# 0.1.0 - This was actually the initial input of the original real time detect silence script from Miro, with some minor adjustments to fix indentation and syntax errors, adjustment of global variables and implementing some error handling plus the addition of AudioMonitor for better modularity. Some improvements to readability were also made.
