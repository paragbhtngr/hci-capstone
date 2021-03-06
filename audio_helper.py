import pyaudio
import wave
import sys

from threading import Thread, Event
from time import sleep


class AudioFile(Thread):
    chunk = 1024

    def __init__(self, file):
        """ Init audio stream """
        Thread.__init__(self)
        self.wf = wave.open(file, 'rb')
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format = self.p.get_format_from_width(self.wf.getsampwidth()),
            channels = self.wf.getnchannels(),
            rate = self.wf.getframerate(),
            output = True
        )
        self._stop = Event()

    def run(self):
        self._stop.clear()
        """ Play entire file """
        while not self._stop.is_set():
            data = self.wf.readframes(self.chunk)
            self.stream.write(data)

    def stop(self):
        """ Graceful shutdown """
        self._stop.set()
        self.stream.close()
        self.p.terminate()
