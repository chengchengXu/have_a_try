import atrader as at

def get_data(target):
    fre = 'min'
    fre_num = 1
    begin_date = '2015-01-01'
    end_date = '2019-12-31'
    data = at.get_kdata(target_list=[target],
                        frequency=fre,
                        fre_num=fre_num,
                        begin_date=begin_date,
                        end_date=end_date,
                        fq=at.enums.FQ_NA,
                        # fill_up=False,
                        df=True,
                        sort_by_date=False
                        )
    data.rename(columns={'time': 'datetime'}, inplace=True)
    data.to_csv(f'.\\at_data\\{target}.csv', na_rep='0.0')
    print(data.head())


if __name__ == '__main__':
    get_data('SHFE.AG0000')