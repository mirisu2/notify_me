from os import environ

from flask import Flask, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_redis import FlaskRedis

app = Flask(__name__)
app.config['DEBUG'] = environ.get('DEBUG')
app.config['ENV'] = environ.get('ENV')
app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
app.config['REDIS_URL'] = environ.get('REDIS_URL')
app.config['ALLOWED_TOKENS'] = environ.get('ALLOWED_TOKENS')
app.config['CHANNEL'] = environ.get('CHANNEL')
redis_client = FlaskRedis(app)


limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=[],
    headers_enabled=True,
    strategy='fixed-window-elastic-expiry'
)


@limiter.request_filter
def ip_whitelist():
    return request.remote_addr == "127.0.0.1"


from app.api import email
from app.api import telegram


limiter.limit("10 per second")(email.bp)
limiter.limit("10 per second")(telegram.bp)

app.register_blueprint(email.bp)
app.register_blueprint(telegram.bp)


@app.route("/ping")
@limiter.limit("5 per minute", override_defaults=False)
def ping():
    return "PONG"
