from flask import Flask, render_template, request, jsonify
import os
from pydub import AudioSegment
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import soundfile as sf

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Cargar modelo y procesador una sola vez
processor = Wav2Vec2Processor.from_pretrained("./wav2vec2-spanish-custom")
model = Wav2Vec2ForCTC.from_pretrained("./wav2vec2-spanish-custom")
model.eval()

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

    # Convertir a wav si es necesario
    ext = filename.split('.')[-1].lower()
    if ext == 'mp3':
        sound = AudioSegment.from_mp3(filename)
        wav_filename = filename.rsplit('.', 1)[0] + '.wav'
        sound.export(wav_filename, format='wav')
    elif ext == 'webm':
        sound = AudioSegment.from_file(filename, format='webm')
        wav_filename = filename.rsplit('.', 1)[0] + '.wav'
        sound.export(wav_filename, format='wav')
    else:
        wav_filename = filename

    # Leer audio y convertir a texto usando Wav2Vec2
    try:
        speech, rate = sf.read(wav_filename)
        input_values = processor(speech, sampling_rate=rate, return_tensors="pt").input_values
        with torch.no_grad():
            logits = model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        text = processor.batch_decode(predicted_ids)[0]
    except Exception as e:
        text = f'Error: {str(e)}'

    # Limpiar archivos
    os.remove(filename)
    if wav_filename != filename:
        os.remove(wav_filename)

    return jsonify({'text': text})

if __name__ == '__main__':
    app.run(debug=True)
