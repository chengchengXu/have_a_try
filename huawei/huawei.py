# coding: utf-8

import sys
import os
import requests as rq
import json
from datetime import datetime, timedelta, timezone

token_file = "huawei_token.json"

ecs_status_code = {
    'SUCCEED_REQ': (200, '请求成功。')
    , 'SUCCEED_LATER': (202, '任务提交成功，当前系统繁忙，下发的任务会延迟处理。')
    , 'SUCCEED_TASK': (204, '任务提交成功。')
    , 'MULTIPLE_CHOICES': (300, '被请求的资源存在多个可供选择的响应。')
    , 'BAD_REQUEST': (400, '服务器未能处理请求。')
    , 'UNAUTHORIZED': (401, '被请求的页面需要用户名和密码。')
    , 'FORBIDDEN': (403, '对被请求页面的访问被禁止。')
    , 'NOT_FOUND': (404, '服务器无法找到被请求的页面。')
    , 'METHOD_NOT_ALLOWED': (405, '请求中指定的方法不被允许。')
    , 'NOT_ACCEPTABLE': (406, '服务器生成的响应无法被客户端所接受。')
    , 'PROXY_AUTHENTICATION_REQUIRED': (407, '用户必须首先使用代理服务器进行验证，这样请求才会被处理。')
    , 'REQUEST_TIMEOUT': (408, '请求超出了服务器的等待时间。')
    , 'CONFLICT': (409, '由于冲突，请求无法被完成。')
    , 'INTERNAL_SERVER_ERROR': (500, '请求未完成。服务异常。')
    , 'NOT_IMPLEMENTED': (501, '请求未完成。服务器不支持所请求的功能。')
    , 'BAD_GATEWAY': (502, '请求未完成。服务器从上游服务器收到一个无效的响应。')
    , 'SERVICE_UNAVAILABLE': (503, '请求未完成。系统暂时异常。')
    , 'GATEWAY_TIMEOUT': (504, '网关超时。')
}
ecs_status_code_succeed_key = ['SUCCEED_TASK', 'SUCCEED_LATER', 'SUCCEED_REQ']
ecs_status_code_succeed_code = [c for k, (c, d) in ecs_status_code.items() if k in ecs_status_code_succeed_key]

vpc_status_code = {
    'SUCCEED_OK': (200, 'GET、PUT、POST操作正常返回')
    , 'SUCCEED_CREATED': (201, 'OPENSTACK NEUTRON API的POST操作正常返回')
    , 'SUCCEED_NO_CONTENT': (204, 'DELETE操作正常返回')
    , 'BAD_REQUEST': (400, '服务器未能处理请求。')
    , 'UNAUTHORIZED': (401, '被请求的页面需要用户名和密码。')
    , 'FORBIDDEN': (403, '对被请求页面的访问被禁止。')
    , 'NOT_FOUND': (404, '服务器无法找到被请求的页面。')
    , 'METHOD_NOT_ALLOWED': (405, '请求中指定的方法不被允许。')
    , 'NOT_ACCEPTABLE': (406, '服务器生成的响应无法被客户端所接受。')
    , 'PROXY_AUTHENTICATION_REQUIRED': (407, '用户必须首先使用代理服务器进行验证，这样请求才会被处理。')
    , 'REQUEST_TIMEOUT': (408, '请求超出了服务器的等待时间。')
    , 'CONFLICT': (409, '由于冲突，请求无法被完成。')
    , 'INTERNAL_SERVER_ERROR': (500, '请求未完成。服务异常。')
    , 'NOT_IMPLEMENTED': (501, '请求未完成。服务器不支持所请求的功能。')
    , 'BAD_GATEWAY': (502, '请求未完成。服务器从上游服务器收到一个无效的响应。')
    , 'SERVICE_UNAVAILABLE': (503, '请求未完成。系统暂时异常。')
    , 'GATEWAY_TIMEOUT': (504, '网关超时。')
}
vpc_status_code_succeed_key = ['SUCCEED_OK', 'SUCCEED_CREATED', 'SUCCEED_NO_CONTENT']
vpc_status_code_succeed_code = [c for k, (c, d) in vpc_status_code.items() if k in vpc_status_code_succeed_key]

eps_status_code = {
    'OK': (200, 'GET和PUT操作正常返回。')
    , 'CREATED': (201, 'POST操作正常返回。')
    , 'ACCEPTED': (202, '请求已被接受。')
    , 'NO_CONTENT': (204, '正常返回。')
    , 'BAD_REQUEST': (400, '服务器未能处理请求。')
    , 'UNAUTHORIZED': (401, '被请求的页面需要用户名和密码。')
    , 'FORBIDDEN': (403, '对被请求页面的访问被禁止。')
    , 'NOT_FOUND': (404, '服务器无法找到被请求的页面。')
    , 'METHOD_NOT_ALLOWED': (405, '请求中指定的方法不被允许。')
    , 'NOT_ACCEPTABLE': (406, '服务器生成的响应无法被客户端所接受。')
    , 'PROXY_AUTHENTICATION_REQUIRED': (407, '用户必须首先使用代理服务器进行验证，这样请求才会被处理。')
    , 'REQUEST_TIMEOUT': (408, '请求超出了服务器的等待时间。')
    , 'CONFLICT': (409, '由于冲突，请求无法被完成。')
    , 'INTERNAL_SERVER_ERROR': (500, '请求未完成。服务异常。')
    , 'NOT_IMPLEMENTED': (501, '请求未完成。服务器不支持所请求的功能。')
    , 'BAD_GATEWAY': (502, '请求未完成。服务器从上游服务器收到一个无效的响应。')
    , 'SERVICE_UNAVAILABLE': (503, '请求未完成。系统暂时异常。')
    , 'GATEWAY_TIMEOUT': (504, '网关超时。')
}
eps_status_code_succeed_key = ['OK', 'CREATED', 'ACCEPTED', 'NO_CONTENT']
eps_status_code_succeed_code = [c for k, (c, d) in eps_status_code.items() if k in eps_status_code_succeed_key]

ims_status_code = {
    'OK': (200, '正常。')
    , 'BAD_REQUEST': (400, '请求错误，具体返回错误码请参考错误码。')
    , 'UNAUTHORIZED': (401, '鉴权失败。')
    , 'FORBIDDEN': (403, '没有操作权限。')
    , 'NOT_FOUND': (404, '找不到资源。')
    , 'INTERNAL_SERVER_ERROR': (500, '服务内部错误。')
    , 'SERVICE_UNAVAILABLE': (503, '服务不可用。')
}
ims_status_code_succeed_key = ['OK']
ims_status_code_succeed_code = [c for k, (c, d) in ims_status_code.items() if k in ims_status_code_succeed_key]

swr_status_code = {
    'OK': (200, '请求成功。')
    , 'BAD_REQUEST': (400, '错误请求，返回错误信息。')
    , 'UNAUTHORIZED': (401, '鉴权失败的报错信息。')
    , 'INTERNAL_SERVER_ERROR': (500, '服务器内部错误，返回错误信息。')
}
swr_status_code_succeed_key = ['OK']
swr_status_code_succeed_code = [c for k, (c, d) in swr_status_code.items() if k in swr_status_code_succeed_key]

