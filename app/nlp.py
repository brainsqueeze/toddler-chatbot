import os

import torch
from transformers import Speech2TextProcessor
from transformers import Speech2TextForConditionalGeneration
from transformers import Wav2Vec2Tokenizer
from transformers import Wav2Vec2ForCTC
# from transformers import TRANSFORMERS_CACHE
from transformers import pipeline

import librosa

os.environ["TOKENIZERS_PARALLELISM"] = "true"


class Transcriber:

    def __init__(self, model_name: str = 'facebook/s2t-small-librispeech-asr') -> None:
        if model_name == 'facebook/s2t-small-librispeech-asr':
            self.model = Speech2TextForConditionalGeneration.from_pretrained(model_name)
            self.processor = Speech2TextProcessor.from_pretrained(model_name)
            self.process = self.__process_s2t
        elif model_name == 'facebook/wav2vec2-base-960h':
            self.processor = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
            self.model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
            self.process = self.__process_w2v
        else:
            raise TypeError(f"Model {model_name} either does not exist or is not supported")

    @staticmethod
    def load(wave_file: str):
        if wave_file.endswith('.wav'):
            data, sample_rate = librosa.load(wave_file, sr=16000)
        else:
            data, sample_rate = librosa.load(f"{wave_file}.wav", sr=16000)
        return data, sample_rate

    def __process_w2v(self, wave_file: str):
        data, _ = self.load(wave_file)

        input_values = self.processor(data, return_tensors="pt", padding="longest").input_values
        logits = self.model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        return self.processor.batch_decode(predicted_ids)

    def __process_s2t(self, wave_file: str):
        data, sample_rate = self.load(wave_file)

        # Batch size 1
        input_features = self.processor(data, sampling_rate=sample_rate, return_tensors="pt").input_features
        generated_ids = self.model.generate(input_ids=input_features)
        return self.processor.batch_decode(generated_ids)


def build_qa_model(model_name: str = 'deepset/roberta-base-squad2'):
    return pipeline(task='question-answering', model=model_name)
