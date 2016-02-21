import requests

CONFIG_ENDPOINT = "https://api.github.com/repos/fyrd/caniuse/contents/features-json"
FEATURE_ENDPOINT = "https://raw.githubusercontent.com/Fyrd/caniuse/master/features-json/%s.json"


class FeatureService(object):

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
        except requests.exceptions.RequestException as e:
            # todo log e through "app" once that's been refactored
            # todo consider loading offline data
            print e

    def parse(self, data):
        try:
            for item in data:
                slug = item.get('name').split('.json')[0]
                self.qp.add_valid_slug(slug)
        except AttributeError:
            # todo log parsing error through "app" once that's been refactored
            pass

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

    min_map = {}
    prefixes = None
    suffixes = None
    valid_slugs = None

    def __init__(self, prefixes=None, suffixes=None, valid_slugs=None):
        self.prefixes = prefixes or []
        self.suffixes = suffixes or []
        self.valid_slugs = valid_slugs or []

    def minify(self, s):
        """minifies a slug or query by stripping all dashes, spaces, prefixes and suffixes"""
        s = s.lower()
        to_remove = [None, '-', '+']
        for char in to_remove:
            s = ''.join(s.split(char))
        for prefix in self.prefixes:
            if prefix in s and s.index(prefix) == 0:
                s = s[len(prefix):]
        for suffix in self.suffixes:
            if suffix in s and s.index(suffix) == len(s) - len(suffix):
                s = s[:-1*len(suffix)]
        return s

    def add_valid_slug(self, slug):
        if slug not in self.valid_slugs:
            self.valid_slugs.append(slug)
            self.min_map[self.minify(slug)] = slug

    def get_slug(self, query):
        return self.min_map.get(self.minify(query))

    def is_valid_slug(self, slug):
        return slug in self.valid_slugs


class FeatureModel(object):

    @staticmethod
    def float_sem_ver(s):
        if '-' in s:
            return FeatureModel.float_multiple_versions(s)
        try:
            digits = s.split('.')
            return float('.'.join([digits.pop(0), ''.join(digits)]))
        except ValueError:
            return None

    @staticmethod
    def float_multiple_versions(s):
        lowest = s.split('-').pop(0)
        try:
            return float(lowest)
        except ValueError:
            return FeatureModel.float_sem_ver(lowest)

    @staticmethod
    def float_version(s):
        try:
            return float(s)
        except ValueError:
            return FeatureModel.float_multiple_versions(s)

    @staticmethod
    def parse_browser_stats(data):
        stat_map = {}
        for version, status in data.iteritems():
            current_stat = stat_map.get(status)
            if current_stat:
                if FeatureModel.float_version(version) < FeatureModel.float_version(current_stat):
                    stat_map[status] = version
            else:
                stat_map[status] = version
        return stat_map

    data = None
    support = {}
    endpoint = None
    slug = None

    def __init__(self, slug):
        self.endpoint = FEATURE_ENDPOINT % slug

    def load(self):
        try:
            r = requests.get(self.endpoint)
            self.parse(r.json())
        except requests.exceptions.RequestException as e:
            # todo log error through "app" once that's been refactored
            print e
        return self.data

    def parse(self, data):
        try:
            stats = data.get('stats').items()
            self.data = data
            for browser, stat in stats:
                self.support[browser] = FeatureModel.parse_browser_stats(stat)
        except AttributeError as e:
            # todo log parsing error through "app" once that's been refactored
            print e

    def get_min_support_by_flags(self, browser_id, flags):
        browser_support = self.support.get(browser_id)
        for flag in flags:
            version = browser_support.get(flag)
            if version:
                return version, []
            for key in browser_support.keys():
                if flag in key:
                    stripped_key, notes = self.get_version_notes_from_flag(key)
                    if stripped_key and stripped_key == flag:
                        return browser_support.get(key), notes
        return None, None

    def get_version_notes_from_flag(self, v_flag):
        try:
            notes_from_flag = v_flag[v_flag.index('#'):]
            flag = v_flag[0:v_flag.index(' #')]
            notes = []
            for note_i in ''.join(notes_from_flag.split('#')).split():
                notes.append({
                    'index': note_i,
                    'text': self.data.get('notes_by_num').get(note_i)
                })
            return flag, notes
        except ValueError:
            pass
        return v_flag, None

    def get_relevant_notes(self, browser_keys, flag_set):
        notes = []
        if self.data.get('notes'):
            notes.append({'index': None, 'text': self.data.get('notes')})
        for flags in flag_set:
            for browser_id in browser_keys:
                version, sup_notes = self.get_min_support_by_flags(browser_id, flags)
                for note in sup_notes or []:
                    if note not in notes:
                        notes.append(note)
        return notes
