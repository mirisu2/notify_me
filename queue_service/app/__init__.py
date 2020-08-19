import logging
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

logger = logging.getLogger('__notify__')
ch_console = logging.StreamHandler()
ch_console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
ch_console.setFormatter(formatter)
logger.addHandler(ch_console)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=[],
    headers_enabled=True,
    strategy='fixed-window-elastic-expiry'
)
limiter.logger.addHandler(ch_console)


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
