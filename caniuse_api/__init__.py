from flask import Flask
from flask.ext.markdown import Markdown
from caniuse_api.apps.core.views import main_blueprint
from caniuse_api.apps.caniuse_proxy.views import proxy_blueprint
from caniuse_api.apps.caniuse_bot.views import bot_blueprint

app = Flask(__name__)
Markdown(app)

try:
    app.config.from_envvar('CANIUSE_API_SETTINGS')
except RuntimeError as e:
    app.config.from_object('caniuse_api.settings.local')

app.register_blueprint(main_blueprint)
app.register_blueprint(proxy_blueprint, url_prefix='/api/features')
app.register_blueprint(bot_blueprint, url_prefix='/api/features')
