from subprocess import call
from app.audio import SpeechToWave
from app.nlp import Transcriber

transcriber = Transcriber('facebook/wav2vec2-base-960h')


def speak(message: str) -> None:
    message = message.replace("'", "\'")
    call(["say", f"'{message}"])


def listen_for_answer(listen_time: int = 3) -> str:
    recorder = SpeechToWave()

    wave_file = recorder.record(listen_time)
    text = transcriber.process(wave_file)
    recorder.delete_file(wave_file)
    return ' '.join(text).strip()


def main():
    speak("Hi, what is your name?")
    name = listen_for_answer()

    speak(f"Hello {name}! Are you happy or sad?")
    answer = listen_for_answer(2)

    while True:
        try:
            if 'sad' in answer.lower():
                speak("Why are you sad?")
                answer = listen_for_answer(2)
            elif 'crying' in answer.lower():
                speak("Why are you crying?")
                answer = listen_for_answer(2)
            elif 'happy' in answer.lower():
                speak("Why are you happy?")
                answer = listen_for_answer(2)
            else:
                speak("Would you like to play again?")
                answer = listen_for_answer(2)
                if "no" in answer.lower():
                    break
            continue
        except KeyboardInterrupt:
            break
    return


if __name__ == '__main__':
    main()
