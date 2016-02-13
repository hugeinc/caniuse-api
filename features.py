import requests

CONFIG_ENDPOINT = "https://api.github.com/repos/fyrd/caniuse/contents/features-json"
FEATURE_ENDPOINT = "https://raw.githubusercontent.com/Fyrd/caniuse/master/features-json/%s.json"


class FeatureService(object):

    endpoint = None
    qp = None
    config = []

    def __init__(self, config_endpoint=CONFIG_ENDPOINT):
        self.endpoint = config_endpoint
        self.qp = QueryParser(['css', 'css3'])

    def load(self):
        r = requests.get(self.endpoint)
        self.parse(r.json())

    def parse(self, data):
        self.config = data
        for item in data:
            slug = item.get('name').split('.json')[0]
            self.qp.add_valid_slug(slug)

    def get_feature(self, slug):
        if self.qp.is_valid_slug(slug):
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
        return " ".join((" ".join(val.split())).lower().split('+'))

    @staticmethod
    def slugify(val):
        return '-'.join(val.split())

    @staticmethod
    def prepend(val, prefix):
        return '-'.join([prefix, val])

    @staticmethod
    def condense(val):
        return ''.join(val.split())

    map = {}
    prefixes = None
    valid_slugs = None

    def __init__(self, prefixes=[], valid_slugs=[]):
        self.prefixes = prefixes
        self.valid_slugs = valid_slugs

    def add_valid_slug(self, slug):
        if slug not in self.valid_slugs:
            self.valid_slugs.append(slug)
            # todo add a dict called "map"
            # todo covert slug to dashless, spaceless, un-prefixed string
            # todo key prepped queries in dict, "map" against valid slugs
            # todo refactor search to use this

    def get_slug(self, query):

        query = QueryParser.prep(query)
        formats = [query, QueryParser.slugify(query), QueryParser.condense(query)]

        for formatted in formats:
            if formatted in self.valid_slugs:
                return formatted
            for prefix in self.prefixes:
                prefixed = QueryParser.prepend(formatted, prefix)
                if prefixed in self.valid_slugs:
                    return prefixed
        return None

    def is_valid_slug(self, slug):
        return slug in self.valid_slugs


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
