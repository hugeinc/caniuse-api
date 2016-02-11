import requests

CONFIG_ENDPOINT = "https://api.github.com/repos/fyrd/caniuse/contents/features-json"
FEATURE_ENDPOINT = "https://raw.githubusercontent.com/Fyrd/caniuse/master/features-json/%s.json"


class FeatureService(object):
    endpoint = None
    qp = None
    config = []

    def __init__(self, config_endpoint=CONFIG_ENDPOINT):
        self.endpoint = config_endpoint
        self.qp = QueryParser()

    def load(self):
        r = requests.get(self.endpoint)
        self.parse(r.json())

    def parse(self, data):
        self.config = data
        for item in data:
            slug = item.get('name').split('.json')[0]
            self.qp.map.append(slug)

    def get_feature(self, slug):
        if slug in self.qp.map:
            feature = FeatureModel(slug)
            feature.load()
            return feature
        return None

    def search(self, query):
        slug = self.qp.get_slug(query)
        if slug:
            feature = FeatureModel(slug)
            feature.load()
            return feature
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

    map = []

    def get_slug(self, query):

        query = QueryParser.prep(query)
        formats = [query, QueryParser.slugify(query), QueryParser.condense(query)]

        for formatted in formats:

            if formatted in self.map:
                return formatted

            if QueryParser.prepend(formatted, 'css') in self.map:
                return QueryParser.prepend(formatted, 'css')

            if QueryParser.prepend(formatted, 'css3') in self.map:
                return QueryParser.prepend(formatted, 'css3')

        return None


class FeatureModel(object):

    data = []
    endpoint = None
    slug = None

    def __init__(self, slug):
        self.endpoint = FEATURE_ENDPOINT % slug

    def load(self):
        r = requests.get(self.endpoint)
        self.parse(r.json())
        return self.data

    def parse(self, data):
        self.data = data
