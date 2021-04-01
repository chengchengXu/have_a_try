# coding: utf-8

import os
import numpy as np
import pandas as pd
import atrader as at

output_data_folder = 'k_factor'
output_csv_name = 'game_data.csv'
data_base_year = 2017
data_year = [2018, 2019]


def main():
    make_game_data()


def convert_to_normal_code(x):
    if x.endswith('.SZ'):
        return 'szse.' + x.replace('.SZ', '')
    if x.endswith('.SH'):
        return 'sse.' + x.replace('.SH', '')
    if x.startswith('szse.'):
        return x
    print('[Warning] Unknown code:', x)
    return x


def extract_code():
    # column
    # random_num, code_num, code
    file_code = '基础数据latest1.csv'
    df_code = pd.read_csv(file_code, encoding='GBK')
    df_code = df_code.rename(columns={'股票编号': 'code_num'})
    df_code['code'] = df_code['code'].map(convert_to_normal_code)
    # print(df_code)
    # df_code = df_code[0:3]  # for test
    return df_code


def extract_factor_by_file1():
    csv_factor = 'factor.csv'
    txt_factor = 'export_factor_list.txt'
    df_factor = pd.read_csv(csv_factor, encoding='utf-8')
    list_factor = [x.strip() for x in open(txt_factor, mode='r', encoding='utf-8').readlines()]
    set_factor = set(list_factor)
    if len(set_factor) != len(list_factor):
        print('Not match factor number for list', len(list_factor), 'set', len(set_factor))
    diff = set_factor - set(df_factor['remarks'])
    if len(diff):
        print(diff)
    df_factor = df_factor[df_factor.remarks.isin(list_factor)]

    # assign bad factor
    # 'InformationRatio120','120日信息比率'
    # 'CashFlowPS','每股现金流量净额'
    # 'TORPS','每股营业总收入'
    df_factor = df_factor.append([{'name': 'InformationRatio120', 'factorNo': 'InformationRatio120', 'remarks': '120日信息比率'}
                      , {'name': 'CashFlowPS', 'factorNo': 'CashFlowPS', 'remarks': '每股现金流量净额'}
                      , {'name': 'TORPS', 'factorNo': 'TORPS', 'remarks': '每股营业总收入'}]
                     , ignore_index=True)
    print(df_factor)
    return df_factor


def extract_factor_by_file2():
    csv_factor = '因子列表.csv'
    df_factor = pd.read_csv(csv_factor, encoding='GBK')
    df_factor = df_factor.rename(columns={'因子代码': 'factorNo', '因子名称': 'remarks'})
    return df_factor


def extract_factor():
    # column
    # factorNo, remarks
    return extract_factor_by_file2()


def make_game_data():
    if not output_csv_name or not output_data_folder:
        raise NotImplementedError
    if not (data_base_year and data_year and all([1990 <= data_base_year <= y <= 2100 for y in data_year])):
        raise NotImplementedError
    df_factor = extract_factor()
    df_code = extract_code()

    print('Prepare already, loading configuration finished')

    # get k data and factor data to self csv
    raw_data = acquire_k_factor_data(data_year, set(df_code['code']), list(df_factor['factorNo']))

    print('Acquire k data and factor data finished')

    # combine data to one
    game_data = combine_convert_data(raw_data, df_code, df_factor)

    print('Combine and convert data finished')

    # data to file
    file_path = os.path.join(os.getcwd(), output_data_folder, output_csv_name)
    game_data.to_csv(path_or_buf=file_path, encoding='utf-8', index=False, mode='w')

    print('Output csv data file finished, see the file path', file_path)


def acquire_k_factor_data(acquire_year, set_code, list_f):
    folder_data = os.path.join(os.getcwd(), output_data_folder)
    data = dict()
    for y in acquire_year:
        folder_year = os.path.join(folder_data, str(y))
        if not os.path.isdir(folder_year):
            os.makedirs(folder_year)
        b_date = '%d-01-01'%y
        e_date = '%d-12-31'%y

        for tid in set_code:

            file_path = os.path.join(folder_year, '%s_%d.csv' % (tid, y))
            if os.path.isfile(file_path):
                s_data = pd.read_csv(file_path, encoding='utf-8')

            else:
                kdata = at.get_kdata(target_list=[tid], frequency='day', fre_num=1, begin_date=b_date, end_date=e_date, fq=at.enums.FQ_FORWARD, fill_up=True, df=True, sort_by_date=True)
                fdata = at.get_factor_by_code(factor_list=list_f, target=tid, begin_date=b_date, end_date=e_date)

                kdata = kdata.rename(columns={'time': 'k_time'})
                kdata['date'] = kdata['k_time'].map(lambda x: x.date())
                fdata = fdata.rename(columns={'date': 'factor_time'})
                fdata['date'] = fdata['factor_time'].map(lambda x: x.date())
                s_data = pd.merge(kdata, fdata, on='date', how='left')

                # save
                s_data.to_csv(path_or_buf=file_path, encoding='utf-8')

            data[(y, tid)] = s_data
            print('Acquired data for (%d, %s)' % (y, tid))

    return data


def combine_convert_data(raw_datas, df_code, df_factor):
    df_code = df_code.set_index('code')
    for (y, tid), raw_data in raw_datas.items():
        # add code_num random_num
        raw_data['code_num'] = df_code.at[tid, 'code_num']
        raw_data['random_num'] = df_code.at[tid, 'random_num']
    # combine data
    data = pd.concat([raw_data for (y, tid), raw_data in raw_datas.items()])
    # split date to several column
    date = data['date'].map(lambda x: str(x).split('-'))
    data['year'] = [int(d[0]) - data_base_year for d in date]
    data['month'] = [int(d[1]) for d in date]
    data['day'] = [int(d[2]) for d in date]
    # convert column name
    normal_map = {
        'code_num': '股票编号'
        , 'random_num': '随机编码'
        , 'code': '股票代码'
        , 'year': '年'
        , 'month': '月'
        , 'day': '日'
        , 'open': '开盘价'
        , 'high': '最高价'
        , 'low': '最低价'
        , 'close': '收盘价'
        , 'volume': '成交量'
        , 'amount': '成交金额'
    }
    # order will random when go below python 3.6
    base_order = ['code_num', 'random_num', 'code', 'year', 'month', 'day', 'open', 'high', 'low', 'close', 'volume', 'amount']
    order = base_order + [getattr(f, 'factorNo') for f in df_factor.itertuples(index=True, name='Pandas')]
    data = data[order]
    data = data.rename(columns={getattr(f, 'factorNo'): getattr(f, 'remarks')
                                for f in df_factor.itertuples(index=True, name='Pandas')})
    data = data.rename(columns=normal_map)
    return data


if __name__ == "__main__":
    main()
