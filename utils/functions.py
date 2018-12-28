import random

from functools import wraps

from flask import session, redirect, url_for


def get_sqlalche_uri(DATABASE):
    user = DATABASE['USER']
    name = DATABASE['NAME']
    password = DATABASE['PASSWORD']
    host = DATABASE['HOST']
    port = DATABASE['PORT']
    driver = DATABASE['DRIVER']
    engine = DATABASE['ENGINE']
    return '%s+%s://%s:%s@%s:%s/%s' % (engine, driver, user, password, host, port, name)


def get_generateCode():
    strs = 'qwertyuiopasdfghjklzxcvbnm1234567890'
    code = ''
    for _ in range(0,4):
        code += random.choice(strs)
    return code


def is_login(func):
    @wraps(func)
    def login_status(*args, **kwargs):
        try:
            if not session['user_id']:
                return redirect(url_for('user.login'))
            return func(*args, **kwargs)
        except:
            return redirect(url_for('user.login'))
    return login_status



