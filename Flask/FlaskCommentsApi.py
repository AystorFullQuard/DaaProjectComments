from flask import Flask, request, jsonify
from googleapiclient.discovery import build
import os
import json

app = Flask(__name__)

# My Api youtube key
API_KEY = 'AIzaSyBdintWx6tYkvnhwpjmBDeo55LNITEx_os'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


def get_comments(video_id):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
    comments = []
    results = youtube.commentThreads().list(part="snippet", videoId=video_id, textFormat="plainText").execute()

    while results:
        for item in results['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append({
                'author': comment['authorDisplayName'],
                'text': comment['textDisplay'],
                'published_at': comment['publishedAt']
            })

        if 'nextPageToken' in results:
            results = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                pageToken=results['nextPageToken'],
                textFormat="plainText"
            ).execute()
        else:
            break

    return {'comments': comments}


@app.route('/get_comments', methods=['GET'])
def get_comments_route():
    video_url = request.args.get('video_url')
    if not video_url:
        return jsonify({'error': 'No video URL provided'}), 400

    video_id = video_url.split("v=")[1]
    comments = get_comments(video_id)

    return app.response_class(
        response=json.dumps(comments, ensure_ascii=False).encode('utf-8'),
        status=200,
        mimetype='application/json; charset=utf-8'
    )


if __name__ == '__main__':
    app.run(debug=True, port=5001)
