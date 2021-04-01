# -*- coding: utf-8 -*-
# 通联数据机密
# --------------------------------------------------------------------
# 通联数据股份公司版权所有 © 2013-2020
#
# 注意：本文所载所有信息均属于通联数据股份公司资产。本文所包含的知识和技术概念均属于
# 通联数据产权，并可能由中国、美国和其他国家专利或申请中的专利所覆盖，并受商业秘密或
# 版权法保护。
# 除非事先获得通联数据股份公司书面许可，严禁传播文中信息或复制本材料。
#
# DataYes CONFIDENTIAL
# --------------------------------------------------------------------
# Copyright © 2013-2020 DataYes, All Rights Reserved.
#
# NOTICE: All information contained herein is the property of DataYes
# Incorporated. The intellectual and technical concepts contained herein are
# proprietary to DataYes Incorporated, and may be covered by China, U.S. and
# Other Countries Patents, patents in process, and are protected by trade
# secret or copyright law.
# Dissemination of this information or reproduction of this material is
# strictly forbidden unless prior written permission is obtained from DataYes.

# -*- coding: utf-8 -*-
'''
Created on 2014-3-17

@author: cheng.li
'''
from __future__ import unicode_literals

import inspect
import json
import os
import shutil
import re
from copy import deepcopy
import sys
import logging
import socket
import requests
import json
from requests.exceptions import ReadTimeout
from . import settings, global_cache_map
from platform import python_version

from .version import __version__

csv_encoding = 'gb2312'
request_encoding = 'UTF-8'
server = {}
remote_api_url = 'http://mercury-community-vip'
timeout = 120
source_header = {'SOURCE': 'mercury'}
client_info = {"python_version": python_version(),
               "client_version": __version__,
               "module": ''}


def set_client_info(sub_module='code'):
    mode = os.getenv('mode', 'ipython')
    client_info["module"] = 'uqer_%s_%s' % (mode, sub_module)


set_client_info()


def set_source_header(source):
    if source not in ['mercury_sdk', 'mercury_ipython']:
        return
    source_header['SOURCE'] = source


def get_http_result(httpClient, requestString, gw):
    username = os.environ.get('DatayesPrincipalName', 'unknown_user')
    if gw:
        result = requests.get("https://%s:%d/data/v1%s" % (httpClient[2], httpClient[3], requestString),
                              headers={'Connection': 'keep-alive',
                                       'Authorization': 'Bearer ' + get_token(),
                                       'SOURCE': source_header['SOURCE'] + ':' + username,
                                       'CLIENT_INFO': json.dumps(client_info)},
                              timeout=timeout,
                              verify=False)
    else:
        result = requests.get("http://%s:%d%s" % (httpClient[0], httpClient[1], requestString),
                              headers={'Connection': 'keep-alive',
                                       'SOURCE': source_header['SOURCE'] + ':' + username,
                                       'CLIENT_INFO': json.dumps(client_info)},
                              timeout=timeout)
    return result


def get_real_string(input_string):
    if sys.version_info.major == 2:
        out = input_string.encode('utf-8')
    else:
        out = input_string
    return out


def __getCSV__(requestString, httpClient, gw=True):
    if os.environ.get('internal_api_need_gw', '1') != '1':
        gw = False
    max_len = 500000 if not gw else 100000
    try:
        result = get_http_result(httpClient, requestString, gw)
        if result.status_code == 400:
            raise Exception(get_real_string('请检查输入参数，可能某列表输入参数过长'))
        if result.status_code != 200:
            raise Exception(get_real_string('服务器出现问题，异常代码 %d' % result.status_code))
        if int(result.headers.get('dyes-rsp-count', 0)) == max_len:
            result2 = get_http_result(httpClient, requestString + '&pagenum=2', gw)
            if int(result2.headers.get('dyes-rsp-count', 0)) > 0:
                raise Exception(get_real_string('返回数据量过大，请修改参数减小返回数据量'))
        return result.text
    except ReadTimeout:
        logging.error('timeout for %s' % requestString)
        raise Exception(get_real_string('DataAPI查询服务超时'))
    except Exception as e:
        import traceback
        logging.error('error for %s' % requestString)
        raise e


