from flask import Flask, render_template, request, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os

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

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Configuration pour Railway
if os.getenv('RAILWAY_ENVIRONMENT'):
    app.config['SERVER_NAME'] = 'mystartup-production.up.railway.app'
    app.config['PREFERRED_URL_SCHEME'] = 'https'

# OAuth Google
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/',
    userinfo_endpoint='https://www.googleapis.com/oauth2/v3/userinfo',  # ✅ indispensable
    client_kwargs={
        'scope': 'email profile'  # ✅ PAS "openid"
    }
)



@app.route('/', methods=['GET', 'POST'])
def index():
    summary = None
    topics = None
    emotions = None
    emotion_labels = []
    emotion_values = []
    history = load_history()

    if request.method == 'POST':
        if 'email' not in session:
            return redirect(url_for('login'))  # demande login si non connecté

        video_url = request.form['youtube_url']
        video_id = extract_video_id(video_url)
        try:
            video_title, thumbnail_url = get_video_info(video_id)
        except Exception as e:
            video_title, thumbnail_url = "Unknown video", None

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
    return redirect(url_for('index'))

@app.route('/login')
def login():
    # Pour Railway, on force l'URL HTTPS
    redirect_uri = "https://mystartup-production.up.railway.app/auth"
    print("REDIRECT URI FOR GOOGLE:", redirect_uri)
    return google.authorize_redirect(redirect_uri)


@app.route('/auth')
def auth():
    token = google.authorize_access_token()
    print("TOKEN:", token)  # 🪵 pour debug
    resp = google.get('oauth2/v3/userinfo')
    print("USERINFO RAW:", resp.text)  # 🪵 affiche le contenu brut

    try:
        user_info = resp.json()
    except Exception as e:
        return f"Erreur lors du décodage JSON: {resp.text}", 500

    session['email'] = user_info['email']
    session['name'] = user_info.get('name')
    session['picture'] = user_info.get('picture')
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('name', None)
    session.pop('picture', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)