cci_status_code = {
    'CONTINUE': (100, '继续请求。这个临时响应用来通知客户端，它的部分请求已经被服务器接收，且仍未被拒绝。')
    , 'SWITCHING_PROTOCOLS': (101, '切换协议。只能切换到更高级的协议。例如，切换到HTTP的新版本协议。')
    , 'OK': (200, 'GET、PUT、POST操作正常返回。')
    , 'CREATED': (201, '创建类的请求完全成功。')
    , 'ACCEPTED': (202, '已经接受请求，但未处理完成。')
    , 'NON-AUTHORITATIVE_INFORMATION': (203, '非授权信息，请求成功。')
    , 'NOCONTENT': (204, '请求完全成功，同时HTTP响应不包含响应体。在响应OPTIONS方法的HTTP请求时返回此状态码。')
    , 'RESET_CONTENT': (205, '重置内容，服务器处理成功。')
    , 'PARTIAL_CONTENT': (206, '服务器成功处理了部分GET请求。')
    , 'MULTIPLE_CHOICES': (300, '多种选择。请求的资源可包括多个位置，相应可返回一个资源特征与地址的列表用于用户终端（例如：浏览器）选择。')
    , 'MOVED_PERMANENTLY': (301, '永久移动，请求的资源已被永久的移动到新的URI，返回信息会包括新的URI。')
    , 'FOUND': (302, '资源被临时移动。')
    , 'SEE_OTHER': (303, '查看其它地址。使用GET和POST请求查看。')
    , 'NOT_MODIFIED': (304, '所请求的资源未修改，服务器返回此状态码时，不会返回任何资源。')
    , 'USE_PROXY': (305, '所请求的资源必须通过代理访问。')
    , 'UNUSED': (306, '已经被废弃的HTTP状态码。')
    , 'BADREQUEST': (400, '非法请求。建议直接修改该请求，不要重试该请求。')
    , 'UNAUTHORIZED': (401, '在客户端提供认证信息后，返回该状态码，表明服务端指出客户端所提供的认证信息不正确或非法。')
    , 'PAYMENT_REQUIRED': (402, '保留请求。')
    , 'FORBIDDEN': (403, '请求被拒绝访问。返回该状态码，表明请求能够到达服务端，且服务端能够理解用户请求，但是拒绝做更多的事情，因为该请求被设置为拒绝访问，建议直接修改该请求，不要重试该请求。')
    , 'NOTFOUND': (404, '所请求的资源不存在。建议直接修改该请求，不要重试该请求。')
    , 'METHODNOTALLOWED': (405, '请求中带有该资源不支持的方法。建议直接修改该请求，不要重试该请求。')
    , 'NOT_ACCEPTABLE': (406, '服务器无法根据客户端请求的内容特性完成请求。')
    , 'PROXY_AUTHENTICATION_REQUIRED': (407, '请求要求代理的身份认证，与401类似，但请求者应当使用代理进行授权。')
    , 'REQUEST_TIME-OUT': (408, '服务器等候请求时发生超时。客户端可以随时再次提交该请求而无需进行任何更改。')
    , 'CONFLICT': (409, '服务器在完成请求时发生冲突。返回该状态码，表明客户端尝试创建的资源已经存在，或者由于冲突请求的更新操作不能被完成。')
    , 'GONE': (410, '客户端请求的资源已经不存在。返回该状态码，表明请求的资源已被永久删除。')
    , 'LENGTH_REQUIRED': (411, '服务器无法处理客户端发送的不带Content-Length的请求信息。')
    , 'PRECONDITION_FAILED': (412, '未满足前提条件，服务器未满足请求者在请求中设置的其中一个前提条件。')
    , 'REQUEST_ENTITY_TOO_LARGE': (
        413, '由于请求的实体过大，服务器无法处理，因此拒绝请求。为防止客户端的连续请求，服务器可能会关闭连接。如果只是服务器暂时无法处理，则会包含一个Retry-After的响应信息。')
    , 'REQUEST-URI_TOO_LARGE': (414, '请求的URI过长（URI通常为网址），服务器无法处理。')
    , 'UNSUPPORTED_MEDIA_TYPE': (415, '服务器无法处理请求附带的媒体格式。')
    , 'REQUESTED_RANGE_NOT_SATISFIABLE': (416, '客户端请求的范围无效。')
    , 'EXPECTATION_FAILED': (417, '服务器无法满足Expect的请求头信息。')
    , 'UNPROCESSABLEENTITY': (422, '请求格式正确，但是由于含有语义错误，无法响应。')
    , 'TOOMANYREQUESTS': (429, '表明请求超出了客户端访问频率的限制或者服务端接收到多于它能处理的请求。建议客户端读取相应的Retry-After首部，然后等待该首部指出的时间后再重试。')
    , 'INTERNALSERVERERROR': (500, '表明服务端能被请求访问到，但是不能理解用户的请求。')
    , 'NOT_IMPLEMENTED': (501, '服务器不支持请求的功能，无法完成请求。')
    , 'BAD_GATEWAY': (502, '充当网关或代理的服务器，从远端服务器接收到了一个无效的请求。')
    , 'SERVICEUNAVAILABLE': (503, '被请求的服务无效。建议直接修改该请求，不要重试该请求。')
    , 'SERVERTIMEOUT': (504, '请求在给定的时间内无法完成。客户端仅在为请求指定超时（Timeout）参数时会得到该响应。')
    , 'HTTP_VERSION_NOT_SUPPORTED': (505, '服务器不支持请求的HTTP协议的版本，无法完成处理。')

}
cci_status_code_succeed_key = ['OK', 'CREATED', 'ACCEPTED', 'NON-AUTHORITATIVE_INFORMATION', 'NOCONTENT',
                               'RESET_CONTENT', 'PARTIAL_CONTENT']
cci_status_code_succeed_code = [c for k, (c, d) in cci_status_code.items() if k in cci_status_code_succeed_key]

aom_status_code = {
    'OK': (200, '请求响应成功。')
    , 'BADREQUEST': (400, '非法请求。建议直接修改该请求，不要重试该请求。')
    , 'UNAUTHORIZED': (401, '在客户端提供认证信息后，返回该状态码，表明服务端指出客户端所提供的认证信息不正确或非法。')
    , 'FORBIDDEN': (403, '请求被拒绝访问。返回该状态码，表明请求能够到达服务端，且服务端能够理解用户请求，但是拒绝做更多的事情，因为该请求被设置为拒绝访问，建议直接修改该请求，不要重试该请求。')
    , 'INTERNALSERVERERROR': (500, '表明服务端能被请求访问到，但是不能理解用户的请求。')
    , 'SERVICEUNAVAILABLE': (503, '被请求的服务无效。建议直接修改该请求，不要重试该请求。')
}
aom_status_code_succeed_key = ['OK']
aom_status_code_succeed_code = [c for k, (c, d) in aom_status_code.items() if k in aom_status_code_succeed_key]

