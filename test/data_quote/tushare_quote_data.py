import tushare as ts

if __name__ == '__main__':
    ts.set_token('7ac46604fbe6fc854980b29f29336a3f96db1c68fd27e5de32977399')
    pro = ts.pro_api()
    df = pro.daily(ts_code='000333.SZ', start_date='20160101', end_date='20191231')

    df.rename(columns={'trade_date': 'datetime', 'vol': 'volume'}, inplace=True)
    df['datetime'] = df['datetime'].map(lambda x: f'{x[:4]}-{x[4:6]}-{x[6:]}')

    df.to_csv('tushare.csv')
    print(df.head())
