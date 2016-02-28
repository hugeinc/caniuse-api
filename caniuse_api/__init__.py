import os
from flask import Flask, render_template, jsonify
from flask.ext.markdown import Markdown
from caniuse_api.apps.core.views import main_blueprint
from caniuse_api.apps.caniuse_proxy.views import proxy_blueprint
from caniuse_api.apps.caniuse_bot.views import bot_blueprint
from caniuse_api.apps.google_auth.views import get_google_auth_blueprint

app = Flask(__name__)
Markdown(app)

if os.environ.get('IS_HEROKU', None):
    # reads config vars directly from .env
    app.config.from_object('caniuse_api.settings.heroku')
elif not app.config.from_envvar('CANIUSE_API_CFG', True):
    # DO NOT DEPLOY W/ LOCAL SETTINGS
    app.config.from_object('caniuse_api.settings.local')

app.register_blueprint(main_blueprint)
app.register_blueprint(proxy_blueprint, url_prefix='/api/features')
app.register_blueprint(bot_blueprint, url_prefix='/api/features')
app.register_blueprint(
    get_google_auth_blueprint(app.config),
    url_prefix='/auth/google'
)


@app.errorhandler(404)
def page_not_found(e):
    return render_template(
        'error.html',
        status_code=e.code,
        message="The page you're looking for could not be found."
    )


@app.errorhandler(401)
def not_authorized(e):
    resp = jsonify(
        errors=[{
            'status': 401,
            'title': 'Un Authorized',
            'detail': "This endpoint requires a valid API Token",
        }]
    )
    resp.status_code = 401
    return resp
