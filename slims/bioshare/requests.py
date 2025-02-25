import re
import urllib, json
from django.conf import settings
from .config import CREATE_URL, GET_URL
def bioshare_request(url, token, data=None):
    print('bioshare url', url, 'token', token)
    params = json.dumps(data).encode('utf8')
    if data:
        req = urllib.request.Request(url, data=params)
    else:
        req = urllib.request.Request(url)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', 'Token {}'.format(token))
    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            data = json.load(response)
            return data
        else:
            raise Exception('API error')
    except urllib.request.HTTPError as e:
        error_message = e.read()
        raise Exception(error_message)

def parse_share_id(url):
    SHARE_REGEX = r'^https?:\/\/.+\/bioshare\/view\/(?P<share>[a-zA-Z0-9]{15})\/?$'
    matches = re.match(SHARE_REGEX, url)
    if not matches:
        return None
    return matches[1]

def bioshare_post(url, token, data):
    return bioshare_request(url, token, data)

def bioshare_get(url, token):
    return bioshare_request(url, token)

def get_share(token, id):
    url = GET_URL.format(id=id)
    return bioshare_get(url, token)

def create_share(token, name, description=None, filesystem=None):
        description = description or 'Genome Center LIMS generated share'
        params = {"name":name,"notes":description,'read_only':False}
        if filesystem:
            params['filesystem'] = filesystem
        return bioshare_post(CREATE_URL, token, params)['id']