import re
import urllib.request, json
from django.conf import settings
from .settings import CREATE_URL, GET_URL, AUTH_TOKEN, SYMLINK_URL

def bioshare_request(url, token=AUTH_TOKEN, data=None):
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

def bioshare_post(url, data):
    return bioshare_request(url, AUTH_TOKEN, data)

def bioshare_get(url):
    return bioshare_request(url, AUTH_TOKEN)

def get_share(id):
    url = GET_URL.format(id=id)
    return bioshare_get(url)

def create_share(name, description=None, filesystem=None):
        description = description or 'Genome Center LIMS generated share'
        params = {"name":name,"notes":description,'read_only':False}
        if filesystem:
            params['filesystem'] = filesystem
        return bioshare_post(CREATE_URL, params)['id']

def link_data(share_id, target, share_path):
        url = SYMLINK_URL.format(id=share_id)
        params = {"name":share_path,"target":target}
        # try:
        return bioshare_post(url, params)
        # except Exception as e:
        #      print(e)