from flask import Flask, request, jsonify, abort
from features import FeatureMap, FeatureModel

app = Flask(__name__)
allFeatures = FeatureMap()


@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error=404, text=str(e)), 404

@app.route('/')
def index():
	return "The Can I Use API!"

@app.route('/api/features/data', methods=['GET'])
def apiAllFeaturesData():
	return jsonify({'data':allFeatures.data})

@app.route('/api/features/all', methods=['GET'])
def apiAllFeatures():
	return jsonify({'data':allFeatures.endpoints})

@app.route('/api/features/search', methods=['GET'])
def apiFeatureSearch():
	query = request.args.get('q')
	endpoint = allFeatures.search(query)
	if (endpoint):
		feature = FeatureModel(endpoint)
		feature.load()
		return jsonify(feature.data)

	return abort(404, {'errors':dict(message="feature %r not found" % query)})

@app.route('/api/features/<string:slug>', methods=['GET'])
def apiGetFeature(slug):
	feature = allFeatures.getFeature(slug)
	if (feature):
		return jsonify(feature)
	else:
		return abort(404, {'errors':dict(message="feature not found")})

if __name__ == '__main__':
	allFeatures.load()
	app.debug = True
	app.run()