# encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from suds.client import Client
import json
from datetime import datetime, timedelta
import random
import requests
import base64
import xlrd
import settings
import jwt
import base64
import time
import hashlib

from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import column, and_, or_, not_, select, text, exists, literal, union_all, case, alias, null, literal_column, extract, cast
from models import *

engine = create_engine('postgresql+psycopg2://%s:%s@%s/%s' % (settings.USER, settings.PASSWORD,
                                                              settings.DATA_HOST, settings.DATABASE), echo=True, client_encoding='utf8')
Session = sessionmaker(bind=engine)
partner_map = {}
employee_map = {}
product_map = {}

def get_params(request):
    params = request.params
    body = request.body.read()
    if body:
        rec = json.loads(body)
        for item in rec:
            params[item] = rec.get(item)
    return params

def build_sign(app_secret, params):
    data = params
    keys = list(data.keys())
    keys = sorted(keys)
    values = {}
    for key in keys:
        values[key] = data[key]
    sign_ = "%s%s" % (json.dumps(values,sort_keys=True), app_secret)
    print sign_.decode("unicode_escape").replace(' ', '')
    return md5_sign(sign_.decode("unicode_escape").replace(' ', ''))


def md5_sign(content):
    return hashlib.md5(content).hexdigest()


def request_access_token(set_of_book):
    data = {"user": set_of_book.user_name, "time": int(time.time()), "command": "GetToken"}
    sign = build_sign(set_of_book.app_key, data)
    data["sign"] = sign
    r = requests.post("%s/access-token" % settings.url, data=json.dumps(data))
    if r.status_code != 200 or (r.json().get("code") != 0):
        print r.text
        raise Exception(r.text)
    return r.json().get("output").get("access_token"), r.json().get("output").get("expires")


def request_trade_list(app_key, data):
    data["time"] = int(time.time())
    sign = build_sign(app_key, data)
    data["sign"] = sign
    r = requests.post("%s/trade" % settings.url, data=json.dumps(data))
    if r.status_code != 200 or (r.json().get("code") != 0):
        print r.text
        raise Exception(r.text)
    return r.json()

def get_set_of_book(session, set_of_book):
    set_of_book = session.query(SetOfBook).filter(SetOfBook.set_of_book == set_of_book).first()
    if not set_of_book:
        raise Exception(u'账套配置不存在')
    return set_of_book

def get_device(session, set_of_book, dev_id):
    current = session.query(Device).filter(Device.dev_id == dev_id, Device.set_of_book == set_of_book).first()
    if not current:
        return None
    return current

def get_access_token(session, set_of_book):
    sob = get_set_of_book(session, set_of_book)
    now = datetime.now()
    if now > sob.expired_at:
        try:
            access_token, expires = request_access_token(sob)
            sob.access_token = access_token
            sob.token_created_at = now
            sob.expired_at = now + timedelta(seconds=expires)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
    return sob.access_token


def query_device(session, params, set_of_book):
    a = devices
    fields = [a]
    q = select(fields, from_obj=(a)).where(a.c.set_of_book == set_of_book)
    if params.get("name"):
        q = q.where(a.c.name == params.get("name"))
    start = params.get("start")
    limit = params.get("limit")
    results = []
    if start and limit:
        x = q.alias("x")
        total = session.execute(x.count()).scalar()
        trades = session.execute(q.order_by(a.c.created_at.desc()).offset(start).limit(limit)).fetchall()
        for item in trades:
            trade = ObjectDict(id=item.id, set_of_book=item.set_of_book, name=item.name, dev_id=item.dev_id, store_id=item.store_id, bank_id=item.bank_id, member_id=item.member_id, employee_id=item.employee_id, bill_type=item.bill_type, created_at=item.created_at.strftime('%Y-%m-%d %H:%M:%S') if item.created_at else "", created_user=item.created_user, updated_at=item.updated_at.strftime('%Y-%m-%d %H:%M:%S') if item.updated_at else "", updated_user=item.updated_user)
            results.append(trade)
    else:
        trades = session.execute(q.order_by(a.c.created_at.desc())).fetchall()
        for item in trades:
            trade = ObjectDict(id=item.id, set_of_book=item.set_of_book, name=item.name, dev_id=item.dev_id, store_id=item.store_id, bank_id=item.bank_id, member_id=item.member_id, employee_id=item.employee_id, bill_type=item.bill_type, created_at=item.created_at.strftime('%Y-%m-%d %H:%M:%S') if item.created_at else "", created_user=item.created_user, updated_at=item.updated_at.strftime('%Y-%m-%d %H:%M:%S') if item.updated_at else "", updated_user=item.updated_user)
            results.append(trade)
        total = len(results)
    result = {"total": total, "state": 1, "root": results}
    return result


