import requests

ALL_FEATURES_ENDPOINT = "https://api.github.com/repos/fyrd/caniuse/contents/features-json"


class FeatureService(object):

    endpoint = None
    data = []
    endpoints = {}

    def __init__(self, root_endpoint=ALL_FEATURES_ENDPOINT):
        self.endpoint = root_endpoint

    def load(self):
        r = requests.get(self.endpoint)
        self.parse(r.json())

    def parse(self, data):
        self.data = data
        for item in data:
            slug = item.get('name').split('.json')[0]
            self.endpoints[slug] = item.get('download_url')

    def get_feature(self, slug):
        url = self.endpoints.get(slug)
        if url:
            feature = FeatureModel(url)
            return feature.load()
        return None

    def search(self, query):
        url = self.query_to_end_point(query)
        if url:
            feature = FeatureModel(url)
            feature.load()
            return feature
        return None

    # todo make query parser an instance property
    # todo set map on parse
    # todo move this and a "map" property into query parser
    def query_to_end_point(self, query):
        qp = QueryParser
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
        # 3rd try prepend "css-''
        endpoint = self.endpoints.get(qp.prepend(slugified, 'css'))
        if endpoint:
            return endpoint
        # 4th try prepend "css3-''
        endpoint = self.endpoints.get(qp.prepend(slugified, 'css3'))
        if endpoint:
            return endpoint
        # Try removing dashes
        condensed = qp.condense(query)
        endpoint = self.endpoints.get(condensed)
        if endpoint:
            return endpoint
        endpoint = self.endpoints.get(qp.prepend(condensed, 'css'))
        if endpoint:
            return endpoint
        endpoint = self.endpoints.get(qp.prepend(condensed, 'css3'))
        if endpoint:
            return endpoint

        # finally, give up...
        return None


class QueryParser(object):

    @staticmethod
    def prep(val):
        return " ".join(val.lower().strip().split('+'))

    @staticmethod
    def slugify(val):
        return '-'.join(val.split())

    @staticmethod
    def prepend(val, prefix):
        return '-'.join([prefix, val])

    @staticmethod
    def condense(val):
        return ''.join(val.split())


class FeatureModel(object):

    # todo endpoint constant
    # todo build endpoint with slug interpolated into constant

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
