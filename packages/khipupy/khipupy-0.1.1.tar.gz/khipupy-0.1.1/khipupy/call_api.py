from .header_signature import header_signature
from .settings import (
    KHIPU_HEADER,
    AUTHORIZED_HTTP_METHODS,
    API_METHODS,
)


def call_api(url, secret, receiver_id, data={}, method='get', extra=''):
    api_response = {
        'response': '',
        'status': 400
    }
    kiphu_endpoint = '{0}{1}'.format(url, extra)
    formatted_header = KHIPU_HEADER.copy()
    signature = header_signature(
        method=method,
        url=kiphu_endpoint,
        params=data,
        secret=secret,
        receiver_id=receiver_id,
    )
    formatted_header['Authorization'] = signature

    request_config = {
        'url': kiphu_endpoint,
        'params': data,
        'headers': formatted_header,
    }

    method_called = method.lower()

    if method_called in AUTHORIZED_HTTP_METHODS:
        response = API_METHODS[method_called](request_config)

        api_response['response'] = response.json()
        api_response['status'] = response.status_code

    else:
        api_response['response'] = {
            'message': 'metodo no reconocido, solo se permite GET, POST y DELETE'
        }

    return api_response
