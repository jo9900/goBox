# encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

if 'threading' in sys.modules:
    raise Exception('threading module loaded before patching!')

import gevent

if '__pypy__' in sys.builtin_module_names:
    from psycopg2cffi import compat
    compat.register()
from gevent import monkey

monkey.patch_all()

from psyco_gevent import make_psycopg_green
make_psycopg_green()

from bottle import Bottle, request, run, static_file, response, abort, template

import bottle
import jwt

app = Bottle()

import settings
from sqlalchemy.orm import sessionmaker
import requests
from models import *
from common import *
from datetime import datetime, timedelta

from tornado.template import Template
from sqlalchemy import literal, select, func, case, union_all, and_, null, or_

engine = create_engine('postgresql+psycopg2://%s:%s@%s/%s' % (settings.USER, settings.PASSWORD,
                                                              settings.DATA_HOST, settings.DATABASE), echo=True, client_encoding='utf8')
Session = sessionmaker(bind=engine)

bottle.debug(settings.DEBUG)
app.catchall = False
bottle.TEMPLATE_PATH.append(settings.TEMPLATE_PATH)


def token_auth(func):

    def wrapper(*args, **kwargs):
        try:
            token = request.headers.get("Token")
            if not token:
                raise Exception(u"必须传递令牌")
            data = jwt.decode(token, settings.secret)
            kwargs["access_level"] = data.get("access_level")
            kwargs["token"] = data.get("token")
            kwargs["set_of_book"] = data.get("set_of_book")
            kwargs["url"] = data.get("url")
            kwargs["user_name"] = data.get("user_name")
            return func(*args, **kwargs)
        except Exception as e:
            return {"state": 0, "errmsg": str(e)}
        
    return wrapper


@app.error(500)
def error500(error):
    response.set_header('Content-Type', 'text/plain; charset=utf-8')

    return unicode(error.body)


@app.route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root=settings.STATIC_PATH)


@app.route('/api/access_token')
def generate():
    try:
        token = request.headers.get("Token")
        url = request.params.get("url")
        set_of_book = request.params.get("set_of_book")
        user_name = request.params.get("user_name")
        if not url:
            raise Exception(u"必须传递url")
        if not set_of_book:
            raise Exception(u"必须传递账套号")
        if not user_name:
            raise Exception(u"必须传递用户名")
        if not token:
            return {"state": 0, "errmsg": u"必须传递token"}
        params = ObjectDict(security_key=settings.security_key)
        r = requests.get('%s/api/security_keys?action=has_security_key' % url, headers={"Token": token}, params=params)
        if not r.text or r.text == 'null':
            raise Exception("没有权限")
        result = r.json()
        result["token"] = token
        result["url"] = url
        result["set_of_book"] = set_of_book
        result["user_name"] = user_name
        data = jwt.encode(result, settings.secret)
        return {"state": 1, "token": data}
    except Exception as e:
        return {"state": 0, "errmsg": str(e)}


@app.route('/api/set_of_books')
@token_auth
def create_set_of_book(**kwargs):
    session = Session()
    try:
        access_level = kwargs.get("access_level")
        if not access_level & 1:
            raise Exception(u"没有访问级 查看")
        params = get_params(request)
        set_of_book = params.get("set_of_book")
        if not set_of_book:
            raise Exception(u"必须传递账套号")
        sob = session.query(SetOfBook).filter(SetOfBook.set_of_book == set_of_book).first()
        if not sob:
            raise Exception(u"账套配置 %s 不存在" % set_of_book)
        result = sob.to_dict()
        result["state"] = 1
        return result
    except Exception as e:
        return {"state": 0, "errmsg": str(e)}
    finally:
        session.close()


@app.route('/api/set_of_books/<id:int>', method='PUT')
@token_auth
def update_set_of_book(id, **kwargs):
    session = Session()
    try:
        access_level = kwargs.get("access_level")
        if not access_level & 2:
            raise Exception(u"没有访问级 编辑")
        user_name = kwargs.get("user_name")
        params = get_params(request)
        current = session.query(SetOfBook).get(id)
        if not current:
            raise Exception(u"账套配置不存在")
        app_key = params.get("app_key")
        if app_key:
            current.app_key = app_key
        if params.get("user_name"):
            current.user_name = params.get("user_name")
        access_token, expires = request_access_token(current)
        now = datetime.now()
        current.access_token = access_token
        current.token_created_at = now
        current.expired_at = now + timedelta(seconds=expires)
        current.updated_at = now
        current.updated_user = user_name
        result = current.to_dict()
        result["state"] = 1
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        return {"state": 0, "errmsg": str(e)}
    finally:
        session.close()


