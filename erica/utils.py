from urllib.parse import parse_qs, urlparse


def get_param(url, param):
    """
    Returns the parameter value of param inside the url query.
    :param url: the url.
    :param param: the param to look for.
    :return: the first parameter value matching param key if it exists, None otherwise.
    """
    query_string = urlparse(url).query

    params = parse_qs(query_string)
    if param in params:
        return params[param][0]
