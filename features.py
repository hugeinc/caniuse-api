import requests

ALL_FEATURES_ENDPOINT = "https://api.github.com/repos/fyrd/caniuse/contents/features-json"

class FeatureService(object):

	endpoint = None	
	data = []
	endpoints = {}

	def __init__(self, rootEndpoint=ALL_FEATURES_ENDPOINT):
		self.endpoint = rootEndpoint

	def load(self):
		r = requests.get(self.endpoint)
		self.parse(r.json())
		
	def parse(self, data):
		self.data = data
		for item in data:
			slug = item.get('name').split('.json')[0]
			self.endpoints[slug] = item.get('download_url')

	def getFeature(self, slug):
		url = self.endpoints.get(slug)
		if (url):
			feature = FeatureModel(url)
			return feature.load()
		return None

	def search(self, query):
		url = self.queryToEndPoint(query)
		if (url):
			feature = FeatureModel(url)
			feature.load()
			return feature
		return None

	def queryToEndPoint(self, query):
		qp = QueryParser()
		# 1st convert to lower case
		query = qp.prep(query)
		endpoint = self.endpoints.get(query)
		if endpoint:
			return endpoint
		# 2nd try replacing spaces with dashes
		slugified = qp.slugify(query)
		endpoint = self.endpoints.get(slugified)
		if endpoint:
			return endpoint
		# 3rd try prepending "css-''
		endpoint = self.endpoints.get(qp.prepend(slugified, 'css'))
		if (endpoint):
			return endpoint
		# 4th try prepending "css3-''
		endpoint = self.endpoints.get(qp.prepend(slugified, 'css3'))
		if (endpoint):
			return endpoint
		# Try removing dashes
		condensed = qp.condense(query)
		endpoint = self.endpoints.get(condensed)
		if (endpoint):
			return endpoint
		endpoint = self.endpoints.get(qp.prepend(condensed, 'css'))
		if (endpoint):
			return endpoint
		endpoint = self.endpoints.get(qp.prepend(condensed, 'css3'))
		if (endpoint):
			return endpoint

		# finally, give up...
		return None


class QueryParser(object):

	def prep(self, str):
		return " ".join(str.lower().strip().split('+'))

	def slugify(self, str):
		return '-'.join(str.split())

	def prepend(self, str, prefix):
		return '-'.join([prefix, str])

	def condense(self, str):
		return ''.join(str.split())


class FeatureModel(object):

	data = []
	endpoint = None

	def __init__(self, endpoint):
		self.endpoint = endpoint

	def load(self):
		r = requests.get(self.endpoint)
		self.parse(r.json())
		return self.data

	def parse(self, data):
		self.data = data
