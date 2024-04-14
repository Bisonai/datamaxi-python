import re
import uuid
import responses


def mock_http_response(
    method, uri, response_data, http_status=200, headers=None, body_data=""
):
    if headers is None:
        headers = {}

    def decorator(fn):
        @responses.activate
        def wrapper(*args, **kwargs):
            responses.add(
                method,
                re.compile(".*" + uri),
                json=response_data,
                body=body_data,
                status=http_status,
                headers=headers,
            )
            return fn(*args, **kwargs)

        return wrapper

    return decorator


def random_str() -> str:
    return uuid.uuid4().hex