@app.route('/api/devices', method='POST')
@token_auth
def create_device(**kwargs):
    session = Session()
    try:
        access_level = kwargs.get("access_level")
        if not access_level & 4:
            raise Exception(u"没有访问级 新建")
        set_of_book = kwargs.get("set_of_book")
        user_name = kwargs.get("user_name")
        params = get_params(request)
        if not params.get("name"):
            raise Exception(u'必须传递名称')
        if not params.get("dev_id"):
            raise Exception(u'必须传递设备id')
        if not params.get("store_id"):
            raise Exception(u'必须传递仓库')
        if not params.get("bank_id"):
            raise Exception(u'必须传递收款账户')
        if not params.get("member_id"):
            raise Exception(u'必须传递会员')
        if not params.get("employee_id"):
            raise Exception(u'必须传递员工')
        if "bill_type" not in params:
            raise Exception(u'必须传递默认发票类型')
        old = get_device(session, set_of_book, params.get("dev_id"))
        if old:
            raise Exception(u'设备id %s 对应的配置已存在,不能重复' % params.get("dev_id"))
        new_device = Device(set_of_book=set_of_book, name=params.get("name"), dev_id=params.get("dev_id"), store_id=params.get("store_id"), bank_id=params.get("bank_id"), member_id=params.get("member_id"), employee_id=params.get("employee_id"), bill_type=(params.get("bill_type") or 0), created_at=datetime.now(), created_user=user_name)
        session.add(new_device)
        session.flush()
        result = new_device.to_dict()
        result["state"] = 1
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        return {"state": 0, "errmsg": str(e)}
    finally:
        session.close()


@app.route('/api/devices')
@app.route('/api/devices/<id:int>')
@token_auth
def read_device(id=None, **kwargs):
    session = Session()
    try:
        access_level = kwargs.get("access_level")
        if not access_level & 1:
            raise Exception(u"没有访问级 查看")
        set_of_book = kwargs.get("set_of_book")
        if id:
            current = session.query(Device).filter(Device.id == id, Device.set_of_book == set_of_book).first()
            if not current:
                raise Exception(u'该货柜配置不存在,请刷新后重试')
            result = current.to_dict()
            result["state"] = 1
        else:
            params = get_params(request)
            result = query_device(session, params, set_of_book)
        return result
    except Exception as e:
        return {"state": 0, "errmsg": str(e)}
    finally:
        session.close()


@app.route('/api/devices/<id:int>', method='PUT')
@token_auth
def update_device(id, **kwargs):
    session = Session()
    try:
        access_level = kwargs.get("access_level")
        if not access_level & 2:
            raise Exception(u"没有访问级 编辑")
        user_name = kwargs.get("user_name")
        set_of_book = kwargs.get("set_of_book")
        params = get_params(request)
        current = session.query(Device).filter(Device.id == id, Device.set_of_book == set_of_book).first()
        if not current:
            raise Exception(u'该货柜配置不存在,请刷新后重试')
        if params.get("name"):
            current.name = params.get("name")
        if params.get("dev_id"):
            old = get_device(session, set_of_book, params.get("dev_id"))
            if old and old.id != current.id:
                raise Exception(u'设备id %s 对应的配置已存在,不能重复' % params.get("dev_id"))
            current.dev_id = params.get("dev_id")
        if params.get("store_id"):
            current.store_id = params.get("store_id")
        if params.get("bank_id"):
            current.bank_id = params.get("bank_id")
        if params.get("member_id"):
            current.member_id = params.get("member_id")
        if params.get("employee_id"):
            current.employee_id = params.get("employee_id")
        if params.get("bill_type"):
            current.bill_type = params.get("bill_type")
        current.updated_at = datetime.now()
        current.updated_user = user_name
        session.commit()
        result = current.to_dict()
        result["state"] = 1
        return result
    except Exception as e:
        session.rollback()
        return {"state": 0, "errmsg": str(e)}
    finally:
        session.close()


