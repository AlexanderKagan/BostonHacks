import typing as tp
import json
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# path to private ibm credentials
with open('../keys/ibm_tone_analysis.json') as f:
    credentials = json.load(f)


class IBMEmotionalAnalysis:
    def __init__(self):
        self._authenticator = IAMAuthenticator(credentials['key'])
        self._analyzer = ToneAnalyzerV3(
            version='2017-09-21',
            authenticator=self._authenticator
        )
        self._analyzer.set_service_url(credentials['url'])

    def extract_emotions_from_raw_text(self, text: str) ->tp.Dict[str, int]:
        response = self._analyzer.tone({'text': text}, content_type='application/json').get_result()
        output = {}
        for tone in response['document_tone']['tones']:
            output[tone['tone_name'].lower()] = tone['score']
        return output


if __name__ == '__main__':
    emotion_extractor = IBMEmotionalAnalysis()
    text = "I'm so sad ( I missed my bus and have to walk 3 kilometres"
    print(emotion_extractor.extract_emotions_from_raw_text(text))