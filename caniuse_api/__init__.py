from flask import Flask
from flask.ext.markdown import Markdown
from caniuse_api.apps.core.views import main_blueprint

app = Flask(__name__)
Markdown(app)
app.config.from_object('caniuse_api.settings.local')
app.register_blueprint(main_blueprint)