status_code = {
    ('post_iam_get_token', 'SUCCEED'): [201]
    , ('post_cci_create_deployment', 'SUCCEED'): cci_status_code_succeed_code
    , ('delete_cci_delete_deployment', 'SUCCEED'): cci_status_code_succeed_code
    , ('get_cci_get_create_job', 'SUCCEED'): cci_status_code_succeed_code
    , ('get_cci_get_namespace_job', 'SUCCEED'): cci_status_code_succeed_code
    , ('get_cci_get_specific_job', 'SUCCEED'): cci_status_code_succeed_code
    , ('get_cci_get_specific_job_status', 'SUCCEED'): cci_status_code_succeed_code
    , ('delete_cci_delete_specific_job', 'SUCCEED'): cci_status_code_succeed_code
    , ('delete_cci_delete_jobs', 'SUCCEED'): cci_status_code_succeed_code
    , ('post_cci_create_ingress', 'SUCCEED'): cci_status_code_succeed_code
    , ('get_cci_get_ingress_list', 'SUCCEED'): cci_status_code_succeed_code
    , ('get_cci_get_pod_list', 'SUCCEED'): cci_status_code_succeed_code
    , ('get_cci_get_pod_info', 'SUCCEED'): cci_status_code_succeed_code
    , ('post_cci_create_service', 'SUCCEED'): cci_status_code_succeed_code
    , ('delete_cci_delete_service', 'SUCCEED'): cci_status_code_succeed_code
    , ('get_iam_get_project_id', 'SUCCEED'): [200]
    , ('get_ecs_get_availability_zone', 'SUCCEED'): ecs_status_code_succeed_code
    , ('get_ecs_get_ssh_list', 'SUCCEED'): ecs_status_code_succeed_code
    , ('get_vpc_get_vpc_list', 'SUCCEED'): vpc_status_code_succeed_code
    , ('get_vpc_get_subnet_list', 'SUCCEED'): vpc_status_code_succeed_code
    , ('get_eps_get_ente_proj_list', 'SUCCEED'): eps_status_code_succeed_code
    , ('get_ims_get_image_list', 'SUCCEED'): ims_status_code_succeed_code
    , ('get_swr_get_image_list', 'SUCCEED'): swr_status_code_succeed_code
    , ('post_aom_get_monitoring_data', 'SUCCEED'): aom_status_code_succeed_code
    , ('post_aom_get_indicator', 'SUCCEED'): aom_status_code_succeed_code
}

# local config
# region_name = 'cn-south-1'
region_name = 'cn-east-3'
availability_zone = {'cn-south-1': []}
service_with_project_token = ["vpc", "ims", "aom"]
endpoint = {
    "iam": "iam.cn-south-1.myhuaweicloud.com"
    , "cci": "cci.cn-south-1.myhuaweicloud.com"
    # , "cci": "cci.cn-east-3.myhuaweicloud.com"
    , "ecs": "ecs.cn-south-1.myhuaweicloud.com"
    , "vpc": "vpc.cn-south-1.myhuaweicloud.com"
    , "eps": "eps.myhuaweicloud.com"
    , "ims": "ims.cn-south-1.myhuaweicloud.com"
    , "swr": "swr-api.cn-south-1.myhuaweicloud.com"
    # , "swr": "swr-api.cn-east-3.myhuaweicloud.com"
    , "aom": "aom.cn-south-1.myhuaweicloud.com"
    # , "aom": "aom.cn-east-3.myhuaweicloud.com"
}

cci_namespace = 'cci-afm-prod'
# cci_namespace = 'cci-afm-test'
swr_namespace = 'dq-test'


def main():
    get_huawei_token(refresh=True)
    depl_mesg = post_cci_create_deployment(endpoint=endpoint['cci'], namespace=cci_namespace)
    # delete_cci_delete_deployment(endpoint=endpoint['cci']
    #                              , namespace=cci_namespace
    #                              # , name=depl_mesg['metadata']['name']
    #                              , name="deployment-test-200804-151921"
    #                              , by_way='bg')
    # get_cci_get_create_job(endpoint=endpoint['cci'], namespace=cci_namespace)
    # get_cci_get_namespace_job(endpoint=endpoint['cci'], namespace=cci_namespace)
    # get_cci_get_specific_job(endpoint=endpoint['cci'], namespace=cci_namespace, name='job-test-210105-102902-noexist')
    # get_cci_get_specific_job_status(endpoint=endpoint['cci'], namespace=cci_namespace, name='cci-job-20201211')
    # delete_cci_delete_specific_job(endpoint=endpoint['cci'], namespace=cci_namespace, name='cci-job-20211141', by_way="fg")
    # delete_cci_delete_jobs(endpoint=endpoint['cci'], namespace=cci_namespace, by_way="fg")
    # post_cci_create_ingress(endpoint=endpoint['cci'], namespace=cci_namespace)
    # get_cci_get_ingress_list(endpoint=endpoint['cci'], namespace=cci_namespace)
    # get_cci_get_pod_list(endpoint=endpoint['cci'], namespace=cci_namespace, condition={'labelSelector': {'name': 'calculationtask-66-1742fc3c513', 'server': 'javajupyterhub'}})
    # get_cci_get_pod_info(endpoint=endpoint['cci'], namespace=cci_namespace, pod_name='test')
    # get_cci_get_pod_info(endpoint=endpoint['cci'], namespace=cci_namespace, pod_name=pod_name)
    # serv_mesg = post_cci_create_service(endpoint=endpoint['cci'], namespace=cci_namespace)
    # delete_cci_delete_service(endpoint=endpoint['cci'], namespace=cci_namespace, name=serv_mesg['metadata']['name'])
    # get_iam_get_project_id()
    # project_id = get_huawei_region_project_id(region_name=region_name)
    # get_ecs_get_ssh_list(endpoint=endpoint['ecs'], project_id=project_id)
    # get_ecs_get_availability_zone(endpoint=endpoint['ecs'], project_id=project_id)
    # get_vpc_get_vpc_list(endpoint=endpoint['vpc'], project_id=project_id)
    # get_vpc_get_subnet_list(endpoint=endpoint['vpc'], project_id=project_id)
    # get_eps_get_ente_proj_list(endpoint=endpoint['eps'])
    # get_ims_get_image_list(endpoint=endpoint['ims'], project_id=project_id)
    # get_swr_get_image_list(endpoint['swr'], namespace='dq-test')
    # post_aom_get_monitoring_data(endpoint=endpoint['aom'], project_id=project_id, fill_value='null', deployment_name='notebooktask-d5nb5173-17800121971')
    # post_aom_get_monitoring_data(endpoint=endpoint['aom'], project_id=project_id, fill_value='null', deployment_name=depl_mesg['metadata']['name'])
    # post_aom_get_indicator(endpoint=endpoint['aom'], project_id=project_id, type='', limit=1000, start=0)


