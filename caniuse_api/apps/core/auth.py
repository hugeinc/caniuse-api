from flask import request, current_app, abort, session, g


def validate_token(token):
    app_token = current_app.config.get('TOKEN')
    current_app.logger.info(
        'token: %r : %r', token, app_token
    )
    return token and token == app_token


def authorized(fn):
    def _wrap(*args, **kwargs):
        token = request.args.get('token')
        if not validate_token(token):
            current_app.logger.error('Unauthorized')
            abort(401)
            return None
        return fn(*args, **kwargs)
    return _wrap


def get_api_token():
    return session.get('api_token', None)


def logout_user():
    g.user = None
    session.pop('api_token', None)
    session.pop('access_token', None)
