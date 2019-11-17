import json

import bottle
from bottle import route, request, error, template, static_file, response

from audio_recognition.speech_processing import audio_to_text
from text_processing.text_metric import TextMetricEvaluator
import json

app = bottle.app()

tme = TextMetricEvaluator()


@route('/')
def index():
    return template('static/index.html')


@route('/recorder_receiver', method='POST')
def recorder_receiver():
    audio_data = request.files.get('audio_data')
    audio_data.save('record.wav')
    try:
        converted_from_audio = audio_to_text('record.wav')
        print(converted_from_audio)
        analyze_result = tme.evaluate(converted_from_audio)
        print(analyze_result)
    except KeyError as e:
        return tme.random_response('')
    response.content_type = 'application/json'
    return json.dumps(analyze_result)


@route('/<filename:path>')
def send_file(filename):
    return static_file(filename, root='static/')


if __name__ == '__main__':
    bottle.debug(True)
    bottle.run(app=app, host='localhost', port=5050)
