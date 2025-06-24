from flask import Flask, render_template, request, jsonify
import lyricsgenius
import requests

app = Flask(__name__)

# Token da Genius
GENIUS_API_TOKEN = "PBj78jewAAmw6KJWJFLX2ygN2O2T3NEXy1QY1EsDfi84wk9zKQ-X0CWZd9Fksrzy"
genius = lyricsgenius.Genius(GENIUS_API_TOKEN)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_lyrics", methods=["POST"])
def get_lyrics():
    data = request.json
    artist = data.get("artist")
    song = data.get("song")

    if not artist or not song:
        return jsonify({"error": "Dados incompletos"}), 400

    try:
        result = genius.search_song(song, artist)
        if result and result.lyrics:
            return jsonify({"lyrics": result.lyrics})
        else:
            return jsonify({"error": "Letra não encontrada."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/translate", methods=["POST"])
def translate():
    data = request.json
    text = data.get("text")

    if not text:
        return jsonify({"error": "Texto não enviado"}), 400

    try:
        translate_url = "https://libretranslate.de/translate"
        payload = {
            "q": text,
            "source": "en",
            "target": "pt",
            "format": "text"
        }
        response = requests.post(translate_url, json=payload)
        result = response.json()
        return jsonify({"translatedText": result.get("translatedText", "Falha na tradução.")})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)