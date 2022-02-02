import pyodbc
from datetime import datetime
from datetime import date

CONN_STR = "Driver={ODBC Driver 17 for SQL Server};Server=13.68.246.119;Database=CRM;uid=sa;pwd=dataport;Trusted_Connection=no;"

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
        x = []
        for key in jsonData:
            x.append(jsonData[key])
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
        for x in range(0, array_no):
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
            return str(e)

    def BatchInsertIntoTable(self, tablename, tableproperties, array_no, data):
        cursor = self.connection.cursor()
        dataarray = self.ConvertJsonListToArrayList(data)
        print(dataarray)
        myvalues = '('
        for x in range(0, array_no):
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
            print(e)
            return str(e)

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

    # def GetProjects():
    #     conn = pyodbc.connect(CONN_STR)
    #     cursor = conn.cursor()
    #     query = """SELECT [project_id]
    #                 ,[project_name]
    #                 ,[site_location]
    #                 ,[is_active]
    #                 ,[start_date]
    #             FROM [dbo].[Project]"""

    #     cursor.execute(query)
    #     data = dictfetchall(cursor)
    #     cursor.close()
    #     conn.close()
    #     return data

    # def GetTasks():
    #     cursor = self.connection.cursor()
    #     query = """SELECT * FROM [dbo].[Task]"""

    #     cursor.execute(query)
    #     data = dictfetchall(cursor)
    #     cursor.close()
    #     conn.close()
    #     return data

    # def GetCategories():
    #     cursor = self.connection.cursor()
    #     query = """SELECT * FROM [dbo].[Category]"""

    #     cursor.execute(query)
    #     data = dictfetchall(cursor)
    #     cursor.close()
    #     conn.close()
    #     return data