def get_resp_content_with_status_check(comm, resp):
    if resp.status_code in status_code[comm, 'SUCCEED']:
        mesg = json.loads(resp.content)
    else:
        print(comm, resp.content)
        mesg = None

    return mesg


# IAM token
def get_huawei_token(refresh=False):
    if refresh \
            or not hasattr(get_huawei_token, 'token') \
            or not hasattr(get_huawei_token, 'expire_time') \
            or not get_huawei_token.token \
            or not get_huawei_token.expire_time \
            or now_is_expired(get_huawei_token.expire_time):
        token_mesg, token, expire_time = load_token(), None, None
        if token_mesg:
            token, expire_time = decompose_token(token_mesg)
        if refresh or token_mesg is None or token is None or expire_time is None or now_is_expired(expire_time):
            token_mesg = post_iam_get_token(endpoint=endpoint['iam'])
            if not token_mesg:
                return None, None

            save_token(token_mesg)
            token, expire_time = decompose_token(token_mesg)
        # None may assign to token and expire_time
        get_huawei_token.token, get_huawei_token.expire_time = token, expire_time

    # return get_huawei_token.token, get_huawei_token.expire_time
    return get_huawei_token.token


def now_is_expired(expire_time):
    return datetime.now().astimezone() > expire_time.astimezone() - timedelta(minutes=1)


def post_iam_get_token(endpoint):
    uri = f'/v3/auth/tokens'
    url = f'https://{endpoint}{uri}'
    headers = {'Content-Type': 'application/json;charset=utf8'}

    # dict_data = {
    #     "auth": {
    #         "identity": {
    #             "methods": ["password"],
    #             "password": {
    #                 "user": {
    #                     "name": "hw13258492",
    #                     "password": "Dq20201020",
    #                     "domain": {
    #                         "name": "hw13258492"
    #                     }
    #                 }
    #             }
    #         },
    #         "scope": {
    #             "project": {
    #                 "name": "cn-east-3"
    #             },
    #             # "project": {
    #             #     "name": "cn-south-1"
    #             # },
    #             # "domain": {
    #             #     "name": "hw13258492"
    #             # }
    #         }
    #     }
    # }
    dict_data = {"auth": {"identity": {"methods": ["password"], "password": {
        "user": {"name": "hw83457760", "password": "Dq20201020", "domain": {"name": "hw83457760"}}}},
                          "scope": {"project": {"name": "cn-south-1"}}}}
    #
    # with open('huaweiyun_token_param.json', mode='w', encoding='utf-8') as f:
    #     json.dump(dict_data, f)

    resp = rq.post(url, data=json.dumps(dict_data), headers=headers)

    mesg = get_resp_content_with_status_check(sys._getframe().f_code.co_name, resp)

    if mesg:
        mesg["token"]["X-Subject-Token"] = resp.headers["X-Subject-Token"]

    return mesg


def load_token():
    if not os.path.exists(token_file):
        return None

    token_mesg = None
    with open(token_file, mode="r", encoding="utf-8") as f:
        token_mesg = json.load(f)

    return token_mesg


def save_token(token_mesg):
    # token_mesg["token"]["X-Subject-Token"] = token
    try:
        with open(token_file, mode='w', encoding='utf-8') as f:
            json.dump(token_mesg, f)
    except OSError:
        os.remove(token_file)


def decompose_token(token_mesg):
    token = token_mesg["token"]["X-Subject-Token"]
    expire_time = datetime.strptime(token_mesg["token"]["expires_at"], "%Y-%m-%dT%H:%M:%S.%fZ").replace(
        tzinfo=timezone.utc).astimezone()
    return token, expire_time


# CCI deployment
def post_cci_create_deployment(endpoint, namespace):  # OK
    business_condition = {'image': 'location:version', 'cpu': "1", 'memory': '1Gi', 'vol': 's1:d1:mode, s2:d2:mode',
                          'net': 'ip:port'}

    uri = f'/apis/apps/v1/namespaces/{namespace}/deployments'
    url = f'https://{endpoint}{uri}'
    headers = {'Content-Type': 'application/json;charset=utf8'
        , "X-Auth-Token": get_huawei_token()}

    # sample redis
    #     dict_data = {
    #         "apiVersion": "apps/v1",
    #         "kind": "Deployment",
    #         "metadata": {
    #             "name": f"deployment-test-{datetime.now().strftime('%y%m%d-%H%M%S')}"
    #         },
    #         "spec": {
    #             "replicas": 1,
    #             "selector": {
    #                 "matchLabels": {
    #                     "app": "redis"
    #                 }
    #             },
    #             "template": {
    #                 "metadata": {
    #                     "labels": {
    #                         "app": "redis"
    #                     }
    #                 },
    #                 "spec": {
    #                     "containers": [
    #                         {
    #                             "image": "redis",
    #                             "name": "container-0",
    #                             "resources": {
    #                                 "limits": {
    #                                     "cpu": "500m",
    #                                     "memory": "1024Mi"
    #                                 },
    #                                 "requests": {
    #                                     "cpu": "500m",
    #                                     "memory": "1024Mi"
    #                                 }
    #                             }
    #                         }
    #                     ],
    #                     "imagePullSecrets": [
    #                         {
    #                             "name": "imagepull-secret"
    #                         }
    #                     ],
    #                     "priority": 0
    #                 }
    #             }
    #         }
    #     }

    volume_name = "cci-sfs-import-prod"
    # volume_name = "cci-sfs-import-kd5rdq1g-mshx"
    dict_data = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": f"deployment-test-{datetime.now().strftime('%y%m%d-%H%M%S')}"
        },
        "spec": {
            "replicas": 1,  # number of pod instance
            "selector": {
                "matchLabels": {  # 选择的标签
                    "app": "dq-notebook-check-test"
                }
            },
            "template": {
                "metadata": {
                    "labels": {  # 标签用来选择控制器或服务等
                        "app": "dq-notebook-check-test"
                    }
                },
                "spec": {
                    "volumes": [
                        {
                            "name": volume_name,
                            "persistentVolumeClaim": {  # 拟挂载文件服务声明
                                "claimName": volume_name
                            }
                        }
                    ],
                    "containers": [
                        {
                            "image": "swr.cn-east-3.myhuaweicloud.com/digquant/dq_notebook:1.4-prod",  # 镜像地址
                            "name": "container-0",  # 容器运行名称
                            "resources": {
                                "limits": {
                                    "cpu": "500m",
                                    "memory": "1Gi"
                                },
                                "requests": {
                                    "cpu": "500m",
                                    "memory": "1Gi"
                                }

                                # "limits": {
                                #     "cpu": "500m",
                                #     "memory": "1024Mi"
                                # },
                                # "requests": {
                                #     "cpu": "500m",
                                #     "memory": "1024Mi"
                                # }
                            },
                            "volumeMounts": [
                                {
                                    "name": volume_name,  # 挂载的文件服务名称
                                    "mountPath": "/afm/input/",  # 目标文件系统中挂载路径
                                    "subPath": "afm/ResultSet/ModelOptimization",  # 文件服务的字路径
                                    "readOnly": True
                                },
                                # {
                                #     "name": "cci-sfs-import-kbrl90nz-7vhz",
                                #     "mountPath": "/afm/working/call_qr_code.py",
                                #     "subPath": "afm/call_qr_code.py",
                                #     "readOnly": False
                                # },
                                {
                                    "name": volume_name,
                                    "mountPath": "/afm/working",
                                    "subPath": "afm/dq_afm",
                                    "readOnly": False
                                },
                            ],
                        }
                    ],
                    "imagePullSecrets": [
                        {
                            "name": "imagepull-secret"
                        }
                    ],
                    "priority": 0
                }
            }
        }
    }

    resp = rq.post(url, data=json.dumps(dict_data), headers=headers)

    mesg = get_resp_content_with_status_check(sys._getframe().f_code.co_name, resp)

    return mesg


