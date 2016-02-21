from flask import Flask, request, jsonify, abort
from features import FeatureService
from hipchat import ICanHazBot
from flask.ext.markdown import Markdown

app = Flask(__name__, template_folder="templates")
Markdown(app)

features = FeatureService()


@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error=404, text=str(e)), 404


@app.route('/')
def index():
    return "The Can I Use API!"


@app.route('/api/features/', methods=['GET'])
def api_all_features():
    return jsonify({'features': features.qp.valid_slugs})


@app.route('/api/features/search', methods=['GET'])
def api_feature_search():
    query = request.args.get('q', '')
    feature = features.search(query)
    if feature and feature.data:
        return jsonify(feature.data)
    return abort(404, {'errors': dict(message="feature %r not found" % query)})


@app.route('/api/features/<string:slug>', methods=['GET'])
def api_get_feature(slug):
    feature = features.get_feature(slug)
    if feature and feature.data:
        return jsonify(feature.data)
    else:
        return abort(404, {'errors': dict(message="feature not found")})


@app.route('/api/features/hipchat', methods=['POST'])
def api_hip_chat():
    bot = ICanHazBot(features)
    response = bot.parse_request(request.get_json())
    return jsonify(response.data)


if __name__ == '__main__':
    features.load()
    # app.debug = True
    app.run()
