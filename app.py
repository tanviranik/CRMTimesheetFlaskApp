from flask import Flask, render_template, session, request, redirect, url_for, jsonify
from modules import convert_to_dict, make_ordinal
# from models import GetProjects, GetEmplyees, insert_employee_data, GetTasks, GetCategories, insert_hour_logs

from models import DataContext
from flask_cors import CORS
import json
import datetime

# app = Flask(__name__, template_folder='template')
app = Flask(__name__)
application = app

CORS(app)

from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)


# create a list of dicts from a CSV
presidents_list = convert_to_dict("presidents.csv")

# create a list of tuples in which the first item is the number
# (Presidency) and the second item is the name (President)
pairs_list = []
for p in presidents_list:
    pairs_list.append( (p['Presidency'], p['President']) )

hourlogs_tbl_pros = '([employee_id],[task_id],[category_id],[notes],[insert_date],[entry_date],[start_time],[end_time],[total_hours])'
category_tbl_pros = '([category_name])'
employee_tbl_pros = '([employee_name],[title],[joining_date],cast([hourly_rate] as float) as hourly_rate,[username],[password],[email])'
project_tbl_pros = '([project_name],[site_location],[is_active],[start_date])'
task_tbl_pros = '([task_id],[category_id],[notes],[insert_date],[entry_date],[start_time],[end_time],[total_hours])'
inventory_tbl_pros = '([inventory_name],[quantity],[unit],[hourlog_id])'
hourlog_table = '[dbo].[HourLogs]'
inventory_table = '[dbo].[InventoryTracker]'
weekpaystub_table = '[dbo].[WeekPayStub]'

# first route

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', pairs=pairs_list, the_title="Presidents Index")

@app.route('/timesheet')
def timesheet():
    return render_template('timesheet.html', the_title="Ai DOM - Time Sheet", weektitle="")

@app.route('/newtimesheet')
def newtimesheet():
    selecteddate = request.args.get('selecteddate')
    hourlog_id = 0
    return render_template('new_timesheet_entry.html', the_title="Ai DOM - New Entry", start_date=selecteddate, hourlog_id=hourlog_id)

@app.route('/edittimesheet')
def edittimesheet():
    selecteddate = ''
    hourlog_id = request.args.get('hourlog_id')
    return render_template('new_timesheet_entry.html', the_title="Ai DOM - Edit Entry", start_date=selecteddate, hourlog_id=hourlog_id)

@app.route('/save_timesheet', methods=['POST', 'GET'])
def save_timesheet():
    dbcontext = DataContext('x','x','x','x')
    dbcontext.Connect()
    global data
    if request.method == 'POST':
        data = request.json
    #request.form.get('word') edit_timesheet
    # datadict = json.load(data)
    # print(datadict)
    # print(data)
    hourlogdt = data['HourLogs']
    # hourlog_table = '[dbo].[HourLogs]'
    array_no = 9
    result = dbcontext.InsertIntoTable(hourlog_table, hourlogs_tbl_pros, array_no, hourlogdt)
    
    if result != '1':
        dbcontext.Disconnect()
        response = jsonify(GetResponseMessage(result))
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    # InventoryTracker
    # print(data["InventoryTracker"])
    # inventory = json.dumps(data["InventoryTracker"])
    # print(inventory)    
    inventorydt = data['InventoryTracker']
    # print(hourlog)
    if len(inventorydt) > 0:
        hourlog = dbcontext.GetByFilter(hourlog_table, 1, '' ,'order by hourlog_id desc')[0]
        for dt in inventorydt:
            dt['hourlog_id'] = hourlog['hourlog_id']
        print(inventorydt)
        # inventory_table = '[dbo].[InventoryTracker]'
        result = dbcontext.BatchInsertIntoTable(inventory_table, inventory_tbl_pros, 4, inventorydt)
    dbcontext.Disconnect()
    response = jsonify(GetResponseMessage(result))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/edit_timesheet', methods=['POST', 'GET'])
def edit_timesheet():
    dbcontext = DataContext('x','x','x','x')
    dbcontext.Connect()
    global data
    if request.method == 'POST':
        data = request.json
    hourlogdt = data['HourLogs']
    # print(hourlogdt)
    result = dbcontext.UpdateIntoTableById(hourlog_table, hourlogdt)
    
    if result != '1':
        dbcontext.Disconnect()
        response = jsonify(GetResponseMessage(result))
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    inventorylist = data['InventoryTracker']
    if len(inventorylist) > 0:        
        for inventory in inventorylist:
            if inventory['inventory_tracker_id'] > 0:
                # update command here
                result = dbcontext.UpdateIntoTableById(inventory_table, inventory)
            else:
                #inser command here
                inventory['hourlog_id'] = hourlogdt['hourlog_id']                
                result = dbcontext.InsertIntoTable(inventory_table, inventory_tbl_pros, 4, inventory)
    removeinventorylist = data['RemovedInventories']
    if len(removeinventorylist) > 0:        
        for remove_inventory in removeinventorylist:
            delete_clause = "inventory_tracker_id = " + str(remove_inventory['inventory_tracker_id'])
            result = dbcontext.DeleteFromTableById(inventory_table, delete_clause)
    dbcontext.Disconnect()
    # result = '1'
    response = jsonify(GetResponseMessage(result))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/deletetimesheet', methods=['GET'])
def deletetimesheet():
    hourlog_id = request.args.get('hourlog_id')
    dbcontext = DataContext('x','x','x','x')
    dbcontext.Connect()
    where_clause = 'hourlog_id = ' + hourlog_id
    result = dbcontext.DeleteFromTableById(inventory_table, where_clause)
    if result == '1':
        result = dbcontext.DeleteFromTableById(hourlog_table, where_clause)
    response = jsonify(GetResponseMessage(result))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/report')
