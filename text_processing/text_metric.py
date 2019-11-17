import textstat
import nltk

from text_processing.emotions_extractor import IBMEmotionalAnalysis


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

    def evaluate(self, text: str):
        return {
            'easy_to_listen_score': self._ease_mapper[(round(textstat.flesch_reading_ease(text)) - 1) // 10],
            'text_general_level': self._general_level_mapper[textstat.text_standard(text, float_output=True)],
            'text_uniqueness': self._uniqueness_mapper[self.text_uniqueness(text) * 10],
            'emotions': list(self._emotion_detector.extract_emotions_from_raw_text(text))
        }

    @classmethod
    def text_uniqueness(cls, text: str):
        tokens = nltk.word_tokenize(text)
        return len(set(nltk.word_tokenize(text))) / len(tokens)


if __name__ == '__main__':
    tme = TextMetricEvaluator()
    print(tme.evaluate('I believe we can do it better. Otherwise, there is nothing to talk about'))