def download_orders(session, set_of_book, params, user_name):
    access_token = get_access_token(session, set_of_book)
    sob = get_set_of_book(session, set_of_book)
    data = ObjectDict(access_token=access_token, command="QueryTrade")
    start_date = params.get("start_date")
    end_date = params.get("end_date")
    if start_date:
        data.start_date = start_date
    if end_date:
        data.end_date = end_date
    dev_id = params.get("dev_id")
    if dev_id:
        data.dev_id = dev_id
    trans_id = params.get("trans_id")
    if trans_id:
        data.trans_id = trans_id
    status = params.get("status")
    if status:
        data.status = status
    orders = request_trade_list(sob.app_key, data)
    trade_list = orders.get("output").get("trade_list")
    trade_lists = ObjectDict()
    for trade in trade_list:
        if trade.get("trans_id") in trade_lists:
            trade_ = trade_lists.get(trade.get("trans_id"))
        else:
            trade_ = ObjectDict(trans_id=trade.get("trans_id"), status=trade.get("status"), e_id=trade.get("e_id"), dev_id=trade.get("dev_id"), create_time=trade.get("create_time"), update_time=trade.get("update_time"), total_amount=0, lines=[])
            trade_lists[trade_.trans_id] = trade_
        product_line = ObjectDict(num=trade.get("num"), cost=trade.get("cost"), barcode=trade.get("barcode"), name=trade.get("name"), amount=trade.get("amount"), tax_price=trade.get("amount")/trade.get("num"))
        trade_.total_amount += product_line.amount
        trade_.lines.append(product_line)
    try:
        for key, value in trade_lists.items():
            current = session.query(Order).filter(Order.trans_id == key, Order.set_of_book == set_of_book).first()
            if not current:
                new_order = Order(trans_id=key, status=value.status, set_of_book=set_of_book, e_id=value.e_id, dev_id=value.dev_id, create_time=value.create_time, update_time=value.update_time, total_amount=value.total_amount, products={"items": value.lines}, created_at=datetime.now(), created_user=user_name)
                session.add(new_order)
        session.commit()
        return None
    except Exception as e:
        session.rollback()
        raise e

def query_orders(session, set_of_book, params):
    a = orders
    fields = [a]
    q = select(fields, from_obj=(a)).where(a.c.set_of_book == set_of_book)
    if params.get("dev_id"):
        q = q.where(a.c.dev_id == params.get("dev_id"))
    if params.get("start_date"):
        q = q.where(a.c.create_time >= params.get("start_date"))
    if params.get("end_date"):
        q = q.where(a.c.create_time <= params.get("end_date"))
    if params.get("status"):
        q = q.where(a.c.status == params.get("status"))
    if params.get("trans_id"):
        q = q.where(a.c.trans_id == params.get("trans_id"))
    is_imported = params.get("is_imported")
    if is_imported:
        if int(is_imported) == 1:
            q = q.where(a.c.is_imported == True)
        else:
            q = q.where(a.c.is_imported == False)
    start = params.get("start")
    limit = params.get("limit")
    results = []
    if start and limit:
        x = q.alias("x")
        total = session.execute(x.count()).scalar()
        trades = session.execute(q.order_by(a.c.create_time.desc()).offset(start).limit(limit)).fetchall()
        for item in trades:
            trade = ObjectDict(id=item.id, trans_id=item.trans_id, status=item.status, e_id=item.e_id, dev_id=item.dev_id, total_amount=item.total_amount, create_time=item.create_time.strftime('%Y-%m-%d %H:%M:%S') if item.create_time else "", update_time=item.update_time.strftime('%Y-%m-%d %H:%M:%S') if item.update_time else "", created_at=item.created_at.strftime('%Y-%m-%d %H:%M:%S') if item.created_at else "", created_user=item.created_user, updated_at=item.updated_at.strftime('%Y-%m-%d %H:%M:%S') if item.updated_at else "", updated_user=item.updated_user, is_imported=item.is_imported, imported_at=item.imported_at.strftime('%Y-%m-%d %H:%M:%S') if item.imported_at else "", imported_user=item.imported_user, retail_id=item.retail_id, products=item.products, retail_code=item.retail_code, set_of_book=item.set_of_book)
            results.append(trade)
    else:
        trades = session.execute(q.order_by(a.c.created_at.desc())).fetchall()
        for item in trades:
            trade = ObjectDict(id=item.id, trans_id=item.trans_id, status=item.status, e_id=item.e_id, dev_id=item.dev_id, total_amount=item.total_amount, create_time=item.create_time.strftime('%Y-%m-%d %H:%M:%S') if item.create_time else "", update_time=item.update_time.strftime('%Y-%m-%d %H:%M:%S') if item.update_time else "", created_at=item.created_at.strftime('%Y-%m-%d %H:%M:%S') if item.created_at else "", created_user=item.created_user, updated_at=item.updated_at.strftime('%Y-%m-%d %H:%M:%S') if item.updated_at else "", updated_user=item.updated_user, is_imported=item.is_imported, imported_at=item.imported_at.strftime('%Y-%m-%d %H:%M:%S') if item.imported_at else "", imported_user=item.imported_user, retail_id=item.retail_id, products=item.products, retail_code=item.retail_code, set_of_book=item.set_of_book)
            results.append(trade)
        total = len(results)
    result = {"total": total, "state": 1, "root": results}
    return result


