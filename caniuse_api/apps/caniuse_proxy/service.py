import requests
from flask import current_app
from caniuse_api.apps.caniuse_proxy.util import QueryParser
from caniuse_api.apps.caniuse_proxy.model import FeatureModel

CONFIG_ENDPOINT = "https://api.github.com/repos/" \
                  "fyrd/caniuse/contents/features-json"


class FeatureService(object):

    @staticmethod
    def get_instance():
        try:
            return FeatureService.__instance
        except AttributeError:
            current_app.logger.info('initializing feature service')
            FeatureService.__instance = FeatureService()
            FeatureService.__instance.load()
        return FeatureService.__instance

    endpoint = None
    qp = None

    def __init__(self, config_endpoint=CONFIG_ENDPOINT):
        self.endpoint = config_endpoint
        self.qp = QueryParser(['css', 'css3'], ['2d'])

    def load(self, config_endpoint=None):
        endpoint = config_endpoint or self.endpoint
        try:
            r = requests.get(endpoint)
            self.parse(r.json())
            return True
        except requests.exceptions.RequestException as e:
            current_app.logger.error(
                'Error loading config for FeatureService: %r' %
                e.message
            )
            return False

    def parse(self, data):
        try:
            for item in data:
                slug = item.get('name').split('.json')[0]
                self.qp.add_valid_slug(slug)
        except AttributeError as e:
            current_app.logger.error(
                'Error parsing config for FeatureService: %r' %
                e.message
            )
            current_app.logger.error(e.message)

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
