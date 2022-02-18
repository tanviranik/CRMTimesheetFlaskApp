from docxtpl import DocxTemplate, InlineImage
from io import BytesIO
from models import GetContextEmployeePayStub
import os
from docx2pdf import convert
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
import base64

def from_template(template_path, employee_id, startdate, enddate):
    template = DocxTemplate(template_path)
    context = GetContextEmployeePayStub(employee_id, startdate, enddate)  # gets the context used to render the document
    if len(context) == 0:
        return None

    total_pay = round(float(context[0]['total_pay']), 2)
    income_tax = round(total_pay * 0.1, 2)
    cpp = round(total_pay * 0.02, 2)
    ei = round(total_pay * 0.01, 2)
    deductions = round(income_tax + cpp + ei, 2)
    
    net_pay = round(total_pay - deductions, 2)
    result =  {
        'EmployeeId': context[0]['employee_id'],
        'EmployeeName': context[0]['employee_name'],
        'EmployeeAddress': context[0]['employee_address'],
        'City': context[0]['city'],
        'Province': context[0]['province'],
        'ZipCode': context[0]['postalcode'],
        'PayDate': str(context[0]['paydate']),
        'PayPeriodStartDate': str(context[0]['startdate']),
        'PayPeriodEndDate': str(context[0]['enddate']),
        'Hrs': round(float(context[0]['total_hours']), 2),
        'R1': round(float(context[0]['hourly_rate']),2),
        'P3': "${:,.2f}".format(total_pay),
        'AccountNumberLast4': context[0]['bank_account'],
        'tax': "${:,.2f}".format(income_tax),
        'cpp': "${:,.2f}".format(cpp),
        'ei': "${:,.2f}".format(ei),
        'taxt': "${:,.2f}".format(deductions),
        'NetPay': "${:,.2f}".format(net_pay),
        'H1': round(float(context[0]['total_hours']),2),
        'H2': '-',
        'H3': '-',

        'R2': '-',
        'R3': '-',
        'P1': "${:,.2f}".format(total_pay),
        'P2': '-',
        'P3': '-',
        'Y1': '-',
        'Y2': '-',
        'Y3': '-'
    }
    target_file = BytesIO()
    template.render(result)
    template.save(target_file)
    return target_file

def generate_document(template_source_path, template_filename, employee_id, startdate, enddate):
    document = from_template(os.path.join(template_source_path, template_filename), employee_id, startdate, enddate)
    if document is None:
        return None
        
    date_time_str = datetime.now().strftime('%Y%m%d%H%M%S')
    generated_docx_filename = template_filename.split('.')[0] + '_' + date_time_str + '.' + template_filename.split('.')[1]
    generated_pdf_filename = template_filename.split('.')[0] + '_' + date_time_str + '.pdf'
    with open( os.path.join(template_source_path, generated_docx_filename), "wb") as f:
        f.write(document.getbuffer())
    convert(os.path.join(template_source_path, generated_docx_filename), os.path.join(template_source_path, generated_pdf_filename))
    return generated_pdf_filename

def send_employee_paystub_attaced(to_email, filename):
    return
