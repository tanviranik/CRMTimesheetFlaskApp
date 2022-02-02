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

def GetTasks():
    conn = pyodbc.connect(CONN_STR)
    cursor = conn.cursor()
    query = """SELECT * FROM [dbo].[Task]"""

    cursor.execute(query)
    data = dictfetchall(cursor)
    cursor.close()
    conn.close()
    return data

def GetCategories():
    conn = pyodbc.connect(CONN_STR)
    cursor = conn.cursor()
    query = """SELECT * FROM [dbo].[Category]"""

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

def insert_inventory(inventory, last_insert_id):
    try:        
        datarow = [data["employee_id"], data["employee_id"], data["task_id"], data["category_id"], data["notes"], data["insert_date"], data["entry_date"], data["start_time"], data["end_time"]]
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
        last_insert_id = conn.insert_id()        
        cursor.close()
        conn.close()
        insert_inventory(data["InventoryTracker"],last_insert_id)
    except Exception as e:
        print('Exception occured : ', e, '. For Datarow: ', datarow)

def insert_hour_logs(data):
    try:        
        datarow = [data["employee_id"], data["task_id"], data["category_id"], data["notes"], data["insert_date"], data["entry_date"], data["start_time"], data["end_time"], data['total_hours']]
        conn = pyodbc.connect(CONN_STR)
        cursor = conn.cursor()
        sql_command = ("""INSERT INTO [dbo].[HourLogs]
                            (
                            [employee_id]
                            ,[task_id]
                            ,[category_id]
                            ,[notes]
                            ,[insert_date]
                            ,[entry_date]
                            ,[start_time]
                            ,[end_time]
                            ,[total_hours]
                            ) 
                        VALUES (?,?,?, ?, ?,?,?,?,?)""") 
        cursor.execute(sql_command, datarow)
        conn.commit()
        last_insert_id = cursor.fetchone()[0] 
        cursor.close()
        conn.close()
        return last_insert_id
    except Exception as e:
        print('Exception occured : ', e, '. For Datarow: ', datarow)

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