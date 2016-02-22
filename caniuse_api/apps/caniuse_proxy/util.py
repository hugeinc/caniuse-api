
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
