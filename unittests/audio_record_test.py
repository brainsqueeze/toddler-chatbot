from app.audio import SpeechToWave


recorder = SpeechToWave()
wave_file = recorder.record(10)
print(wave_file)

