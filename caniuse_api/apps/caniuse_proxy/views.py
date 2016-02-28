from flask import request, jsonify, abort, Blueprint
from caniuse_api.apps.caniuse_proxy.service import FeatureService


proxy_blueprint = Blueprint(
    'caniuse_api_proxy',
    __name__,
    template_folder='templates'
)


@proxy_blueprint.route('/', methods=['GET'])
def all_proxy_features():
    features = FeatureService.get_instance()
    return jsonify({
        'features': features.qp.valid_slugs
    })


@proxy_blueprint.route('/search', methods=['GET'])
def search_proxy_features():
    query = request.args.get('q', '')
    features = FeatureService.get_instance()
    feature = features.search(query)
    if feature and feature.data:
        return jsonify(feature.data)
    return abort(404, {
        'errors': dict(message="feature %r not found" % query)
    })


@proxy_blueprint.route('/<string:slug>', methods=['GET'])
def feature_proxy(slug):
    features = FeatureService.get_instance()
    feature = features.get_feature(slug)
    if feature and feature.data:
        return jsonify(feature.data)
    else:
        return abort(404, {
            'errors': dict(message="feature not found")
        })


@proxy_blueprint.errorhandler(404)
def not_authorized(e):
    resp = jsonify(
        errors=[{
            'status': 404,
            'title': 'Feature Not Found',
            'detail': str(e),
        }]
    )
    resp.status_code = 404
    return resp
