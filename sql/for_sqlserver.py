import pyodbc
import pandas as pd

server = '10.86.168.132'
database = 'TLDB'
username = 'extrac_reader'
password = 'Ocsevn2SQL'
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = conn.cursor()

## test 1 good
# cursor.execute("SELECT @@version;")
# row = cursor.fetchone()
# while row:
#     print(row[0])
#     row = cursor.fetchone()

## test 2 good
# cursor.execute(
#     """
#     SELECT top 100 * FROM [dbo].[fund_indic_info]
#     """
# )
# print(cursor)
#
# for row in cursor:
#     print(row)

## test 3 good
sql_query = pd.read_sql_query('SELECT top 100 * FROM [dbo].[fund_indic_info]', conn)
print(sql_query)
print(type(sql_query))
sql_query.to_csv('test.csv', index=False, encoding='utf-8')

