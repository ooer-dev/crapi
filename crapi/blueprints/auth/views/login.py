from flask import current_app, flash, get_flashed_messages, redirect, render_template, request, url_for
from flask_login import current_user, login_user
from flask_wtf.csrf import generate_csrf, validate_csrf
from itsdangerous import BadData

from crapi.blueprints.auth import blueprint
from crapi.blueprints.auth.util import DISCORD_AUTHORIZATION_URL, DISCORD_TOKEN_URL, authenticate_user, \
    is_safe_url, make_serializer, make_session, redirect_back


def generate_state():
    state_data = {'csrf': generate_csrf()}

    next_url = request.args.get('next')
    if is_safe_url(next_url):
        state_data['next'] = next_url

    s = make_serializer()

    return s.dumps(state_data)


@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect_back()

    state = generate_state()
    discord = make_session()
    authorization_url, _ = discord.authorization_url(DISCORD_AUTHORIZATION_URL, state)

    if get_flashed_messages(category_filter=['danger']):
        return render_template('auth/login.html', url=authorization_url)

    return redirect(authorization_url)


@blueprint.route('/login/callback')
def login_callback():
    if current_user.is_authenticated:
        return redirect_back()

    def _handle_error(error: str = ''):
        reasons = {
            'access_denied': 'You did not approve access to your Discord account.',
            'no_guild': 'You are not a member of r/Ooer.',
            'no_guild_admin': 'You are not an administrator of r/Ooer.',
        }

        flash(
            "Couldn't log in. " + reasons.get(error, 'An unknown error occurred.'),
            category='danger'
        )

        if is_safe_url(next_url):
            return redirect(url_for('auth.login', next=next_url))
        else:
            return redirect(url_for('auth.login'))

    try:
        s = make_serializer()
        state_data = s.loads(request.args.get('state'), max_age=300)
        validate_csrf(state_data.get('csrf'))
    except BadData:
        return _handle_error()

    next_url = state_data.get('next')

    if 'error' in request.args:
        return _handle_error(request.args['error'])

    if 'code' not in request.args:
        return _handle_error()

    discord = make_session()

    try:
        discord.fetch_token(
            DISCORD_TOKEN_URL,
            client_secret=current_app.config.get('DISCORD_CLIENT_SECRET'),
            code=request.args.get('code'),
        )
    except Exception:
        return _handle_error()

    discord_user = discord.get('https://discord.com/api/users/@me').json()
    guilds = discord.get('https://discord.com/api/users/@me/guilds').json()

    guild_id = current_app.config.get('DISCORD_GUILD_ID')
    guild = next((g for g in guilds if g['id'] == guild_id), None)
    if not guild:
        return _handle_error('no_guild')

    permissions = int(guild['permissions'])
    if (permissions & 0x8) != 0x8:
        return _handle_error('no_guild_admin')

    user = authenticate_user(discord_user)

    if not login_user(user, remember=True):
        return _handle_error()

    flash('Logged in!', category='success')
    return redirect_back(next_url)
