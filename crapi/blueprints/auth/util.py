from urllib.parse import urljoin, urlparse

from flask import current_app, redirect, request
from itsdangerous import URLSafeTimedSerializer
from requests_oauthlib import OAuth2Session

from crapi.models import db
from crapi.models.user import User


DISCORD_AUTHORIZATION_URL = 'https://discord.com/api/oauth2/authorize'
DISCORD_TOKEN_URL = 'https://discord.com/api/oauth2/token'


def make_serializer() -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(
        current_app.config.get('SECRET_KEY', 'ohmaniamnotgoodwithsecretplstohelp'),
        salt='ohmaniamnotgoodwithcomputerplstohelp'
    )


def make_session(token=None) -> OAuth2Session:
    return OAuth2Session(
        client_id=current_app.config.get('DISCORD_CLIENT_ID'),
        token=token,
        scope=['identify', 'guilds'],
        redirect_uri=current_app.config.get('DISCORD_REDIRECT_URI'),
    )


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(next_url=None):
    if not next_url:
        next_url = request.args.get('next', '/')

    if is_safe_url(next_url):
        return redirect(next_url)
    else:
        return redirect('/')


def authenticate_user(discord_user):
    discord_user_id = int(discord_user['id'])

    user = User.query.filter_by(discord_id=discord_user_id).first()

    if not user:
        user = User(discord_id=discord_user_id)

    user.username = discord_user['username'] + '#' + discord_user['discriminator']
    db.session.add(user)
    db.session.commit()

    return user
