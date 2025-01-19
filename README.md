# Whisper Sentinel
Whisper Sentinel is a Python based tool that will assist with monitoring of an audio source for gaps in the audio being provided, for which alerting will be provided over email and logged in a file stored on the originating system.
This system is most helpful for Radio Broadcast applications, where a break in programming can impact the listening experience for those tuned into the broadcast and impact revenue for the station.

The tool is a single flat file which requires only a few lines of configuration once your system is properly configured to run the tool. It is designed to function on anything from a small single board computer to a virtual machine or desktop, as long as you have a way of providing the application with an audio input source it can listen to.

The essence of the tool was derived from a project by Miro - https://www.mirobarsa.com/technology/real-time-detect-silence-from-audio-input-in-linux/ but contains some adaptions to improve it's usability.

**This script is provided under an MIT License.**

**Copyright (c) 2025 Trent Geddes.**

**Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is provided to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software, in it's entirety without edits.**

**THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.**

