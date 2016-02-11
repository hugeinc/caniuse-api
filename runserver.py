from flask import Flask, request, jsonify, abort
from features import FeatureService, FeatureModel

app = Flask(__name__)
features = FeatureService()


@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error=404, text=str(e)), 404


@app.route('/')
def index():
	return "The Can I Use API!"


@app.route('/api/features/data', methods=['GET'])
def apiAllFeaturesData():
	return jsonify({'data': features.data})


@app.route('/api/features/all', methods=['GET'])
def apiAllFeatures():
	return jsonify({'data': features.endpoints})


@app.route('/api/features/search', methods=['GET'])
def apiFeatureSearch():
	query = request.args.get('q')
	feature = features.search(query)
	if (feature):
		return jsonify(feature.data)
	return abort(404, {'errors':dict(message="feature %r not found" % query)})


@app.route('/api/features/<string:slug>', methods=['GET'])
def apiGetFeature(slug):
	feature = features.getFeature(slug)
	if (feature):
		return jsonify(feature)
	else:
		return abort(404, {'errors':dict(message="feature not found")})

if __name__ == '__main__':
	features.load()
	#app.debug = True
	app.run()