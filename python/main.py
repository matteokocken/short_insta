from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
from pathlib import Path
import whisper
import os
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)

def download_video(video_url, output_path):
    """
    Télécharge une vidéo depuis une URL en utilisant yt-dlp.
    """
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_path
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

def generate_subtitles(video_path):
    """
    Génère des sous-titres pour une vidéo à l'aide de Whisper.
    """
    model = whisper.load_model("base")  # ou un autre modèle selon les besoins
    result = model.transcribe(video_path)
    return result['text']

@app.route('/get_subtitles', methods=['POST'])
def get_subtitles():
    data = request.json
    video_url = data.get('video_url')
    if not video_url:
        return jsonify({'error': 'No video URL provided'}), 400

    # Générer un nom de fichier unique pour chaque vidéo
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = uuid.uuid4().hex
    output_path = f"videos/{timestamp}_{unique_id}.mp4"

    try:
        print("Téléchargement de la vidéo...")
        download_video(video_url, output_path)

        if Path(output_path).is_file():
            print("Génération des sous-titres...")
            subtitles = generate_subtitles(output_path)

            # Supprimer la vidéo après la transcription
            os.remove(output_path)

            return jsonify({'subtitles': subtitles})
        else:
            return jsonify({'error': 'Failed to download the video'}), 500
    except Exception as e:
        # S'assurer que la vidéo est supprimée même en cas d'erreur
        if Path(output_path).is_file():
            os.remove(output_path)
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)