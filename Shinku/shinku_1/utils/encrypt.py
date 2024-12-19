import hashlib
from django.conf import settings
def md5(data_string):
    hasher = hashlib.md5(settings.SECRET_KEY.encode('utf8'))
    hasher.update(data_string.encode('utf-8'))
    return hasher.hexdigest()