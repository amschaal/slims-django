from django.conf import settings
CREATE_URL = settings.BIOSHARE_BASE_URL + '/bioshare/api/shares/create/'
GET_URL = settings.BIOSHARE_BASE_URL + '/bioshare/api/shares/{id}/'
VIEW_URL = settings.BIOSHARE_BASE_URL + '/bioshare/view/{id}/'
GET_PERMISSIONS_URL = settings.BIOSHARE_BASE_URL + '/bioshare/api/get_permissions/{id}'
SET_PERMISSIONS_URL = settings.BIOSHARE_BASE_URL + '/bioshare/api/set_permissions/{id}'
SYMLINK_URL = settings.BIOSHARE_BASE_URL + '/bioshare/create_symlink/{id}/'
DEFAULT_GROUP = getattr(settings,'BIOSHARE_DEFAULT_GROUP',None)
AUTH_TOKEN = settings.BIOSHARE_TOKEN
FILESYSTEM_ID = settings.BIOSHARE_FILESYSTEM_ID
TEST = settings.BIOSHARE_TEST