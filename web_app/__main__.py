from flask import Flask, abort
from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    download_format = request.form.get('format')

    try:
        youtube = YouTube(url)
        video_stream = youtube.streams.get_highest_resolution(
        ) if download_format == 'video' else youtube.streams.filter(only_audio=True).first()
        output_folder = '..\downloads'

        os.makedirs(output_folder, exist_ok=True)
        video_stream.download(output_folder)
        """
        os.path.join(
                    os.path.expanduser("~"), "", "YTconvertor", "Audios")
        """
        return send_file(f"{output_folder}\\{video_stream.title.replace("//", "")}.{video_stream.subtype}", as_attachment=True)

    except Exception as e:
        abort(404)


if __name__ == '__main__':
    app.run(debug=True)
