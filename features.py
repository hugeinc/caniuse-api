import requests

ALL_FEATURES_ENDPOINT = "https://api.github.com/repos/fyrd/caniuse/contents/features-json"

class FeatureMap(object):

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
		# todo need to refactor this...	
		# 1st convert to lower case
		query = query.lower()
		result = self.endpoints.get(query)
		if result:
			return result
		# 2nd try replacing spaces with dashes
		query = "-".join(query.split(' '))
		result = self.endpoints.get(query)
		if result:
			return result
		# 3rd try prepending "css-''
		result = self.endpoints.get("css-" + query)
		if (result):
			return result
		# 4th try prepending "css3-''
		result = self.endpoints.get("css3-" + query)
		if (result):
			return result
		# Try removing dashes
		query = ''.join(query.split('-'))
		result = self.endpoints.get(query)
		if (result):
			return result
		# finally, give up...
		return None


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
