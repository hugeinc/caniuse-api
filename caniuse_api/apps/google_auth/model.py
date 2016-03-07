import json
from urllib2 import Request, urlopen, URLError


class TokenInvalid(Exception):
    pass


class User(object):

    first = ''
    last = ''
    name = ''
    email = ''
    google_id = ''
    profile_pic = ''

    def load(self, access_token):
        headers = {'Authorization': 'OAuth ' + access_token}
        req = Request(
            'https://www.googleapis.com/oauth2/v1/userinfo',
            None,
            headers
        )
        try:
            res = urlopen(req)
        except URLError as e:
            if e.code == 401:
                # token expired or bad token
                raise TokenInvalid()
            else:
                return res.read()
        data = res.read()
        self.parse(data)
        return data

    def parse(self, data):
        parsed = json.loads(data)
        self.first = parsed.get('given_name', '')
        self.last = parsed.get('family_name', '')
        self.name = parsed.get('name', ' '.join([self.first, self.last]))
        self.google_id = parsed.get('id', '')
        self.email = parsed.get('email', '')
        self.profile_pic = parsed.get('picture', '')
        return parsed
