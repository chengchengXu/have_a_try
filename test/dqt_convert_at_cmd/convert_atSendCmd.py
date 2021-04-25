# coding: utf-8

import os
import re


def get_imports_and_func(input_file, interface):
    with open(input_file, mode='r', encoding='utf-8') as f:
        lines = f.readlines()
    funcs = {}
    func_name = None
    f_l = []
    in_func = False
    imports = []
    for line in lines:
        if line.startswith(r'import ') or line.startswith(r'from '):
            imports.append(line)
        if line.startswith(r"#"):
            continue
        if line.startswith(r'def '):
            if in_func:
                funcs[func_name] = f_l
                func_name = None
                in_func = False
            result = re.search(r"(?<=def atSendCmd)\w+", line)
            if result:
                func_name = 'ATrader' + result.group(0)
                if func_name in interface:
                    in_func = True
                    f_l = [line]
                else:
                    func_name = None
            continue
        if in_func:
            f_l.append(line)

    if in_func:
        funcs[func_name] = f_l
        func_name = None
        in_func = False
    [print(f"{func} not found") for func in interface if func not in funcs.keys()]
    return (imports, funcs)


def convert_func(if_type, func, lines):
    c_name = func.replace('ATrader', '')
    tab = ' ' * 4
    enter = '\n'
    in_comment = False
    before_send = []
    after_send = []
    send_param = []
    send_lines_combine = ''
    send = []
    found_send = False
    comment = []
    count_lb = 0
    count_rb = 0
    get_return = False
    for line in lines:
        # def -> class
        if line.startswith(r'def '):
            params = line[line.find('(') + 1: line.find(')')]
            params = [p.strip() for p in params.split(',')] if params else []
            # result = re.search(r"(?<=def )\w+", line)
            c_def = f'class {c_name}({if_type}Server):{enter}'
            uri = f"{tab}_uri = r'{func}'{enter}"
            white_line = f'{enter}'
            init_def = f"{tab}def __init__(self):{enter}"
            # init_content = f'{tab * 2}super().__init__(_uri={c_name}.uri, mode="post", pack={c_name}.pack){enter}'
            continue
        # comment
        line_lstrip = line.lstrip()
        if line_lstrip.startswith(r'"""'):
            comment.append(line)
            if not (line.rstrip().endswith(r'"""') and len(line.strip()) >= 6):
                in_comment = not in_comment
            continue
        if in_comment:
            comment.append(line)
            continue
        # normal line
        if line_lstrip.startswith(r"func_name = 'atSend") \
                or line_lstrip.startswith(r'res = recv_') \
                or line_lstrip.startswith(r'atReturnCh'):
            continue
        if found_send:
            if line_lstrip.startswith(r"return "):
                get_return = True
                continue
            elif len(line_lstrip):
                after_send.append(line)
        elif count_lb != count_rb:
            count_lb += line_lstrip.count('(')
            count_rb += line_lstrip.count(')')
            found_send = count_rb == count_lb
            send_lines_combine += line.strip()
        elif line_lstrip.startswith(r"atserial.ATrader"):
            count_lb += line_lstrip.count('(')
            count_rb += line_lstrip.count(')')
            found_send = count_rb == count_lb
            send_lines_combine = line.strip()
        elif len(line.strip()):
            before_send.append(line)

    real_send = [
        f"{tab}@staticmethod{enter}"
        , f"{tab}def send({''.join([p + ', ' for p in params])}**kwargs):{enter}"
        , f"{tab * 2}if not hasattr({c_name}, 'cmd'):{enter}"
        , f"{tab * 3}{c_name}.cmd = {c_name}(){enter}"
        ,
        f"{tab * 2}return super({c_name}, {c_name}.cmd).send({''.join([p.split(':')[0].split('=')[0] + '=' + p.split(':')[0].split('=')[0] + ', ' for p in params])}**kwargs){enter}"
        , white_line
    ]
    pack = []
    if before_send \
            or send_lines_combine[send_lines_combine.find('(') + 1:send_lines_combine.rfind(')')] != ', '.join(params):
        pack = [f"{tab}@staticmethod{enter}"
            , f"{tab}def pack(kwargs):{enter}"
            , f'{tab * 2}"""{enter}'
            , f'{tab * 2}{send_lines_combine}{enter}' if send_lines_combine else f''
            , f'{enter}' if send_lines_combine and before_send else ''
            , *[f'{tab}{l}' for l in before_send]
            , f'{tab * 2}"""{enter}'
            , f"{tab * 2}return json.dumps(kwargs){enter}"
            , white_line]
    unpack = []
    if after_send or not get_return:
        unpack = [f"{tab}@staticmethod{enter}"
            , f"{tab}def unpack(kwargs):{enter}"
            , f'{tab * 2}"""{enter}'
            , *[f'{tab}{l}' for l in after_send]
            , f'{enter}' if after_send else f''
            , f'{tab * 2}Some return{enter}' if get_return else f'{tab * 2}Nothing return{enter}'
            , f'{tab * 2}"""{enter}'
            , f"{tab * 2}return json.loads(kwargs){enter}"
            , white_line]
    init_pack = f', pack={c_name}.pack' if pack else ''
    init_unpack = f', unpack={c_name}.unpack' if unpack else ''
    init_content = f'{tab * 2}super().__init__(uri={c_name}._uri, mode="post"{init_pack}{init_unpack}){enter}'
    if comment:
        comment.append(white_line)

    new_lines = [
        *[c_def, *comment, uri, white_line]
        , *[init_def, init_content, white_line]
        , *real_send
        , *pack
        , *unpack
        , white_line
    ]
    return new_lines


