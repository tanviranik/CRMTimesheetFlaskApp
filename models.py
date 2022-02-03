import pyodbc
from datetime import datetime
from datetime import date

# CONN_STR = "Driver={ODBC Driver 17 for SQL Server};Server=13.68.246.119;Database=CRM;uid=sa;pwd=dataport;Trusted_Connection=no;"
CONN_STR = "Driver={ODBC Driver 17 for SQL Server};Server=SABBIR\SQLEXPRESS;Database=CRM;uid=sa;pwd=sabbir@12#;Trusted_Connection=no;"

class DataContext:
    def __init__(self,servername,databasename,username,password):
        self.servername = servername
        self.databasename = databasename
        self.username = username
        self.password = password

    def Connect(self):
        self.connection =  pyodbc.connect(CONN_STR)

    def Disconnect(self):
        self.connection.close()

    def dictfetchall(self, cur):
        dataset = cur.fetchall()
        columns = [col[0] for col in cur.description]        
        return [
            dict(zip(columns, row))
            for row in dataset
            ]

    def ParseFloat(self, value):
        #print(value)
        if value is None or value == '':
            return 0
        return float(value)

    def ParseString(self, value):
        if value is None or value == '':
            return ''

    def GetEmplyees():
        cursor = self.connection.cursor()
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

    def GetAll(self, tablename, whereclause='', groupby='',orderby=''):
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT * FROM " + tablename + ' ' + whereclause + ' ' + groupby + ' ' + orderby)
            data = self.dictfetchall(cursor)
            cursor.close()
            return data
        except Exception as e:
            print('inside GetAll')
            return str(e)

    def GetByFilter(self, tablename,numbrows = 0, whereclause='',orderby=''):
        cursor = self.connection.cursor()
        try:
            numrowstr = ''
            if numbrows == 0:                
                numrowstr = ''
            else:
                numrowstr = 'TOP(' + str(numbrows) + ')'
            cursor.execute('SELECT ' + numrowstr + ' * FROM ' + tablename + ' ' + whereclause + ' ' + orderby)
            data = self.dictfetchall(cursor)
            cursor.close()
            return data
        except Exception as e:
            print('inside GetByFilter')
            return str(e)
    
    def GetByFilterWithSelect(self, tablename,numbrows = 0,selectparam = '*', whereclause='',orderby=''):
        cursor = self.connection.cursor()
        try:
            numrowstr = ''
            if numbrows == 0:                
                numrowstr = ''
            else:
                numrowstr = 'TOP(' + str(numbrows) + ')'
            cursor.execute('SELECT ' + numrowstr + ' '+ selectparam +' FROM ' + tablename + ' ' + whereclause + ' ' + orderby)
            data = self.dictfetchall(cursor)
            cursor.close()
            return data
        except Exception as e:
            print('inside GetByFilter')
            return str(e)

    def GetAllbyId(self, tablename, idvalue):
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT * FROM " + tablename + ' where id = ' + idvalue)
            data = self.dictfetchall(cursor)
            cursor.close()
            return data
        except Exception as e:
            print('inside GetAllbyId')
            return str(e)

    def ConvertJsonToArray(self,jsonData):
        i=0
        x = []
        for key in jsonData:
            if i>0:
                x.append(jsonData[key])
            i=i+1
        return x
    
    def ConvertJsonListToArrayList(self,jsonData):        
        x = []
        for dt in jsonData:            
            x.append(self.ConvertJsonToArray(dt))            
        return x

    def InsertIntoTable(self, tablename, tableproperties, array_no, data):        
        cursor = self.connection.cursor()
        dataarray = self.ConvertJsonToArray(data)
        myvalues = '('
        for x in range(0, len(dataarray)):
            if x > 0:
                myvalues = myvalues + ','
            myvalues = myvalues + '?'
        myvalues = myvalues + ')'
        try:
            sql = "INSERT INTO "+tablename+" "+tableproperties+" VALUES "+myvalues
            print(sql)
            cursor.execute(sql, dataarray)
            self.connection.commit()
            cursor.close()
            return '1'
        except Exception as e:
            print('inside InsertIntoTable exception')
            print(str(e))
            return '2'

    def BatchInsertIntoTable(self, tablename, tableproperties, array_no, data):
        cursor = self.connection.cursor()
        dataarray = self.ConvertJsonListToArrayList(data)
        print(dataarray)
        myvalues = '('
        for x in range(0, len(dataarray[0])):
            if x > 0:
                myvalues = myvalues + ','
            myvalues = myvalues + '?'
        myvalues = myvalues + ')'
        try:
            sql = "INSERT INTO "+tablename+" "+tableproperties+" VALUES "+myvalues
            cursor.executemany(sql, dataarray)
            self.connection.commit()
            cursor.close()
            return '1'
        except Exception as e:
            print('inside BatchInsertIntoTable exception')
            print(str(e))
            return '2'

    def PrepareUpdateData(self,jsonData):
        i=0
        update_data_set = ""
        where_clause = ""
        for key in jsonData:
            if isinstance(jsonData[key], int):
                jsonData[key] = str(jsonData[key])
            else:
                jsonData[key] = "'" + jsonData[key] + "'"
            if i>1:
                update_data_set = update_data_set + " , "
            if i==0:
                where_clause = " where " + key + " = " + jsonData[key]
            else:
                update_data_set = update_data_set + " " + key + " = " + jsonData[key]
            i=i+1
        return update_data_set + where_clause

    def UpdateIntoTableById(self, tablename, data):        
        cursor = self.connection.cursor()
        updatedata = self.PrepareUpdateData(data)        
        try:
            sql = "Update " + tablename + " set "+ updatedata
            print(sql)
            cursor.execute(sql)
            self.connection.commit()
            cursor.close()
            return '1'
        except Exception as e:
            print('inside update table exception')
            print(str(e))
            return '2'
    
    def DeleteFromTableById(self, tablename, delete_clause):        
        cursor = self.connection.cursor()
        try:
            sql = "delete from " + tablename + " where "+ delete_clause
            cursor.execute(sql)
            self.connection.commit()
            cursor.close()
            return '1'
        except Exception as e:
            print('inside update table exception')
            print(str(e))
            return '2'

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
            cursor.close()
            conn.close()
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

    def Get7DaysData(self, start_date, end_date):
        cursor = self.connection.cursor()
        query = """select h.hourlog_id,h.employee_id,emp.employee_name, h.task_id, tsk.task_name, proj.project_id, proj.project_name,h.category_id, cat.category_name, h.notes, CONVERT(VARCHAR(30), h.insert_date, 23) insert_date, CONVERT(VARCHAR(30), h.entry_date, 23) entry_date, CONVERT(VARCHAR(30), h.start_time, 24) start_time, CONVERT(VARCHAR(30), h.end_time, 24) end_time, h.total_hours  from HourLogs h
 inner join Employee emp on emp.employee_id = h.employee_id
 inner join Task tsk on tsk.task_id = h.task_id
 inner join Project proj on proj.project_id = tsk.project_id
 inner join Category cat on cat.category_id = h.category_id
 where h.entry_date>='"""+start_date+"""' and h.entry_date <= '"""+end_date+"""'"""

        cursor.execute(query)
        data = self.dictfetchall(cursor)
        cursor.close()
        return data
            