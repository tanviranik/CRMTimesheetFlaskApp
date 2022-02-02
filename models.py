import pyodbc
from datetime import datetime
from datetime import date

CONN_STR = "Driver={ODBC Driver 17 for SQL Server};Server=13.68.246.119;Database=CRM;uid=sa;pwd=dataport;Trusted_Connection=no;"

def dictfetchall(cur):
    dataset = cur.fetchall()
    columns = [col[0] for col in cur.description]
    return [
        dict(zip(columns, row))
        for row in dataset
        ]

def ParseFloat(value):
    #print(value)
    if value is None or value == '':
        return 0
    return float(value)

def ParseString(value):
    if value is None or value == '':
        return ''

def GetProjects():
    conn = pyodbc.connect(CONN_STR)
    cursor = conn.cursor()
    query = """SELECT [project_id]
                ,[project_name]
                ,[site_location]
                ,[is_active]
                ,[start_date]
            FROM [dbo].[Project]"""

    cursor.execute(query)
    data = dictfetchall(cursor)
    cursor.close()
    conn.close()
    return data

def GetEmplyees():
    conn = pyodbc.connect(CONN_STR)
    cursor = conn.cursor()
    query = """SELECT [employee_id]
                ,[employee_name]
                ,[title]
                ,[joining_date]
                ,cast([hourly_rate] as float) as hourly_rate
                ,[username]
                ,[password]
                ,[email]
            FROM [dbo].[Employee]"""

    cursor.execute(query)
    data = dictfetchall(cursor)
    cursor.close()
    conn.close()
    return data

def insert_employee_data(employee_name, title, joining_date, hourly_rate, username, password, email):
    try:
        datarow = [employee_name, title, joining_date, hourly_rate, username, password, email]
        conn = pyodbc.connect(CONN_STR)
        cursor = conn.cursor()
        sql_command = ("""INSERT INTO [dbo].[Employee]
                            (
                            [employee_name]
                            ,[title]
                            ,[joining_date]
                            ,hourly_rate
                            ,[username]
                            ,[password]
                            ,[email]
                            ) 
                        VALUES (?,?,?, ?, ?,?,?)""") 
        cursor.execute(sql_command, datarow) 
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print('Exception occured : ', e, '. For Datarow: ', datarow)