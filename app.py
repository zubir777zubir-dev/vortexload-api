from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp, os

app = Flask(__name__)
CORS(app)

@app.route('/info')
def info():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'no url'}), 400
    ydl_opts = {'quiet': True, 'noplaylist': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        data = ydl.extract_info(url, download=False)
    formats = []
    for f in data.get('formats', []):
        if f.get('url'):
            formats.append({
                'format_id': f.get('format_id'),
                'ext': f.get('ext'),
                'quality': f.get('height'),
                'url': f.get('url'),
                'vcodec': f.get('vcodec'),
                'acodec': f.get('acodec'),
            })
    return jsonify({'title': data.get('title'), 'thumbnail': data.get('thumbnail'), 'formats': formats})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
