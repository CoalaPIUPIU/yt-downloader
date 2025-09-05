from flask import Flask, request, send_file, render_template
import yt_dlp
import os

app = Flask(__name__)

def baixar_musica(nome_musica):
    arquivo_saida = "%(title)s.%(ext)s"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': arquivo_saida,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }
    search_url = f"ytsearch1:{nome_musica}"
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(search_url, download=True)
    return ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/baixar', methods=['POST'])
def baixar():
    nome_musica = request.form['musica']
    arquivo = baixar_musica(nome_musica)
    return send_file(arquivo, as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)