def reportpage():
    return render_template('report.html', the_title="Ai DOM - Reports", weektitle="")

@app.route('/rpthourlogdetail')
def timesheetdetailreport():    
    return render_template('timesheetdetailreport.html', the_title="Reports - Time Sheet Details", weektitle="")

@app.route('/paystub')
def paystub():
    return render_template('paystub.html', the_title="Reports - Pay Stub", weektitle="")

@app.route("/gettimesheetdetail", methods=['GET'])
def gettimesheetdetail():
    dbcontext = DataContext('x','x','x','x')
    dbcontext.Connect()
    filterparams = request.args.get('filterby')
    print(filterparams)
    hourlog = dbcontext.GetDateRangeData(filterparams.startdate, filterparams.enddate, filterparams.emp_id)    
    dbcontext.Disconnect()
    response = json.dumps({'data': hourlog})
    return response

@app.route("/GetPayStubWeek", methods=['GET'])
def GetPayStubWeek():
    dbcontext = DataContext('x','x','x','x')
    dbcontext.Connect()
    columns = "week_id, month_no, CONVERT(VARCHAR(30), startdate, 23) startdate, CONVERT(VARCHAR(30), enddate, 23) enddate, year"
    weeks = dbcontext.GetByFilterWithSelect(weekpaystub_table, 0 , columns, '')
    print(weeks)
    response = json.dumps({'data': weeks})
    return response

@app.route("/get_projects", methods=['GET'])
def get_projects():
    projects = GetProjects()
    response = jsonify({'status_code' : 200, 'data': projects})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/get_hour_log", methods=['GET'])
def get_hour_log():
    hourlog_id = request.args.get('hour_log_id')
    dbcontext = DataContext('x','x','x','x')
    dbcontext.Connect()
    context = {"HourLogs": {}, 'InventoryTracker': []}
    hourlog_selectparam = "hourlog_id,employee_id,task_id, category_id, notes, CONVERT(VARCHAR(30), insert_date, 23) insert_date, CONVERT(VARCHAR(30), entry_date, 23) entry_date, CONVERT(VARCHAR(30), start_time, 24) start_time, CONVERT(VARCHAR(30), end_time, 24) end_time, total_hours"
    where_clause = "where [hourlog_id] = " + hourlog_id
    context['HourLogs'] = dbcontext.GetByFilterWithSelect('[dbo].[HourLogs]', 0, hourlog_selectparam , where_clause)[0]
    # context['HourLogs'] =
    inventory_selectparam = "[inventory_tracker_id],[inventory_name],CONVERT(VARCHAR(30), [quantity]) quantity,[unit],[hourlog_id]"
    context['InventoryTracker'] = dbcontext.GetByFilterWithSelect('[dbo].[InventoryTracker]', 0, inventory_selectparam , where_clause)
    print(context)
    dbcontext.Disconnect()
    # print(context)
    response = json.dumps({'status_code' : 200, 'data': context})
    # response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/get_supporting_data", methods=['GET'])
def get_supporting_data():
    dbcontext = DataContext('x','x','x','x')
    dbcontext.Connect()
    context = {"projectlist": [], 'tasklist': [], 'categorylist': []}    
    context['projectlist'] = dbcontext.GetAll('Project')
    context['tasklist'] = dbcontext.GetAll('Task')
    context['categorylist'] = dbcontext.GetAll('Category')
    dbcontext.Disconnect()
    # print(context)
    response = jsonify({'status_code' : 200, 'data': context})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/get_employees", methods=['GET'])
def get_employees():
    employees = GetEmplyees()
    response = jsonify({'status_code' : 200, 'data': employees})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/GetWeeklyHourLogs", methods=['GET'])
def GetWeeklyHourLogs():
    dbcontext = DataContext('x','x','x','x')
    dbcontext.Connect()
    start_date = request.args.get('startdate')
    end_date = request.args.get('enddate')
    emp_id = request.args.get('emp_id')
    print(start_date)
    print(end_date)
    print(emp_id)
    hourlog = dbcontext.GetDateRangeData(start_date, end_date, emp_id)    
    dbcontext.Disconnect()
    response = jsonify({'status_code' : 200, 'data': hourlog})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/insert_employee", methods=['GET'])
def insert_employee():
    employee_name = request.args.get('employee_name')
    title = request.args.get('title')
    joining_date = request.args.get('joining_date')
    hourly_rate = request.args.get('hourly_rate')
    username = request.args.get('username')
    password = request.args.get('password')
    email = request.args.get('email')

    insert_employee_data(employee_name, title, joining_date, hourly_rate, username, password, email)

    response = jsonify({'status_code' : 200, 'data': [], 'response': 'Successfully inserted into database.'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# second route

@app.route('/president/<num>')
def detail(num):
    try:
        pres_dict = presidents_list[int(num) - 1]
    except:
        return f"<h1>Invalid value for Presidency: {num}</h1>"
    # a little bonus function, imported on line 2 above
    ord = make_ordinal( int(num) )
    return render_template('president.html', pres=pres_dict, ord=ord, the_title=pres_dict['President'])

def GetResponseMessage(msgtype):
    responseMessage = { "MessageType" : 0, "Message": ""}
    if(msgtype == '1'):
        responseMessage['MessageType'] = 1
        responseMessage['Message'] = "Data saved."
    elif(msgtype == '2'):
        responseMessage['MessageType'] = 2
        responseMessage['Message'] = "Save failed."
    else:
        responseMessage['MessageType'] = 3
        responseMessage['Message'] = "Something went wrong"
    return responseMessage

# keep this as is
if __name__ == '__main__':
    app.run(debug=True)
