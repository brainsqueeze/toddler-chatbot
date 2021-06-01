from subprocess import call
from sys import platform
import random
import hashlib
import wave
import os

import pyaudio


def speak(message: str) -> None:
    message = message.replace("'", "\'")
    if platform == 'darwin':
        call(["say", f"'{message}"])
    elif platform == "linux":
        call(["spd-say", f"'{message}"])
    else:
        print(message)


class SpeechToWave:

    # FORMAT = pyaudio.paInt16
    FORMAT = pyaudio.paInt32
    CHANNELS = 2  # Adjust to your number of channels
    RATE = 44100  # Sample Rate
    # RATE = 16_000
    CHUNK = 1024  # Block Size
    RECORD_SECONDS = 5  # Record time

    def __init__(self):
        self.audio = pyaudio.PyAudio()

    def record(self, length: int = 5):
        frames = []
        stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )

        print("recording...")
        for _ in range(0, int(self.RATE / self.CHUNK * length)):
            data = stream.read(self.CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        self.audio.terminate()

        # Write your new .wav file with built in Python 3 Wave module
        file_name = hashlib.sha256(str(random.randint(-100, 100)).encode('utf8')).hexdigest()
        waveFile = wave.open(f"{file_name}.wav", 'wb')
        waveFile.setnchannels(self.CHANNELS)
        waveFile.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        waveFile.setframerate(self.RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        return file_name

    @staticmethod
    def delete_file(wave_file: str):
        if wave_file.endswith(".wav"):
            os.remove(wave_file)
        else:
            os.remove(f"{wave_file}.wav")