def delete_cci_delete_deployment(endpoint, namespace, name, by_way):  # OK
    # test for using Orphan still lose the Pod
    # there is no ReplicaSet in HUAWEI CCI
    delete_method = {
        "only": "Orphan"  # only delete deployment but not ReplicaSet and Pod
        , "fg": "Foreground"  # delete order Pod->ReplicaSet->Deployment
        , "bg": "Background"  # delete order Deployment->ReplicaSet->Pod
    }
    if by_way not in delete_method:
        raise NotImplementedError

    uri = f'/apis/apps/v1/namespaces/{namespace}/deployments/{name}'
    url = f'https://{endpoint}{uri}'
    headers = {'Content-Type': 'application/json;charset=utf8'
        , "X-Auth-Token": get_huawei_token()}

    dict_data = {
        "Kind": "DeleteOptions",
        "apiVersion": "v1",
        "propagationPolicy": delete_method[by_way]
    }

    resp = rq.delete(url, data=json.dumps(dict_data), headers=headers)

    mesg = get_resp_content_with_status_check(sys._getframe().f_code.co_name, resp)

    return mesg


def get_cci_get_create_job(endpoint=endpoint['cci'], namespace=cci_namespace):
    uri = f'/apis/batch/v1/namespaces/{namespace}/jobs'
    url = f'https://{endpoint}{uri}'
    headers = {'Content-Type': 'application/json;charset=utf8'
        , "X-Auth-Token": get_huawei_token()}

    name = f"job-test-{datetime.now().strftime('%y%m%d-%H%M%S')}"

    dict_data = {
        "apiVersion": "batch/v1",
        "kind": "Job",
        "metadata": {
            "name": name,
            # "namespace": namespace
        },
        "spec": {
            "backoffLimit": 0,
            "completions": 1,
            "parallelism": 1,
            "template": {
                "metadata": {
                    "name": name
                },
                "spec": {
                    "volumes": [
                        {
                            "name": "cci-sfs-import-test",
                            "persistentVolumeClaim": {
                                "claimName": "cci-sfs-import-test"
                            },
                        }
                    ],
                    "containers": [
                        {
                            "name": name,
                            "image": "swr.cn-east-3.myhuaweicloud.com/dq-test/python-atrader:0.0.2",  # 镜像地址
                            "resources": {
                                "limits": {
                                    "cpu": "500m",
                                    "memory": "1024Mi"
                                },
                                "requests": {
                                    "cpu": "500m",
                                    "memory": "1024Mi"
                                }
                            },
                            "volumeMounts": [
                                {
                                    "name": "cci-sfs-import-test",  # 挂载的文件服务名称
                                    "mountPath": "/tmp/the_test/",  # 目标文件系统中挂载路径
                                    "subPath": "",  # 文件服务的字路径
                                    "readOnly": False
                                },
                            ],
                            # "command": [
                            #     "python3",
                            #     "/tmp/the_testfffff/test/test.py",
                            # ],
                            "command": [
                                "/bin/bash",
                                "-c",
                                "while true; do echo hello; sleep 10; done",
                            ],
                        }
                    ],
                    "imagePullSecrets": [
                        {
                            "name": "imagepull-secret"
                        }
                    ],
                    "restartPolicy": "Never",
                    "priority": 0,
                    "hostAliases": [
                        {"hostnames": ["dqdata-alpha.digquant.com"],
                         "ip": "192.168.3.178"},
                    ],
                }
            }
        }
    }

    resp = rq.post(url, data=json.dumps(dict_data), headers=headers)

    mesg = get_resp_content_with_status_check(sys._getframe().f_code.co_name, resp)

    return mesg


def get_cci_get_namespace_job(endpoint, namespace):
    uri = f'/apis/batch/v1/namespaces/{namespace}/jobs'
    url = f'https://{endpoint}{uri}'
    headers = {'Content-Type': 'application/json;charset=utf8'
        , "X-Auth-Token": get_huawei_token()}

    dict_data = {}

    resp = rq.get(url, data=json.dumps(dict_data), headers=headers)

    mesg = get_resp_content_with_status_check(sys._getframe().f_code.co_name, resp)

    return mesg


def get_cci_get_specific_job(endpoint, namespace, name):
    uri = f'/apis/batch/v1/namespaces/{namespace}/jobs/{name}'
    url = f'https://{endpoint}{uri}'
    headers = {'Content-Type': 'application/json;charset=utf8'
        , "X-Auth-Token": get_huawei_token()}

    dict_data = {}

    resp = rq.get(url, data=json.dumps(dict_data), headers=headers)

    mesg = get_resp_content_with_status_check(sys._getframe().f_code.co_name, resp)

    return mesg


def get_cci_get_specific_job_status(endpoint, namespace, name):
    uri = f'/apis/batch/v1/namespaces/{namespace}/jobs/{name}/status'
    url = f'https://{endpoint}{uri}'
    headers = {'Content-Type': 'application/json;charset=utf8'
        , "X-Auth-Token": get_huawei_token()}

    dict_data = {}

    resp = rq.get(url, data=json.dumps(dict_data), headers=headers)

    mesg = get_resp_content_with_status_check(sys._getframe().f_code.co_name, resp)

    return mesg


def delete_cci_delete_specific_job(endpoint, namespace, name, by_way='only'):
    delete_method = {
        "only": "Orphan"  # only delete Job but not Pod
        , "fg": "Foreground"  # delete order Pod->Job
        , "bg": "Background"  # delete order Job->Pod
    }
    if by_way not in delete_method:
        raise NotImplementedError

    uri = f'/apis/batch/v1/namespaces/{namespace}/jobs/{name}'
    url = f'https://{endpoint}{uri}'
    headers = {'Content-Type': 'application/json;charset=utf8'
        , "X-Auth-Token": get_huawei_token()}

    dict_data = {
        "Kind": "DeleteOptions",
        "apiVersion": "v1",
        "propagationPolicy": delete_method[by_way]
    }

    resp = rq.delete(url, data=json.dumps(dict_data), headers=headers)

    mesg = get_resp_content_with_status_check(sys._getframe().f_code.co_name, resp)

    return mesg


