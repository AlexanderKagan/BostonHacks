import json

import bottle
from bottle import route, request, error, template, static_file

app = bottle.app()


@route('/')
def index():
    return template('static/index.html')

@route('/recorder_receiver', method='POST')
def recorder_receiver():
    audio_data = request.files.get('audio_data')
    audio_data.save('record.wav')

@route('/<filename:path>')
def send_file(filename):
    return static_file(filename, root='static/')


if __name__ == '__main__':
    bottle.debug(True)
    bottle.run(app=app, host='localhost', port=5050)