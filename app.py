from flask import Flask, request, redirect, session
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'

CLIENT_KEY = 'awyp3dlvxjvvh26j'
CLIENT_SECRET = '0FM8tRF7MogEUZZLr26NKdQfK9ExnFQj'
REDIRECT_URI = 'your_redirect_uri'

@app.route('/')
def index():
    return '<a href="/login">Login with TikTok</a>'

@app.route('/login')
def login():
    auth_url = f"https://www.tiktok.com/v2/auth/authorize/?client_key={CLIENT_KEY}&response_type=code&scope=user.info.basic,video.list&redirect_uri={REDIRECT_URI}&state=your_state"
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_url = 'https://open.tiktokapis.com/v2/oauth/token/'
    data = {
        'client_key': CLIENT_KEY,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI
    }
    response = requests.post(token_url, data=data)
    access_token = response.json().get('access_token')
    session['access_token'] = access_token
    return redirect('/profile')

@app.route('/profile')
def profile():
    access_token = session.get('access_token')
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    user_info_url = 'https://open.tiktokapis.com/v2/user/info/'
    user_info_response = requests.get(
        user_info_url, headers=headers)
