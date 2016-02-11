from flask import Flask, request, jsonify, abort
from features import FeatureService

app = Flask(__name__)
features = FeatureService()


@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error=404, text=str(e)), 404


@app.route('/')
def index():
    return "The Can I Use API!"


@app.route('/api/features', methods=['GET'])
def api_all_features():
    return jsonify({'features': features.qp.map})


@app.route('/api/features/data', methods=['GET'])
def api_all_features_data():
    return jsonify({'data': features.config})


@app.route('/api/features/search', methods=['GET'])
def api_feature_search():
    query = request.args.get('q', '')
    feature = features.search(query)
    if feature:
        return jsonify(feature.data)
    return abort(404, {'errors': dict(message="feature %r not found" % query)})


@app.route('/api/features/<string:slug>', methods=['GET'])
def api_get_feature(slug):
    feature = features.get_feature(slug)
    if feature:
        return jsonify(feature.data)
    else:
        return abort(404, {'errors': dict(message="feature not found")})


if __name__ == '__main__':
    features.load()
    # app.debug = True
    app.run()
