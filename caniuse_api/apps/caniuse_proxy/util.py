
def float_sem_ver(s):
    if '-' in s:
        return float_multiple_versions(s)
    try:
        digits = s.split('.')
        return float('.'.join([digits.pop(0), ''.join(digits)]))
    except ValueError:
        return None


def float_multiple_versions(s):
    lowest = s.split('-').pop(0)
    try:
        return float(lowest)
    except ValueError:
        return float_sem_ver(lowest)


def float_version(s):
    try:
        return float(s)
    except ValueError:
        return float_multiple_versions(s)


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
        """
        Minify a slug or query by stripping all dashes,
        spaces, prefixes and suffixes
        """
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
