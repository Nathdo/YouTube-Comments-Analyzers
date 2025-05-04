from flask import Flask, render_template, request, redirect, url_for
from youtube_api import (
    get_comments_from_url,
    extract_video_id,
    get_video_info
)
from openai_api import (
    analyze_comments,
    extract_topics,
    analyze_emotions,
    extract_emotions
)
from history_manager import load_history, save_to_history
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = None
    topics = None
    emotions = None
    emotion_labels = []
    emotion_values = []
    history = load_history()

    if request.method == 'POST':
        video_url = request.form['youtube_url']
        video_id = extract_video_id(video_url)
        video_title, thumbnail_url = get_video_info(video_id)

        comments = get_comments_from_url(video_url)
        comments_text = "\n".join(comments)

        summary = analyze_comments(comments_text)
        topics = extract_topics(comments_text)

        emotion_result = analyze_emotions(comments_text)
        emotions = {
            "description": emotion_result.get("description", "")
        }
        emotion_labels, emotion_values = extract_emotions(emotion_result.get("counts", {}))

        save_to_history(video_url, summary, video_title, thumbnail_url)
        history = load_history()

    return render_template(
        'index.html',
        summary=summary,
        topics=topics,
        emotions=emotions,
        emotion_labels=emotion_labels,
        emotion_values=emotion_values,
        history=history
    )

@app.route('/clear-history', methods=['POST'])
def clear_history():
    with open("history.json", "w") as f:
        f.write("[]")
    return redirect(url_for('index'))  # redirect to refresh page cleanly

if __name__ == '__main__':
    app.run(debug=True)