def get_cache_key(frame):
    args, _, _, values = inspect.getargvalues(frame)
    func_name = inspect.getframeinfo(frame)[2]
    cache_key = hash([values[arg] for arg in args].__str__())
    return func_name, cache_key


def get_data_from_cache(func_name, cache_key):
    if not settings.cache_enabled:
        return None
    if func_name not in global_cache_map:
        global_cache_map[func_name] = {}
        return None
    if cache_key not in global_cache_map[func_name]:
        return None
    return global_cache_map[func_name][cache_key]


def put_data_in_cache(func_name, cache_key, data):
    if not settings.cache_enabled:
        return
    if func_name not in global_cache_map:
        global_cache_map[func_name] = {}
    try:
        temp_data = deepcopy(data)
    except:
        temp_data = data

    global_cache_map[func_name][cache_key] = temp_data


def splist(l, s):
    return [l[i:i + s] for i in xrange(len(l)) if i % s == 0]


def is_no_data_warn(csvString, print_msg):
    if csvString.startswith('-1:No Data Returned'):
        # if print_msg:
        #     print('没有数据返回。请检查输入参数，若仍有问题，可联系service.uqer@datayes.com')
        return True
    return False


def handle_error(csvString, api_name):
    if csvString.startswith('-403:Need Privilege'):
        result = '无%s接口使用权限，您可以购买优矿专业版（ https://uqer.io/pro ） 或联系 4000 820 386 购买数据' % api_name
    elif csvString.startswith('-403:Need login'):
        result = '您未登陆'
    elif csvString.startswith('-2:Invalid Request Parameter'):
        result = '无效的请求参数。请检查输入参数，若仍有问题，可联系service.uqer@datayes.com'
    elif csvString.startswith('-3:Service Suspend'):
        result = '服务终止。请联系service.uqer@datayes.com'
    elif csvString.startswith('-4:Internal Server Error'):
        result = '内部服务器错误。请联系service.uqer@datayes.com'
    elif csvString.startswith('-5:Server Busy'):
        result = '服务器拥堵。可能是海量用户在同一时间集中调用该数据造成，可稍后再次尝试。' \
                 '如长时间未改善，或频繁出现该问题，可联系sevice.uqer@datayes.com'
    elif csvString.startswith('-6:Trial Times Over'):
        result = '试用次数达到限制。您对该数据的试用权限已经到期'
    elif csvString.startswith('-7:Query Timeout'):
        result = '请求超时。可能您请求的数据量较大或服务器当前忙'
    elif csvString.startswith('-8:Query Failed'):
        result = '请求失败，请联系service.uqer@datayes.com'
    elif csvString.startswith('-9:Required Parameter Missing'):
        result = '必填参数缺失。请仔细复核代码，将其中的参数补充完整后再次尝试'
    elif csvString.startswith('-11:The number of API calls reached limit'):
        result = '当日调用次数达到上限，请优化代码调用逻辑。每日0点重新计数'
    else:
        result = csvString
    raise Exception(get_real_string(result))


def is_pro_user():
    try:
        privilege = os.getenv('privilege', '{}')
        privilege = json.loads(privilege)
        return privilege['basic'] == 1 if 'basic' in privilege else False
    except:
        return False


def get_token():
    import os
    ACCESS_TOKEN = "access_token"
    return os.environ.get(ACCESS_TOKEN, 'd577ea573e2940b1c84503fadac6179be92fea9ca63ba7bf1aad49714d78e8d9')


def __getConn__():
    if not server:
        env_tag = os.getenv('env', 'dev')
        port = int(os.environ.get('dataapi_port', '80'))
        if env_tag != 'dev':
            server[0] = socket.gethostbyname('data-api')
            server[1] = port
            server[3] = 443
            if env_tag == 'prd':
                server[2] = 'api.wmcloud.com'
            else:
                server[2] = 'api.wmcloud-stg.com'
        else:
            server[0] = socket.gethostbyname('Please set the dataapi server url, or set the environment: "env" and "dataapi_port"')
            server[1] = port
            server[2] = 'api.wmcloud.com'
            server[3] = 443
    return server


