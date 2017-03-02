from utils import log
from utils import error
from utils import template
from utils import redirect
from utils import http_response
from routes.routes_user import current_user
from routes.routes_user import login_required

from models import Comment
from models import Weibo


def new(request):
    weibo_id = int(request.query.get('id', -1))
    w = Weibo.find_by(id=weibo_id)
    body = template('comment_new.html', weibo=w)
    return http_response(body)


def add(request):
    u = current_user(request)
    form = request.form()
    c = Comment(form)
    c.user_id = u.id
    c.created_time = c.change_time()
    c.save()
    return redirect('/weibo')


def delete(request):
    comment_id = int(request.query.get('id', -1))
    c = Comment.find_by(id=comment_id)
    u = current_user(request)
    if c.user_id != u.id:
        return error(request)
    Comment.delete(comment_id)
    return redirect('/weibo/detail')


route_dict = {
    '/comment/new': login_required(new),
    '/comment/add': login_required(add),
    '/comment/delete': login_required(delete),
}
