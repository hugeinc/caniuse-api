from flask import request, jsonify, abort, Blueprint, current_app
from caniuse_api.apps.caniuse_bot import CanIUseBot
from caniuse_api.apps.caniuse_proxy.service import FeatureService


main_blueprint = Blueprint(
    'main_blueprint',
    __name__,
    template_folder='templates'
)


@main_blueprint.errorhandler(404)
def page_not_found(e):
    return jsonify(error=404, text=str(e)), 404


@main_blueprint.route('/')
def index():
    current_app.logger.info('this works')
    return "The Can I Use API! Needs some HTML!"


@main_blueprint.route('/api/features/', methods=['GET'])
def api_all_features():
    features = FeatureService.get_instance()
    return jsonify({
        'features': features.qp.valid_slugs
    })


@main_blueprint.route('/api/features/search', methods=['GET'])
def api_feature_search():
    query = request.args.get('q', '')
    features = FeatureService.get_instance()
    feature = features.search(query)
    if feature and feature.data:
        return jsonify(feature.data)
    return abort(404, {
        'errors': dict(message="feature %r not found" % query)
    })


@main_blueprint.route('/api/features/<string:slug>', methods=['GET'])
def api_get_feature(slug):
    features = FeatureService.get_instance()
    feature = features.get_feature(slug)
    if feature and feature.data:
        return jsonify(feature.data)
    else:
        return abort(404, {
            'errors': dict(message="feature not found")
        })


@main_blueprint.route('/api/features/hipchat', methods=['POST'])
def api_hip_chat():
    features = FeatureService.get_instance()
    bot = CanIUseBot(features)
    response = bot.parse_request(request.get_json())
    return jsonify(response.data)

