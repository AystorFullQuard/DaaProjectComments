from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# URLs микросервисов
GET_COMMENTS_URL = 'http://127.0.0.1:5001/get_comments'
ANALYZE_COMMENTS_URL = 'http://127.0.0.1:5002/analyze_comments'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_metrics', methods=['POST'])
def get_metrics():
    data = request.json
    video_url = data.get('video_url')
    if not video_url:
        return jsonify({'error': 'No video URL provided'}), 400

    response = requests.get(GET_COMMENTS_URL, params={'video_url': video_url})
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch comments'}), response.status_code

    comments = response.json()

    analyze_response = requests.post(ANALYZE_COMMENTS_URL, json=comments)
    if analyze_response.status_code != 200:
        return jsonify({'error': 'Failed to analyze comments'}), analyze_response.status_code

    metrics = analyze_response.json()
    return jsonify(metrics)

if __name__ == '__main__':
    app.run(debug=True, port=5003)