def __formatDate__(inputDate):
    return inputDate


def lowcase_keys(d):
    result = {}
    for key, value in d.items():
        lower_key = key.lower()
        result[lower_key] = value
    return result


def showtraceback(self, exc_tuple=None, filename=None, tb_offset=None,
                  exception_only=False):
    import traceback
    import sys

    etype, value, tb = self._get_exc_info(exc_tuple)
    listing = traceback.format_exception(etype, value, tb)
    last_message = ''
    lineno = None
    text = ''

    if listing:
        last_message = listing[-1].decode("unicode-escape")

    except_msg = 'Exception:'
    if last_message.startswith(except_msg):
        last_message = '异常:' + last_message[len(except_msg):]

    for filename, lineno, module, text in traceback.extract_tb(tb):
        if filename.startswith('<mercury-input') and \
                not text.startswith('display=True, return_quartz_data=True'):
            break

    if lineno:
        print('行号: %s\n代码: %s\n%s' % (lineno, text, last_message))
    else:
        print(last_message)


def pretty_traceback():
    if not settings.pretty_traceback_enabled:
        return
    import os
    if os.environ.get('env') in ['qa', 'stg', 'prd']:
        try:
            import IPython
            IPython.core.interactiveshell.InteractiveShell.showtraceback = showtraceback
        except:
            pass


def is_enterprise_user():
    if os.environ.get('enterprise', '0') == '1':
        return True
    else:
        return False


import requests
import os
import codecs
from .version import __version__ as sdk_version

version_url = '%s/w/api/info' % (remote_api_url)
files_url = '%s/w/api/download' % (remote_api_url)


def get_api_version():
    res = requests.get(version_url).json()
    if res.get('code') != 200:
        return '', []

    remote_version = res['data']['version']
    py_files = res['data']['py_files']

    return remote_version, py_files


def get_api_file(filename):
    code = 0
    text = ''

    for i in range(3):
        try:
            response = requests.get('%s/%s' % (files_url, filename))
            code, text = response.status_code, response.text
            if code == 200:
                break
        except:
            pass
        import time;
        time.sleep(1)

    return code, text


regex_full_version = re.compile(r"(\d+)\.(\d+)\.(\d+)")


def larger_than(version1, version2):
    if not version1 or not version2:
        raise Exception("version can not be empty!")

    match1 = regex_full_version.match(version1)
    match2 = regex_full_version.match(version2)

    if not match1 or not match2:
        raise Exception("version format is wrong!")

    result = True  # default value <=
    for v1, v2 in zip(match1.groups(), match2.groups()):
        if int(v1) == int(v2):
            continue

        elif int(v1) < int(v2):
            break

        elif int(v1) > int(v2):
            result = True
            break

    return result


def replace_api_files():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    remote_version, py_files = get_api_version()
    if not remote_version or not larger_than(remote_version, sdk_version):
        return

    for filename in py_files:
        if filename == '__init__':
            continue

        filename = '%s.py' % (filename)
        file_path = os.path.join(dir_path, filename)

        status_code, response = get_api_file(filename)

        if status_code != 200:
            # 文件可能是没下载正确，就不更新了
            continue

        if os.path.isfile(file_path):
            os.remove(file_path)

        with codecs.open(file_path, 'w', "utf-8-sig") as f:
            f.write(response)

    version_str = "__version__ = '%s'" % (remote_version)
    version_file_path = os.path.join(dir_path, 'version.py')
    with open(version_file_path, 'w') as f:
        f.write(version_str)

def replace_api_files_from_data(source_file_path):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filename = 'DATAYES'

    filename = '%s.py' % (filename)
    dst_file_path = os.path.join(dir_path, filename)

    shutil.copyfile(source_file_path, dst_file_path)