def prepare_header(if_type, imports):
    enter = '\n'
    tab = '    '
    import_str = f''.join(imports)
    header = [
        f'# coding: utf-8{enter}'
        f'{enter}'
        f'import json{enter}'
        f'from .basecmd import HttpBaseCmd{enter}'
        f'{import_str}'
        f'{enter}'
        f'{enter}'
        f'class {if_type}Server(HttpBaseCmd):{enter}'
        f'{tab}_endpoint = "{if_type}Server"{enter}'
        f'{enter}'
        f'{tab}def __init__(self, uri, **kwargs):{enter}'
        f'{tab * 2}super().__init__(url=f"http://{{{if_type}Server._endpoint}}{{uri}}", **kwargs){enter}'
        f'{enter}'
        f'{enter}'
    ]
    return header


def convert_funcs(if_type, funcs):
    new_funcs = {func: convert_func(if_type, func, lines) for func, lines in funcs.items()}
    # new_funcs = funcs
    return new_funcs


def save_func(if_type, output_file, header, new_funcs):
    lines = header + sum([f_lines for f_lines in new_funcs.values()], [])
    with open(output_file, mode='w', encoding='utf-8') as f:
        f.writelines(lines)


def const_choice():
    return {
        'DataAPI': [
            "ATraderGetCodeList",
            "ATraderGetCodeListSet",
            "ATraderGetFutureContracts",
            "ATraderGetFutureInfo",  # not exist
            "ATraderGetFutureInfo_20190920",
            "ATraderCheckSubscribeNum",
            "ATraderGetKDataMulti",
            "ATraderGetNKDataMulti",
            "ATraderGetKData",
            "ATraderGetTradingDays",
            "ATraderGetTradingTime",
            "ATraderGetCurTradeDate",
            "ATraderGetPreTradeDate",
            "ATraderGetCurDate",
            "ATraderTransTradeTimeToTradeDate",
            "ATraderGetRtData",
            "ATraderGetTDPData",
            "ATraderGetTDPDataMulti",
            "ATraderGetHistorySet",
            "ATraderGetFundamentalSet",
            "ATraderGetFundamentalSet2",
            "ATraderGetRiskModelSet",
            "ATraderGetMarketSet",
            "ATraderFdmtFieldInfo",
            "ATraderRiskModelFieldInfo",
            "ATraderGetFactor",
            "ATraderGetTargetIns",
            "ATraderGetTargetIns_20190830",
            "ATraderGetHistoryInstruments",
            "ATraderGetFutureInfoExculusively",
            "ATraderGetFutureInfoExculusively_20190918",
            "ATraderGetStockInfoExculusively",
            "ATraderGetTradingDaysByCondition",
            "ATraderBarTime",
            "ATraderConvertTargets",
            "ATraderGetAllFutureIndex",  # not exist
        ],
        'TradeAPI': [
            "ATraderSTTradeGetAccountList",
            "ATraderSTTRadeGetAccountHandle",
            "ATraderSTGetAccountPosition",
            "ATraderIsAccountValid",
            "ATraderCloseOperation",
            "ATraderGetAccountCash",
            "ATraderGetAccountTargetGrossPosition",
            "ATraderGetAccountPositionAndCashInfo",
            "ATraderSTGetAccountInfo",
            "ATraderSTTradeOperation",
            "ATraderCancelOrder",
            "ATraderGetOrderInfo",
            "ATraderGetOrderInfoByDate",
            "ATraderGetUnFinishedOrderInfo",
            "ATraderGetLastOrderInfo",
            "ATraderGetDailyExecution",
            "ATraderGetLastExecution",
            "ATraderSTTradeStopOrder",
            "ATraderGetStopOrderInfo",  # not exist
            "ATraderGetStopOrderInfo3_1_4",
            "ATraderCancelStopOrder",
            "ATraderCancelFrozen",
        ],
        'TaskAPI': [
            "ATraderCreateTaskRealTrade",
            "ATraderStartTaskRealTrade",
            "ATraderStopTaskRealTrade",
            "ATraderCreateTaskBackTest",
            "ATraderStartTaskBackTest",
            "ATraderStopTaskBackTest",
            "ATraderCreateTaskRunFactor",
            "ATraderStartTaskRunFactor",
            "ATraderStopTaskRunFactor",
            "ATraderGetBackTestPerformance",
            "ATraderRiseError",
            "ATraderPutLog",
        ]
    }


