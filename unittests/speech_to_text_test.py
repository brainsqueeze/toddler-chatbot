from app.audio import SpeechToWave
from app.nlp import Transcriber

recorder = SpeechToWave()
transcriber = Transcriber()
print("Recording...")
wave_file = recorder.record(3)

text = transcriber.process(wave_file)
print(text)
recorder.delete_file(wave_file)
