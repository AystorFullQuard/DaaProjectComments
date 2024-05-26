from flask import Flask, request, jsonify
from textblob import TextBlob

app = Flask(__name__)


def analyze_sentiment(comments):
    sentiment_counts = {'positive': 0, 'neutral': 0, 'negative': 0}

    for comment in comments:
        analysis = TextBlob(comment['text'])
        if analysis.sentiment.polarity > 0:
            sentiment_counts['positive'] += 1
        elif analysis.sentiment.polarity == 0:
            sentiment_counts['neutral'] += 1
        else:
            sentiment_counts['negative'] += 1

    return sentiment_counts


@app.route('/analyze_comments', methods=['POST'])
def analyze_comments_route():
    data = request.get_json()
    if 'comments' not in data:
        return jsonify({'error': 'No comments provided'}), 400

    comments = data['comments']
    sentiment_counts = analyze_sentiment(comments)

    return jsonify(sentiment_counts)


if __name__ == '__main__':
    app.run(debug=True, port=5002)