def convert_atcmd_class_file():
    ifs = const_choice()
    if_type = 'TaskAPI'  # 'TradeAPI', 'TaskAPI', 'DataAPI'
    interface = ifs[if_type]
    input_file = 'atcmd.py'
    output_file = f"{if_type.lower()}.py"

    imports, funcs = get_imports_and_func(input_file, interface)
    header = prepare_header(if_type, imports)
    new_funcs = convert_funcs(if_type, funcs)
    save_func(if_type, output_file, header, new_funcs)
    pass


def replace_file_atcmd_with_api(f_str):
    ifs = const_choice()
    rep_dict = {v.replace("ATrader", "atcmd.atSendCmd"): (k, f'{k.lower()}.{v.replace("ATrader", "")}.send') for k, vs in ifs.items() for v in vs}
    match_type = set()
    result = re.findall(r'atcmd.atSendCmd\w+', f_str)
    for res in sorted(set(result), reverse=True):
        if res not in rep_dict.keys():
            print(f'{res} not found')
            continue
        match_type.add(rep_dict[res][0])
        f_str = f_str.replace(res, rep_dict[res][1])
    return f_str, match_type


def convert_atcmd_class_invoke():
    ifs = const_choice()
    proj_folder = r'E:\Workdir_trunk_git\Toolbox\PythonToolBox'
    # proj_folder = r'E:\Workdir_trunk_git\Toolbox\PythonToolBox\atrader\api\history'

    for root, dirs, files in os.walk(proj_folder, topdown=True):
        # print(root)
        # print(dirs)
        # print(files)
        if not len(files):
            continue
        for file in files:
            if not file.endswith('.py'):
                continue
            with open(os.path.join(root, file), mode='r', encoding='utf-8') as f:
                f_str = f.read()
            # remove atcmd
            # add trade | data | task
            f_str, match_type = replace_file_atcmd_with_api(f_str)
            result = re.findall(r'.*import atcmd\s', f_str)
            if len(match_type):
                if len(result):
                    for res in set(result):
                        f_str = f_str.replace(res, ''.join([res.replace(r'atcmd', t.lower()) for t in match_type]))
                else:
                    f_str = ''.join([f'from atrader.tframe.comm import {t.lower()}\n' for t in match_type]) + f_str
            else:
                if len(result):
                    for res in set(result):
                        f_str = f_str.replace(res, '')
                else:
                    continue
            with open(os.path.join(root, file), mode='w', encoding='utf-8') as f:
                f.write(f_str)

    # walk all py file
    # convert atcmd.atSendCmd to xxxapi.yyy.send

    pass


def test():
    ifs = const_choice()
    rep_dict = {v.replace("ATrader", "atcmd.atSendCmd"): (k, f'{k.lower()}.{v.replace("ATrader", "")}.send') for k, vs
                in ifs.items() for v in vs}
    pass


def main():
    # convert_atcmd_class()
    convert_atcmd_class_invoke()
    # test()
    pass


if __name__ == "__main__":
    main()
