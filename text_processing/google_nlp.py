import os
import typing as tp
from collections import defaultdict
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

# path to private google credentials

_from_enum_conversion = {
    0: 'UNKNOWN',
    1: 'PERSON',
    2: 'LOCATION',
    3: 'ORGANIZATION',
    4: 'EVENT',
    5: 'WORK_OF_ART',
    6: 'CONSUMER_GOOD',
    7: 'OTHER',
    8: 'PHONE_NUMBER',
    9: 'ADDRESS',
    10: 'DATE',
    11: 'NUMBER',
    12: 'PRICE'
}


class GoogleNLPModule:
    def __init__(self):
        self._client = language.LanguageServiceClient()

    def extract_sentiment_from_raw_text(self, text: str) -> tp.Dict[str, tp.Any]:
        document = self._create_document(text)
        sentiment = self._client.analyze_sentiment(document=document)
        output = {
            'magnitude': sentiment.document_sentiment.magnitude,
            'sentences': []
        }
        for sentence in sentiment.sentences:
            output['sentences'].append({
                'text': sentence.text.content,
                'sentiment': sentence.sentiment.score,
                'magnitude': sentence.sentiment.magnitude
            })
        return output

    def extract_sentiment_from_sentence(self, text: str):
        document = self._create_document(text)
        sentiment = self._client.analyze_sentiment(document=document).document_sentiment
        return {
            'sentiment': sentiment.score,
            'magnitude': sentiment.magnitude
        }

    def extract_entities_from_sentence(self, text: str) -> tp.Dict[str, tp.Any]:
        document = self._create_document(text)
        extracted_entites = self._client.analyze_entities(document=document)
        output = defaultdict(list)
        for entity in extracted_entites.entities:
            output[_from_enum_conversion[entity.type]].append({'name': entity.name, 'relevance': entity.salience})
        return output

    @classmethod
    def _create_document(cls, text: str):
        return types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)


if __name__ == '__main__':
    google_nlp = GoogleNLPModule()

    # sentiment = google_nlp.extract_sentiment_from_raw_text(
    #     'how about have some shit at paris? I want to rest a little before party :)')
    # for s in sentiment['sentences']:
    #     print(s)

    entities = google_nlp.extract_entities_from_sentence(
        'how about have some shit at paris with Alice in Macdonalds next monday?')
    for s in entities:
        print(s, entities[s])