def import_as_retail(session, id, set_of_book, url, token, user_name):
    id = int(id)
    current = session.query(Order).filter(Order.id == id, Order.set_of_book == set_of_book).first()
    if not current:
        raise Exception(u"id 为 %s 的订单不存在" % id)
    if current.is_imported:
        raise Exception(u" id 为 %s 的订单已导入,不能重复导入" % id)
    if current.status != 100:
        raise Exception(u"id 为 %s 的订单状态不为支付成功" % id)
    device = get_device(session, set_of_book, current.dev_id)
    if not device:
        raise Exception(u'设备id %s 对应货柜配置不存在' % current.dev_id)
    retail = generate_retail(url, token, current, device, set_of_book)
    current.is_imported = True
    current.imported_user = user_name
    current.imported_at = datetime.now()
    current.retail_code = retail.code
    current.retail_id = retail.id
    session.commit()
    confirm_retail(url, token, retail.id)
    execute_retail(url, token, retail.id)
    return {"state": 1}


def generate_retail(url, token, order, device, set_of_book):
    headers = {"Token": token}
    data = ObjectDict(source="gobox", source_id=order.trans_id, store_id=device.store_id, bill_type=device.bill_type,  bank_id=device.bank_id, member_id=device.member_id, employee_id=device.employee_id, total_amount=order.total_amount, bank_amount=order.total_amount)
    tax_rate = 0
    if data.bill_type != 0:
        sob = get_tax_rate(url, token, set_of_book)
        if data.bill_type == 1:
            tax_rate = sob.get("tax_rate")
        else:
            tax_rate = sob.get("vat_tax_rate")
    
    retail_lines = []
    for item in order.products.get("items"):
        line = ObjectDict()
        if item.get("barcode") in product_map:
            product = product_map.get(item.get("barcode"))
        else:
            product = get_product_by_barcode(url, token, item.get("barcode"))
            product_map[item.get("barcode")] = product
        line.product_id = product.id
        line.quantity = item.get("num")
        line.tax_price = item.get("tax_price")
        line.tax_rate = tax_rate
        retail_lines.append(line)
    data.retail_lines = retail_lines
    r = requests.post("%s/api/retails" % url, headers=headers, data=json.dumps(data))
    if r.status_code != 200:
        raise Exception(r.text)
    return json.loads(r.text, object_pairs_hook=ObjectDict)


def check_retail(session, id, set_of_book, params, url, token):
    current = session.query(Order).filter(Order.id == id, Order.is_imported == True, Order.set_of_book == set_of_book).first()
    if not current:
        return {"state": 1}
    retail = get_retail(url, token, current.retail_id)
    if not retail:
        current.is_imported = False
        current.imported_at = None
        current.imported_user = None
        current.retail_id = None
        current.retail_code = None
    else:
        return {"state": 0, "errmsg": u"该合同对应的零售单依然存在,请删除后重试"}
    session.commit()
    return {"state": 1}


def get_retail(url, token, id):
    headers = {"Token": token}
    r = requests.get("%s/api/retails/%s" % (url, id), headers=headers)
    if r.status_code != 200:
        raise Exception(r.text)
    if not r.text or r.text == "null":
        return False
    return True


def get_partner(url, token, name):
    headers = {"Token": token}
    params = {"name": name}
    r = requests.get("%s/api/partners" % url, headers=headers, params=params)
    if r.status_code != 200:
        raise Exception(r.text)
    if not r.json().get("root"):
        raise Exception(u"商业伙伴 %s 不存在" % name)
    return r.json().get("root")[0]


def get_employee(url, token, name):
    headers = {"Token": token}
    params = {"name": name}
    r = requests.get("%s/api/employees" % url, headers=headers, params=params)
    if r.status_code != 200:
        raise Exception(r.text)
    if not r.json().get("root"):
        raise Exception(u"员工 %s 不存在" % name)
    return r.json().get("root")[0]


def get_product_by_barcode(url, token, barcode):
    headers = {"Token": token}
    params = {"barcode": barcode}
    r = requests.get("%s/api/products" % url, headers=headers, params=params)
    if r.status_code != 200:
        raise Exception(r.text)
    if not r.json().get("root"):
        raise Exception(u"产品码为 %s 的商品不存在" % barcode)
    product = ObjectDict(r.json().get("root")[0])
    return product

def get_tax_rate(url, token, set_of_book):
    headers = {"Token": token}
    r = requests.get("%s/api/set_of_books/%s" % (url, set_of_book), headers=headers)
    if r.status_code != 200:
        raise Exception(r.text)
    return r.json()


def confirm_retail(url, token, id):
    headers = {"Token": token}
    r = requests.get("%s/api/retails/%s?action=confirm&action_type=1" % (url, id), headers=headers)
    if r.status_code != 200:
        raise Exception(r.text)
    return True

def execute_retail(url, token, id):
    headers = {"Token": token}
    r = requests.get('%s/api/workflow_current_actions?action=execute_workflow&form_name=retail&form_id=%s&result={"memo":"","cancel":false}' %(url, id), headers=headers)
    if r.status_code != 200:
        raise Exception(r.text)
    time.sleep(0.1)
    if r.json().get("status") != 6:
        execute_retail(url, token, id)
    return True