"""
HMAC Azure Auth plugin for HTTPie.
"""
import datetime
import base64
import hashlib
import hmac
import traceback

from httpie.plugins import AuthPlugin

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

__version__ = '1.0.0'
__author__ = 'Andrew Peacock'
__licence__ = 'MIT'

class HmacAuth:
    def __init__(self, password, algorithm='hmac-sha256',
                 headers=['request-line', 'date'], charset='utf-8'):
        self.password = password
        self.algorithm = algorithm
        self.headers = headers
        self.charset = charset

        self.auth_template = 'HMAC-SHA256 SignedHeaders=date;host;x-ms-content-sha256&Signature={}'

    def __call__(self, r):
        try:

            # add Date header
            if 'date' in self.headers and 'Date' not in r.headers:
                r.headers['Date'] = self.create_date_header()

            # add content header
            r.headers['x-ms-content-sha256'] = self.get_content_hash(r)
            if 'x-ms-content-sha256' not in self.headers:
                self.headers.append('x-ms-content-sha256')

            # get signature
            signature = self.get_signature(r)
            r.headers['Authorization'] = self.auth_template.format(signature)

            return r
        except:
            traceback.print_exc()

    def create_date_header(self):
        now = datetime.datetime.utcnow()
        return now.strftime('%a, %d %b %Y %H:%M:%S GMT')

    def get_content_hash(self, r):
        if r.body:
            if isinstance(r.body, bytes):
                hashed_body = hashlib.sha256(r.body)
            else:
                hashed_body = hashlib.sha256(r.body.encode(self.charset))
        else:
            hashed_body = hashlib.sha256("".encode(self.charset))

        return base64.b64encode(hashed_body.digest()).decode(self.charset)

    def get_signature(self, r):
        method = r.method

        url = urlparse(r.url)
        path_and_query = url.path + '?' + url.query
        host = url.hostname

        date = r.headers.get('Date')
        if not date:
            return ""

        content_hash = r.headers.get('x-ms-content-sha256')
        if not content_hash:
            return ""

        headers_string = date + ";" + host + ";" + content_hash
        string_to_sign = '\n'.join([method, path_and_query, headers_string])

        digest = hmac.new(base64.b64decode(self.password), string_to_sign.encode(self.charset), hashlib.sha256).digest()
        return base64.b64encode(digest).rstrip().decode(self.charset)

class HmacAuthPlugin(AuthPlugin):

    name = 'HMAC Azure auth'
    auth_type = 'azure-hmac'
    description = 'Sign requests using the Azure Communication Service specified HMAC authentication scheme'

    def get_auth(self, username=None, password=None):
        return HmacAuth(password)

