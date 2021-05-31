from subprocess import call
import wikipedia
from app.nlp import build_qa_model
from app.audio import SpeechToWave
from app.nlp import Transcriber

transcriber = Transcriber('facebook/wav2vec2-base-960h')
qa_model = build_qa_model()


def speak(message: str) -> None:
    message = message.replace("'", "\'")
    call(["say", f"'{message}"])


def get_wiki_content(requested_topic: str) -> wikipedia.WikipediaPage:
    hits = wikipedia.search(requested_topic)
    return wikipedia.page(hits[0], auto_suggest=False)


def listen_for_answer(listen_time: int = 3) -> str:
    recorder = SpeechToWave()

    wave_file = recorder.record(listen_time)
    text = transcriber.process(wave_file)
    recorder.delete_file(wave_file)
    return ' '.join(text).strip()
    # return ' '.join([t.split('</s>')[1].strip() for t in text])


def main():
    speak("Hi, what is your name?")
    name = listen_for_answer()

    speak(f"Hello, {name}! What would you like to learn about today?")
    topic = listen_for_answer()

    speak(f"Thanks! I'm reading about {topic} now.")
    wiki_content = get_wiki_content(topic)
    speak(f"What would you like to know about {topic}?")
    question = listen_for_answer(5)

    answer = qa_model(context=wiki_content.summary, question=question)
    speak(answer.get('answer', ''))
    return


if __name__ == '__main__':
    main()
