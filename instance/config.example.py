# Development Settings
DEBUG = False
HOST = "127.0.0.1"
PORT = "5000"

# Application Settings
SECRET_KEY = "changeme"
SESSION_TYPE = "redis"

SQLALCHEMY_DATABASE_URI = 'postgresql://crapi@localhost/crapi'
SQLALCHEMY_TRACK_MODIFICATIONS = False

DISCORD_CLIENT_ID = ""
DISCORD_CLIENT_SECRET = ""
DISCORD_REDIRECT_URI = "https://crapi.localhost/auth/login/callback"
DISCORD_GUILD_ID = "280298381807714304"
