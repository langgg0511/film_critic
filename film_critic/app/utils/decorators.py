from functools import wraps
from flask import abort
from flask_login import current_user


def admin_required(f):
    """
    管理员网页权限装饰器
    :param f:
    :return:
    """
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if not current_user.is_administrator:
            abort(403)
        return f(*args, **kwargs)
    return decorated_func
