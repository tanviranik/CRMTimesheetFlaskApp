from flask import Flask, render_template, session, request, redirect, url_for, jsonify
from modules import convert_to_dict, make_ordinal
from models import GetProjects, GetEmplyees, insert_employee_data
from flask_cors import CORS

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

# first route

@app.route('/')
def index():
    return render_template('index.html', pairs=pairs_list, the_title="Presidents Index")


@app.route('/timesheet')
def timesheet():
    return render_template('timesheet.html', the_title="Ai DOM - Time Sheet", weektitle="")

@app.route('/report')
def reportpage():
    return render_template('report.html', the_title="Ai DOM - Reports", weektitle="")

@app.route("/get_projects", methods=['GET'])
def get_projects():
    projects = GetProjects()
    response = jsonify({'status_code' : 200, 'data': projects})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/get_employees", methods=['GET'])
def get_employees():
    employees = GetEmplyees()
    response = jsonify({'status_code' : 200, 'data': employees})
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


# keep this as is
if __name__ == '__main__':
    app.run(debug=True)
