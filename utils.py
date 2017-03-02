from jinja2 import Environment, FileSystemLoader
import os.path
import time

log_config = {}


def set_log_path():
    fmt = '%Y%m%d%H%M%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(fmt, value)
    log_config['file'] = 'logs/log{}.txt'.format(dt)


def log(*args, **kwargs):
    fmt = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(fmt, value)
    path = log_config.get('file')
    if path is None:
        set_log_path()
        path = log_config['file']
    with open(path, 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


path = '{}/templates/'.format(os.path.dirname(__file__))
loader = FileSystemLoader(path)
env = Environment(loader=loader)


def template(path, **kwargs):
    t = env.get_template(path)
    return t.render(**kwargs)


def redirect(location, headers=None):
    h = {
        'Content-Type': 'text/html',
    }
    if headers is not None:
        h.update(headers)
    h['Location'] = location
    header = response_with_headers(h, 302)
    r = header + '\r\n' + ''
    return r.encode(encoding='utf-8')


def response_with_headers(headers, status_code=200):
    header = 'HTTP/1.1 {} OK\r\n'.format(status_code)
    header += ''.join(['{}: {}\r\n'.format(k, v)
                       for k, v in headers.items()])
    return header


def http_response(body, headers=None):
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    if headers is not None:
        header += ''.join(['{}: {}\r\n'.format(k, v)
                           for k, v in headers.items()])
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def error(request, code=404):
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')
