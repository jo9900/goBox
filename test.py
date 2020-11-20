#encoding=utf-8
import hashlib
import json
 
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

params = {
"access_token": "xxx.yyy.zzz",
"command": "QueryTrade",
"time": 1540274403,
"end_date": "2018-10-23",
"start_date": "2018-10-20"
}
print build_sign("123456abcdef", params)