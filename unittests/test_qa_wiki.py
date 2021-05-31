from subprocess import call
import wikipedia
from app.nlp import build_qa_model

model = build_qa_model()

hits = wikipedia.search('neural network')
page = wikipedia.page(hits[0], auto_suggest=False)

answer = model(context=page.summary, question='What is a neural network?')
print(answer)

call(["say", f"'{answer.get('answer')}"])
