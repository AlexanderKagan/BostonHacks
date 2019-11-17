import random

import textstat
import nltk
import typing
import json

from text_processing.emotions_extractor import IBMEmotionalAnalysis
from text_processing.google_nlp import GoogleNLPModule

with open('data/prewritten_chars.json') as json_file:
    prewritten_chars = json.load(json_file)


class TextMetricEvaluator:
    def __init__(self):
        self._ease_mapper = {
            0: 0,
            1: 1,
            2: 1,
            3: 2,
            4: 3,
            5: 4,
            6: 5,
            7: 6,
            8: 7,
            9: 8,
            10: 9
        }

        self._general_level_mapper = {
            0: 0,
            1: 0,
            2: 0,
            3: 0,
            4: 3,
            5: 4,
            6: 5,
            7: 6,
            8: 7,
            9: 8,
            11: 9,
            12: 9,
            13: 9,
            14: 9,
            15: 9,
        }

        self._uniqueness_mapper = {
            0: 1,
            1: 1,
            2: 2,
            3: 3,
            4: 4,
            5: 5,
            6: 6,
            7: 7,
            8: 8,
            9: 9,
            10: 9
        }

        self._emotion_detector = IBMEmotionalAnalysis()
        self._google_nlp = GoogleNLPModule()

    def evaluate(self, text: str):
        extracted_emotions = self._emotion_detector.extract_emotions_from_raw_text(text)
        extracted_sentiment = self._google_nlp.extract_sentiment_from_raw_text(text)

        # self._ease_mapper[(round(textstat.flesch_reading_ease(text)) - 1) // 10],
        return {
            'clarity': 5,
            'text_general_level': self._general_level_mapper[textstat.text_standard(text, float_output=True)],
            'diversity': self._uniqueness_mapper[self.text_uniqueness(text) * 10],
            'tone': self.emotion_converter(extracted_emotions),
            'emotional_tones': list(extracted_emotions.keys()),
            'speech_sentiment': extracted_sentiment['sentiment']*10 if 'sentiment' in extracted_sentiment else 5,
            'engagement': extracted_emotions['magnitude'] if 'magnitude' in extracted_emotions else 5,
            'who_do_you_look_like': self.who_do_you_look_like(extracted_emotions),
            'calmness': random.randint(5, 9)
        }

    @classmethod
    def text_uniqueness(cls, text: str):
        tokens = nltk.word_tokenize(text)
        return len(set(nltk.word_tokenize(text))) / len(tokens)

    @classmethod
    def emotion_converter(cls, extracted_emotions: typing.Dict[str, typing.Any]):
        if not extracted_emotions:
            return 6
        if 'analytical' in extracted_emotions or 'confident' in extracted_emotions:
            return 8
        if 'tentative' in extracted_emotions:
            return 6
        if 'anger' in extracted_emotions:
            return 5
        if 'fear' in extracted_emotions or 'sadness' in extracted_emotions:
            return 4
        if 'disgust' in extracted_emotions:
            return 4
        if 'joy' in extracted_emotions:
            return 8

    @classmethod
    def who_do_you_look_like(cls, extracted_emotions):
        return random.choice(prewritten_chars)

    @classmethod
    def random_response(cls, text: str):
        clarity = random.randint(3, 10)
        return {
            'clarity': clarity,
            'text_general_level': random.randint(clarity - 2, 10),
            'diversity': random.randint(clarity - 1, 10),
            'tone': random.randint(clarity - 2, 10),
            'emotional_tones': ['joy'],
            'speech_sentiment': random.randint(-5, 5),
            'engagement': random.randint(clarity, 10),
            'who_do_you_look_like': cls.who_do_you_look_like(None),
            'calmness': random.randint(clarity, 10)
        }


if __name__ == '__main__':
    tme = TextMetricEvaluator()
    result = tme.evaluate('I believe we can do it better. Otherwise, there is nothing to talk about')
