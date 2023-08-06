import pandas as __pd
import pyodbc as __odbc

def csv (a_file,a_separator=',') :
    return __pd.read_csv(a_file,a_separator)    

def odbc (a_dsn,a_userid,a_password,a_sql) :
    loc_conn = __odbc.connect('DSN=' + a_dsn + ';UID=' + a_userid + ';PWD=' + a_password)
    return __pd.read_sql(a_sql,loc_conn)

def txt (a_file,a_separator=',') :
    return __pd.read_csv(a_file,a_separator)    

def xls (a_file,a_sheet) :
    return __pd.read_excel(a_file,sheet_name=a_sheet)

