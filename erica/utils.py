from urllib.parse import parse_qs, urlparse


def get_param(url, param):
    query_string = urlparse(url).query

    params = parse_qs(query_string)
    if param in params:
        return params[param][0]