def delete_cci_delete_jobs(endpoint, namespace, by_way='only'):
    delete_method = {
        "only": "Orphan"  # only delete Job but not Pod
        , "fg": "Foreground"  # delete order Pod->Job
        , "bg": "Background"  # delete order Job->Pod
    }
    if by_way not in delete_method:
        raise NotImplementedError

    uri = f'/apis/batch/v1/namespaces/{namespace}/jobs'
    url = f'https://{endpoint}{uri}'
    headers = {'Content-Type': 'application/json;charset=utf8'
        , "X-Auth-Token": get_huawei_token()}

    dict_data = {
        "Kind": "DeleteOptions",
        "apiVersion": "v1",
        "propagationPolicy": delete_method[by_way]
    }

    resp = rq.delete(url, data=json.dumps(dict_data), headers=headers)

    mesg = get_resp_content_with_status_check(sys._getframe().f_code.co_name, resp)

    return mesg


# TODO
# use that when we want to access to the notebook into the docker with http protocol, and services together for LoadBalancer
# TCP can just use services for ClusterIP
def post_cci_create_ingress(endpoint, namespace):
    business_condition = {}

    uri = f'/apis/extensions/v1beta1/namespaces/{namespace}/ingresses'
    url = f'https://{endpoint}{uri}'
    headers = {'Content-Type': 'application/json;charset=utf8'
        , "X-Auth-Token": get_huawei_token()}

    dict_data = {
        "apiVersion": "extensions/v1beta1",
        "kind": "Ingress",
        "metadata": {
            "name": "dq-notebook",
            "labels": {
                "app": "dq-notebook"
            },
            "annotations": {
                # from huawei elb
                "kubernetes.io/elb.id": "f3cb9dcb-4756-4e54-9754-711dc715ec43",
                "kubernetes.io/elb.ip": "124.70.188.170",
                "kubernetes.io/elb.port": "7777"
            }
        },
        "spec": {
            "rules": [
                {
                    "http": {
                        "paths": [
                            {
                                "path": "/",
                                "backend": {
                                    "serviceName": "dq-notebook-ingress",
                                    "servicePort": 8080
                                }
                            }
                        ]
                    }
                }
            ]
        }
    }

    resp = rq.post(url, data=json.dumps(dict_data), headers=headers)

    mesg = get_resp_content_with_status_check(sys._getframe().f_code.co_name, resp)

    return mesg


def get_cci_get_ingress_list(endpoint, namespace):
    uri = f'/apis/extensions/v1beta1/namespaces/{namespace}/ingresses'
    url = f'https://{endpoint}{uri}'
    headers = {'Content-Type': 'application/json;charset=utf8'
        , "X-Auth-Token": get_huawei_token()}

    dict_data = {}

    resp = rq.get(url, data=json.dumps(dict_data), headers=headers)

    mesg = get_resp_content_with_status_check(sys._getframe().f_code.co_name, resp)

    return mesg


def get_cci_get_pod_list(endpoint, namespace, condition):
    """
    get the pod list by condition
    notice may can't get the whole info of pod just after create deployment
    :param endpoint:
    :param namespace:
    :param condition:
    :return:
    """

    condition = {k: [k_ + '=' + v_ for k_, v_ in v.items()] if isinstance(v, dict) else str(v) for k, v in
                 condition.items()}

    uri = f'/api/v1/namespaces/{namespace}/pods'
    url = f'https://{endpoint}{uri}'
    headers = {'Content-Type': 'application/json;charset=utf8'
        , "X-Auth-Token": get_huawei_token()}

    dict_data = {}

    resp = rq.get(url, data=json.dumps(dict_data), headers=headers, params=condition)

    mesg = get_resp_content_with_status_check(sys._getframe().f_code.co_name, resp)

    return mesg


def get_cci_get_pod_info(endpoint, namespace, pod_name):
    uri = f'/api/v1/namespaces/{namespace}/pods/{pod_name}'
    url = f'https://{endpoint}{uri}'
    headers = {'Content-Type': 'application/json;charset=utf8'
        , "X-Auth-Token": get_huawei_token()}

    dict_data = {}

    resp = rq.get(url, data=json.dumps(dict_data), headers=headers)

    mesg = get_resp_content_with_status_check(sys._getframe().f_code.co_name, resp)

    return mesg


def post_cci_create_service(endpoint, namespace):  # OK
    business_condition = {}

    uri = f'/api/v1/namespaces/{namespace}/services'
    url = f'https://{endpoint}{uri}'
    headers = {'Content-Type': 'application/json;charset=utf8'
        , "X-Auth-Token": get_huawei_token()}

    dict_data = {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {
            "name": f"service-test-{datetime.now().strftime('%y%m%d-%H%M%S')}",
            "annotations": {  # outside service parameter
                "kubernetes.io/elb.id": "f3cb9dcb-4756-4e54-9754-711dc715ec43",  # elb service
                "kubernetes.io/elb.ip": "192.168.0.2",  # elb 内部 ip
                "tenant.kubernetes.io/project-id": "0883a8954680f5032f78c018f4771a96",
                # same as the one we use in other function
                "tenant.kubernetes.io/domain-id": "0883a8963e80f2921f5ac0186355e191"  # the id in account info page
            },
            "labels": {  # object label
                "app": "dq-notebook-check-test"
            }
        },
        "spec": {
            "selector": {  # select the specific label object for load balance
                "app": "dq-notebook-check-test"
            },
            "ports": [  # the exposed port parameter of service
                {
                    "name": f"ports-test-{datetime.now().strftime('%y%m%d-%H%M%S')}",
                    "targetPort": 8888,  # docker 内部使用的端口
                    "port": 2345,  # 外网端口
                    "protocol": "TCP"
                }
            ],
            "type": "LoadBalancer"
        }
    }

    resp = rq.post(url, data=json.dumps(dict_data), headers=headers)

    mesg = get_resp_content_with_status_check(sys._getframe().f_code.co_name, resp)

    return mesg


def delete_cci_delete_service(endpoint, namespace, name):  # OK
    uri = f'/api/v1/namespaces/{namespace}/services/{name}'
    url = f'https://{endpoint}{uri}'
    headers = {'Content-Type': 'application/json;charset=utf8'
        , "X-Auth-Token": get_huawei_token()}

    dict_data = {}

    resp = rq.delete(url, data=json.dumps(dict_data), headers=headers)

    mesg = get_resp_content_with_status_check(sys._getframe().f_code.co_name, resp)

    return mesg


# project_id
def get_iam_get_project_id():
    uri = f'/v3/projects'
    url = f'https://iam.myhuaweicloud.com{uri}'  # every endpoint return all project_id
    headers = {'Content-Type': 'application/json;charset=utf8'
        , "X-Auth-Token": get_huawei_token()}

    dict_data = {}

    resp = rq.get(url, data=json.dumps(dict_data), headers=headers)

    mesg = get_resp_content_with_status_check(sys._getframe().f_code.co_name, resp)

    return mesg


def get_huawei_region_project_id(region_name):  # OK
    project_mesg = get_iam_get_project_id()
    if not project_mesg:
        return None
    dict_proj = {proj['name']: proj['id'] for proj in project_mesg.get('projects', [])}
    return dict_proj.get(region_name, None)