@app.route('/api/devices/<id:int>', method='DELETE')
@token_auth
def delete_device(id, **kwargs):
    session = Session()
    try:
        access_level = kwargs.get("access_level")
        if not access_level & 8:
            raise Exception(u"没有访问级 删除")
        set_of_book = kwargs.get("set_of_book")
        current = session.query(Device).filter(Device.id == id, Device.set_of_book == set_of_book).first()
        if not current:
            raise Exception(u'该货柜配置不存在,请刷新后重试')
        session.delete(current)
        return {"state": 1}
    except Exception as e:
        session.rollback()
        return {"state": 0, "errmsg": str(e)}
    finally:
        session.close()


@app.route('/api/orders')
@app.route('/api/orders/<id:int>')
@token_auth
def read_order(id=None, **kwargs):
    session = Session()
    try:
        access_level = kwargs.get("access_level")
        set_of_book = kwargs.get("set_of_book")
        url = kwargs.get("url")
        token = kwargs.get("token")
        user_name = kwargs.get("user_name")
        params = get_params(request)
        action = params.get('action')
        if action == "import":
            if not access_level & 4:
                raise Exception(u"不具备访问级 创建")
            if not id:
                raise Exception(u"必须传递id")
            result = import_as_retail(session, id, set_of_book, url, token, user_name)
        elif action == "init_order":
            if not access_level & 2:
                raise Exception(u"不具备访问级 编辑")
            if not id:
                raise Exception(u"必须传递id")
            result = check_retail(session, id, set_of_book, params, url, token)
        elif action == "get_orders":
            if not access_level & 4:
                raise Exception(u"不具备访问级 创建")
            page = download_orders(session, set_of_book, params, user_name)
            return {"state": 1, "page": page}
        elif action == "trade_view":
            if not access_level & 1:
                raise Exception(u"不具备访问级 查看")
            result = query_orders(session, set_of_book, params)
        else:
            raise Exception(u"不能识别的action %s" % action)
        return result
    except Exception as e:
        session.rollback()
        return {"state": 0, "errmsg": str(e)}
    finally:
        session.close()


@app.route('/api/orders/<id:int>', method='delete')
@token_auth
def clear(id, **kwargs):
    session = Session()
    try:
        access_level = kwargs.get("access_level")
        if not access_level & 8:
            raise Exception(u"不具备访问级 删除")
        set_of_book = kwargs.get("set_of_book")
        if not id:
            raise Exception(u"必选传递id")
        current = session.query(Order).filter(Order.id == id, Order.set_of_book == set_of_book).first()
        if not current:
            raise Exception(u'该订单不存在,请刷新页面后重试')
        if current.is_imported:
            raise Exception(u'该订单已导入,不能删除')
        session.delete(current)
        session.commit()
        return {"state": 1}
    except Exception as e:
        session.rollback()
        return {"state": 0, "errmsg": str(e)}
    finally:
        session.close()


@app.route('/api/create_order', method='POST')
@token_auth
def create_order(**kwargs):
    session = Session()
    try:
        set_of_book = kwargs.get("set_of_book")
        user_name = kwargs.get("user_name")
        params = get_params(request)
        trans_id = params.get("trans_id")
        if not trans_id:
            raise Exception(u"必须传递交易id")
        status = params.get("status")
        if not status:
            raise Exception(u"必须传递交易状态")
        e_id = params.get("e_id")
        if not e_id:
            raise Exception(u"必须传递用户id")
        dev_id = params.get("dev_id")
        if not dev_id:
            raise Exception(u"必须传递设备id")
        create_time = params.get("create_time")
        update_time = params.get("update_time")
        products = params.get("products")
        total_amount = 0
        for item in products:
            total_amount += item.get("amount")
        current = session.query(Order).filter(Order.trans_id == trans_id, Order.set_of_book == set_of_book).first()
        if not current:
            new_order = Order(trans_id=trans_id, status=status, set_of_book=set_of_book, e_id=e_id, dev_id=dev_id, create_time=create_time, update_time=update_time, total_amount=total_amount, products={"items": products}, created_at=datetime.now(), created_user=user_name)
            session.add(new_order)
        else:
            if not current.is_imported:
                current.status = status
                current.e_id = e_id
                current.dev_id = dev_id
                current.create_time = create_time
                current.update_time = update_time
                current.total_amount = total_amount
                current.products = {"items": products}
                current.updated_at = datetime.now()
                current.updated_user = user_name
        session.commit()
        return {"state": 1}
    except Exception as e:
        session.rollback()
        return {"state": 0, "errmsg": str(e)}
    finally:
        session.close()


def main():
    run(app, server="gevent", host=settings.HOST, port=settings.PORT, quiet=True)

if __name__ == '__main__':
    main()