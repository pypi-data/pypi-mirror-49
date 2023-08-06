import urllib.parse
import hashlib
import hmac


def header_signature(method, url, secret, receiver_id, params={}):
    keys = list(params.keys())
    keys.sort()

    string_to_sign = '{0}&{1}'.format(
        method.upper(),
        urllib.parse.quote(url.lower(), safe='')
    )

    for key in keys:
        string_to_sign = string_to_sign + '&{0}={1}'.format(
            urllib.parse.quote(key, safe=''),
            urllib.parse.quote(params[key], safe=''),
        )

    secret_bytes = bytes(secret, 'utf-8')
    sign_bytes = bytes(string_to_sign, 'utf-8')

    kiphu_hash = hmac.new(secret_bytes, sign_bytes, hashlib.sha256).hexdigest()
    signature = '{0}:{1}'.format(receiver_id, kiphu_hash)

    return signature
