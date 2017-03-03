from utils import log
from utils import error
from utils import template
from utils import redirect
from utils import http_response
from routes.routes_user import current_user
from routes.routes_user import login_required

from models import Weibo


def index(request):
    weibo_list = Weibo.all()
    # for w in weibo_list:
    #     w.comments()
    #     w.user()
    body = template('weibo_index.html', weibos=weibo_list)
    return http_response(body)


def detail(request):
    u = current_user(request)
    weibo_list = Weibo.find_all(user_id=u.id)
    body = template('weibo_detail.html', weibos=weibo_list)
    return http_response(body)


def edit(request):
    weibo_id = int(request.query.get('id', -1))
    w = Weibo.find_by(id=weibo_id)
    u = current_user(request)
    if w.user_id != u.id:
        return error(request)
    body = template('weibo_edit.html', weibo=w)
    return http_response(body)


def add(request):
    u = current_user(request)
    form = request.form()
    w = Weibo(form)
    w.user_id = u.id
    w.created_time = w.change_time()
    w.save()
    return redirect('/weibo')


def update(request):
    weibo_id = int(request.query.get('id', -1))
    w = Weibo.find_by(id=weibo_id)
    u = current_user(request)
    if w.user_id != u.id:
        return error(request)
    form = request.form()
    w.content = form.get('content')
    w.save()
    return redirect('/weibo/detail')


def delete(request):
    weibo_id = int(request.query.get('id', -1))
    w = Weibo.find_by(id=weibo_id)
    u = current_user(request)
    if w.user_id != u.id:
        return error(request)
    Weibo.delete(weibo_id)
    return redirect('/weibo/detail')


route_dict = {
    '/weibo': login_required(index),
    '/weibo/detail': login_required(detail),
    '/weibo/add': login_required(add),
    '/weibo/edit': login_required(edit),
    '/weibo/update': login_required(update),
    '/weibo/delete': login_required(delete),
}
