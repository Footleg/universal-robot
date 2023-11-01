#!/usr/bin/env python3
""" 
    Audio Server

    Copyright (C) 2023 Paul 'Footleg' Fretwell
    Released under the GNU GPL v3 license
    Code repo: https://github.com/Footleg/universal-robot

    This module provides both an audio playback service and a text to speech
    method you can call to queue up phrases for your Pi to speak.
    
    The playback service is activated when you run this module in python. It
    will run in a continuous loop monitoring a folder for audio WAV files to
    play. Any WAV files found in the audio_queue folder will be played one
    after the other in file created date order. Once played a file will be
    moved to the audio_store folder. When the server is running, you can test it
    is working simply by copying any WAV file into the audio queue folder. It
    should be played and moved to the audio store folder.
    
    To generate speech from text, import the SpeechGenerator class into your
    python program, and create an instance:
    
        speechGen = SpeechGenerator()
        
    You can then generate and queue audio files to say text by calling the
    queueSpeech method:
    
        speechGen.queueSpeech("Hello Footleg")
        
    This will generate a new WAV file for this text and queue it up for the
    playback service to play. If you send the same text again, it will reuse
    the wav file already generated (from the audio store folder).
    
    Installation dependencies:
    The speech generation features uses flite to generate the audio and
    normalize_audio to boost the volume (as flite is fairly quiet).
    Install these command line tools with:
    
        sudo apt-get install flite normalize-audio
        
    The playback service uses the aplay command line player. This is already
    installed on Raspberry Pi OS.
    
    Flite comes with different voices. You can list these in a terminal with
    the command:
    
        flite -lv
        
    Set the voice to any of those listed by flite when you create the
    SpeechGenerator class. e.g. For voice 'awb':
    
        speechGen = SpeechGenerator(voice="awb")
        
    Set the volume boost with a boost value (in db):
    
        speechGen = SpeechGenerator(voice="awb", boost=6)
        
    If the speech sounds distorted, you have probably boosted it too much for
    your speakers. With the tiny 1.5W speaker I use on my small robots, a
    boost in the range 6-8 works best for most voices.
"""

from os import listdir, system
from os.path import isfile, join, getmtime
from time import sleep

audio_queue = "/home/pi/universal-robot/audio_queue"
audio_store = "/home/pi/universal-robot/audio_store"

class SpeechGenerator():
    def __init__(self,voice:str="kal",boost:int=7):
        self.voice = voice
        self.boost = boost

    def queueSpeech(self,text:str):
        ''' Create an audio wav file to speak '''
        
        # Generate filename for this text
        filename = f"{self.voice}_{self.boost}_" + \
            text.replace(" ", "_").replace("?", "-").replace("\'", ".") + ".wav"
            
        # Check if the file is already generated
        fileInStore = isfile(f"{audio_store}/{filename}")
        if not isfile(f"{audio_queue}/{filename}") and not fileInStore:
            # Generate new file in store
            system(f"flite -voice {self.voice} -t \"{text}\" {audio_store}/{filename}")
            system(f"normalize-audio --gain={self.boost}db {audio_store}/{filename}")
            fileInStore = True
            
        if fileInStore:
            self.playAudio(filename)
            

    def playAudio(self,filename:str):
        if isfile(f"{audio_queue}/{filename}"):
            # File already in queue, so do nothing (prevents file overwrite
            # while being played if same file is requested again before it
            # is processed from the queue
            pass
        elif isfile(f"{audio_store}/{filename}"):
            # Move existing file into queue
            system(f"mv {audio_store}/{filename} {audio_queue}/{filename}")

def runPlaybackServer():
    while True:
        # Watch folder for text files to speak
        files = [f for f in listdir(audio_queue) if isfile(join(audio_queue, f))]

        # Sort files by created date
        files.sort(key=lambda f: getmtime(join(audio_queue, f)))

        for file in files:
            # Play audio file
            system(f"aplay {audio_queue}/{file}")
            # Move out of queue
            system(f"mv {audio_queue}/{file} {audio_store}/{file}")
            sleep(0.2)
            
    sleep(0.2)


if __name__ == '__main__':
    runPlaybackServer()