# ECS server
# TODO
def post_ecs_create_server(project_id):
    uri = f'/v1/{project_id}/cloudservers'
    url = f'https://ecs.cn-south-1.myhuaweicloud.com{uri}'
    headers = {'Content-Type': 'application/json;charset=utf8'
        , "X-Auth-Token": get_huawei_token()}

    dict_data = {
        "server": {
            "availability_zone": "cn-south-1a",  # TODO
            "name": f"server-test-{datetime.now().strftime('%y%m%d-%H%M%S')}",
            "imageRef": "1189efbf-d48b-46ad-a823-94b942e2a000",  # TODO
            "root_volume": {
                "volumetype": "SATA"
            },
            "data_volumes": [
                {
                    "volumetype": "SATA",
                    "size": 100,
                    "multiattach": True,
                    "hw:passthrough": True
                }
            ],
            "flavorRef": "s6.small.1",
            "vpcid": "f739345c-6d0b-4ace-9ed8-6c2dc87cdfd7",  # TODO
            "security_groups": [
                {
                    "id": "92d12392-af90-439c-8520-0ed0aacdc7e1"  # TODO
                }
            ],
            "nics": [
                {
                    "subnet_id": "6b429d41-8e63-4665-a369-2d0d9ee37d08"  # TODO
                }
            ],
            "publicip": {
                "eip": {
                    "iptype": "5_bgp",
                    "bandwidth": {
                        "size": 10,
                        "sharetype": "PER"
                    }
                }
            },
            "key_name": "sshkey-123",  # TODO
            "count": 1,
            "extendparam": {
                "enterprise_project_id": "0"  # get_eps_get_ente_proj_list
            },
            "server_tags": [
                {
                    "key": "key1",
                    "value": "value1"
                }
            ],
            "metadata": {
                "op_svc_userid": "8ea65f4099ba412883e2a0da72b96873",
                "agency_name": "test"
            }
        }
    }


# TODO bad
def get_ecs_get_availability_zone(endpoint, project_id):
    uri = f'/v2.1/{project_id}/os-availability-zone'
    url = f'https://{endpoint}{uri}'
    headers = {'Content-Type': 'application/json;charset=utf8'
        , "X-Auth-Token": get_huawei_token()}

    dict_data = {}

    resp = rq.get(url, data=json.dumps(dict_data), headers=headers)

    mesg = get_resp_content_with_status_check(sys._getframe().f_code.co_name, resp)

    return mesg


# TODO bad
def get_ecs_get_ssh_list(endpoint, project_id):
    uri = f'/v2.1/{project_id}/os-keypairs'
    url = f'https://{endpoint}{uri}'
    headers = {'Content-Type': 'application/json;charset=utf8'
        , "X-Auth-Token": get_huawei_token()}

    dict_data = {}

    resp = rq.get(url, data=json.dumps(dict_data), headers=headers)

    mesg = get_resp_content_with_status_check(sys._getframe().f_code.co_name, resp)

    return mesg


# VPC server
# TODO bad
def get_vpc_get_vpc_list(endpoint, project_id):
    uri = f'/v1/{project_id}/vpcs'
    url = f'https://{endpoint}{uri}'
    headers = {'Content-Type': 'application/json;charset=utf8'
        , "X-Auth-Token": get_huawei_token()}

    dict_data = {}

    resp = rq.get(url, data=json.dumps(dict_data), headers=headers)

    mesg = get_resp_content_with_status_check(sys._getframe().f_code.co_name, resp)

    return mesg


# TODO bad
def get_vpc_get_subnet_list(endpoint, project_id):
    uri = f'/v1/{project_id}/subnets'
    url = f'https://{endpoint}{uri}'
    headers = {'Content-Type': 'application/json;charset=utf8'
        , "X-Auth-Token": get_huawei_token()}

    dict_data = {}

    resp = rq.get(url, data=json.dumps(dict_data), headers=headers)

    mesg = get_resp_content_with_status_check(sys._getframe().f_code.co_name, resp)

    return mesg


# EPS
# TODO only get 0 for enterprise project id
def get_eps_get_ente_proj_list(endpoint):
    # be careful with this interface sometimes need a new token
    uri = f'/v1.0/enterprise-projects'
    url = f'https://{endpoint}{uri}'
    headers = {'Content-Type': 'application/json;charset=utf8'
        , "X-Auth-Token": get_huawei_token()}

    dict_data = {}

    resp = rq.get(url, data=json.dumps(dict_data), headers=headers)

    mesg = get_resp_content_with_status_check(sys._getframe().f_code.co_name, resp)

    return mesg


# IMS
def get_ims_get_image_list(endpoint, project_id):
    # uri = f'/v2/images'
    uri = f'/v2/images?owner={project_id}'
    url = f'https://{endpoint}{uri}'
    headers = {'Content-Type': 'application/json;charset=utf8'
        , "X-Auth-Token": get_huawei_token()}

    dict_data = {}

    resp = rq.get(url, data=json.dumps(dict_data), headers=headers)

    mesg = get_resp_content_with_status_check(sys._getframe().f_code.co_name, resp)

    return mesg


# SWR
def get_swr_get_image_list(endpoint, namespace):
    # uri = f'/v2/manage/repos?filter=center::self|namespace::{namespace}|name::{name}|category::{category}|offset::{offset}|limit::{limit}|order_column::{order_column}|order_type::{order_type}'
    uri = f'/v2/manage/repos?filter=center::self|namespace::{namespace}'
    url = f'https://{endpoint}{uri}'
    headers = {'Content-Type': 'application/json;charset=utf8'
        , "X-Auth-Token": get_huawei_token()}

    dict_data = {}

    resp = rq.get(url, data=json.dumps(dict_data), headers=headers)

    mesg = get_resp_content_with_status_check(sys._getframe().f_code.co_name, resp)

    return mesg


