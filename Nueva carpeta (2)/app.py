from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import os
from pydub import AudioSegment

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['audio']
    filename = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filename)

    # Convert to wav if necessary
    if filename.endswith('.mp3'):
        sound = AudioSegment.from_mp3(filename)
        wav_filename = filename.rsplit('.', 1)[0] + '.wav'
        sound.export(wav_filename, format='wav')
    else:
        wav_filename = filename

    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_filename) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language='es-ES')
        except Exception as e:
            text = f'Error: {str(e)}'

    # Clean up files
    os.remove(filename)
    if wav_filename != filename:
        os.remove(wav_filename)

    return jsonify({'text': text})

if __name__ == '__main__':
    app.run(debug=True)
