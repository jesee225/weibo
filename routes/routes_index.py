from utils import template
from utils import http_response


def route_index(request):
    body = template('index.html')
    return http_response(body)


route_dict = {
    '/': route_index,
}