# AOM
def post_aom_get_monitoring_data(endpoint, project_id, fill_value, deployment_name):  # OK
    business_condition = {'fill_value'}

    fill_value_range = [-1, 0, 'null', 'average']
    if fill_value not in fill_value_range:
        raise NotImplementedError

    uri = f'/v1/{project_id}/ams/metricdata?fillValue={fill_value}'  # fillValue default is -1 when I missed that
    url = f'https://{endpoint}{uri}'
    headers = {'Content-Type': 'application/json;charset=utf8'
        , "X-Auth-Token": get_huawei_token()}

    # 用 pod 名称获取
    # dict_data = {
    #     "metrics": [
    #         {
    #             "namespace": "PAAS.CONTAINER",
    #             "metricName": "cpuCoreLimit",  # CPU内核总量
    #             "dimensions": [
    #                 {
    #                     "name": "podName",
    #                     "value": "cci-deployment-20206302-74658df469-gwbt9"
    #                 }
    #             ]
    #         },
    #         {
    #             "namespace": "PAAS.CONTAINER",
    #             "metricName": "cpuCoreUsed",  # CPU内核占用
    #             "dimensions": [
    #                 {
    #                     "name": "podName",
    #                     "value": "cci-deployment-20206302-74658df469-gwbt9"
    #                 }
    #             ]
    #         },
    #         {
    #             "namespace": "PAAS.CONTAINER",
    #             "metricName": "cpuUsage",  # CPU使用率
    #             "dimensions": [
    #                 {
    #                     "name": "podName",
    #                     "value": "cci-deployment-20206302-74658df469-gwbt9"
    #                 }
    #             ]
    #         },
    #         {
    #             "namespace": "PAAS.CONTAINER",
    #             "metricName": "memCapacity",  # 物理内存总量
    #             "dimensions": [
    #                 {
    #                     "name": "podName",
    #                     "value": "cci-deployment-20206302-74658df469-gwbt9"
    #                 }
    #             ]
    #         },
    #         {
    #             "namespace": "PAAS.CONTAINER",
    #             "metricName": "memUsed",  # 物理内存使用量
    #             "dimensions": [
    #                 {
    #                     "name": "podName",
    #                     "value": "cci-deployment-20206302-74658df469-gwbt9"
    #                 }
    #             ]
    #         },
    #         {
    #             "namespace": "PAAS.CONTAINER",
    #             "metricName": "memUsage",  # 物理内存使用率
    #             "dimensions": [
    #                 {
    #                     "name": "podName",
    #                     "value": "cci-deployment-20206302-74658df469-gwbt9"
    #                 }
    #             ]
    #         },
    #         {
    #             "namespace": "PAAS.CONTAINER",
    #             "metricName": "filesystemCapacity",  # 文件系统容量
    #             "dimensions": [
    #                 {
    #                     "name": "podName",
    #                     "value": "cci-deployment-20206302-74658df469-gwbt9"
    #                 }
    #             ]
    #         },
    #         {
    #             "namespace": "PAAS.CONTAINER",
    #             "metricName": "filesystemAvailable",  # 文件系统可用
    #             "dimensions": [
    #                 {
    #                     "name": "podName",
    #                     "value": "cci-deployment-20206302-74658df469-gwbt9"
    #                 }
    #             ]
    #         },
    #         {
    #             "namespace": "PAAS.CONTAINER",
    #             "metricName": "filesystemUsage",  # 文件系统使用率  # TODO
    #             "dimensions": [
    #                 {
    #                     "name": "podName",
    #                     "value": "cci-deployment-20206302-74658df469-gwbt9"
    #                 }
    #             ]
    #         }
    #         ,{
    #             "namespace": "PAAS.CONTAINER",
    #             "metricName": "recvBytesRate",  # 下行Bps
    #             "dimensions": [
    #                 {
    #                     "name": "podName",
    #                     "value": "cci-deployment-20206302-74658df469-gwbt9"
    #                 }
    #             ]
    #         }
    #     ],
    #     "period": 60,  # 分钟级
    #     "timerange": "-1.-1.5",  # 最近五分钟
    #     "statistics": [
    #         "maximum",
    #         "minimum",
    #         "sum"
    #     ]
    # }
    # 用 deployment 名称获取
    dict_data = {
        "metrics": [
            {
                "namespace": "PAAS.CONTAINER",
                "metricName": "cpuCoreLimit",  # CPU内核总量
                "dimensions": [
                    {
                        "name": "deploymentName",
                        "value": deployment_name
                    }
                ]
            },
            {
                "namespace": "PAAS.CONTAINER",
                "metricName": "cpuCoreUsed",  # CPU内核占用
                "dimensions": [
                    {
                        "name": "deploymentName",
                        "value": deployment_name
                    }
                ]
            },
            {
                "namespace": "PAAS.CONTAINER",
                "metricName": "cpuUsage",  # CPU使用率
                "dimensions": [
                    {
                        "name": "deploymentName",
                        "value": deployment_name
                    }
                ]
            },
            {
                "namespace": "PAAS.CONTAINER",
                "metricName": "memCapacity",  # 物理内存总量
                "dimensions": [
                    {
                        "name": "deploymentName",
                        "value": deployment_name
                    }
                ]
            },
            {
                "namespace": "PAAS.CONTAINER",
                "metricName": "memUsed",  # 物理内存使用量
                "dimensions": [
                    {
                        "name": "deploymentName",
                        "value": deployment_name
                    }
                ]
            },
            {
                "namespace": "PAAS.CONTAINER",
                "metricName": "memUsage",  # 物理内存使用率
                "dimensions": [
                    {
                        "name": "deploymentName",
                        "value": deployment_name
                    }
                ]
            },
            {
                "namespace": "PAAS.CONTAINER",
                "metricName": "filesystemCapacity",  # 文件系统容量
                "dimensions": [
                    {
                        "name": "deploymentName",
                        "value": deployment_name
                    }
                ]
            },
            {
                "namespace": "PAAS.CONTAINER",
                "metricName": "filesystemAvailable",  # 文件系统可用
                "dimensions": [
                    {
                        "name": "deploymentName",
                        "value": deployment_name
                    }
                ]
            },
            {
                "namespace": "PAAS.CONTAINER",
                "metricName": "filesystemUsage",  # 文件系统使用率  # TODO
                "dimensions": [
                    {
                        "name": "deploymentName",
                        "value": deployment_name
                    }
                ]
            },
            {
                "namespace": "PAAS.CONTAINER",
                "metricName": "recvBytesRate",  # 下行Bps
                "dimensions": [
                    {
                        "name": "deploymentName",
                        "value": deployment_name
                    }
                ]
            }
        ],
        "period": 60,  # 分钟级
        "timerange": "-1.-1.5",  # 最近五分钟
        "statistics": [
            "maximum",
            "minimum",
            "sum"
        ]
    }

    resp = rq.post(url, data=json.dumps(dict_data), headers=headers)

    mesg = get_resp_content_with_status_check(sys._getframe().f_code.co_name, resp)

    return mesg


def post_aom_get_indicator(endpoint, project_id, type, limit=1000, start=0):
    business_condition = {'fill_value'}

    if not (0 < limit <= 1000):
        raise NotImplementedError
    if not (start >= 0):
        raise NotImplementedError

    uri = f'/v1/{project_id}/ams/metrics?type={type}&limit={limit}&start={start}'
    # uri = f'/v1/{project_id}/ams/metrics?limit={limit}&start={start}'
    url = f'https://{endpoint}{uri}'
    headers = {'Content-Type': 'application/json;charset=utf8'
        , "X-Auth-Token": get_huawei_token()}

    dict_data = {
        "metricItems": [
            {
                "namespace": "PAAS.CONTAINER",
                "dimensions": [
                    {
                        "name": "appName",
                        "value": "demo"
                    },
                    {
                        "name": "clusterName",
                        "value": "test"
                    }
                ]
            }
        ]
    }

    resp = rq.post(url, data=json.dumps(dict_data), headers=headers)

    mesg = get_resp_content_with_status_check(sys._getframe().f_code.co_name, resp)

    return mesg


if __name__ == "__main__":
    main()
