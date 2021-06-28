import pdfkit
import sys
from sqlalchemy import inspect
from app.models import Api
from app import app, db, requests_helper
from flask import render_template, flash, redirect, url_for, request, session
from json import JSONDecodeError
from datetime import date

def render_html():

    reportData = db.session.query(Api).all()
    print('data is ' + str(reportData), file=sys.stderr)

    try:
        s = Api.query.all()
        apipass = 0
        apifail = 0
        apiwip = 0
        apitotal = 0
        for x in s:
            requesttype = Api.get_requesttype(x)
            apiurl = Api.get_apiurl(x)
            apidata = Api.get_apidata(x)
            response = requests_helper.perform_request(requesttype, apiurl, apidata)
            try:
                if response.status_code < 300:
                    apipass += 1
                    apitotal += 1
                else:
                    apifail += 1
                    apitotal += 1
                Api.set_responsecode(x, response.status_code)
                Api.set_response(x, response.json())
                Api.set_reason(x, response.reason)
            except AttributeError:
                apiwip += 1
            except JSONDecodeError:
                Api.set_response(x, "{}")
        apisuccess = "{:.2f}".format((apipass / apitotal)*100)
    except UnboundLocalError:
        return render_template('index.html', title='Home')

    html_path = f'app/pdf/apiReport_'+get_date()+'.html'
    html_file = open(html_path, 'w')
    html_file.write(render_template('layout.html', title='API List', data=reportData, apipass=apipass, apifail=apifail, apitotal=apitotal, apisuccess=apisuccess, apiwip=apiwip))
    html_file.close()
    print(f"Now converting apiReport ... ")
    pdf_path = f'app/pdf/apiReport_'+get_date()+'.pdf'
    html2pdf(html_path, pdf_path)


def html2pdf(html_path, pdf_path):
    """
    Convert html to pdf using pdfkit which is a wrapper of wkhtmltopdf
    """
    path_wk = r"C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wk)
    options = {
        'page-size': 'Letter',
        'margin-top': '0.35in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None,
        'enable-local-file-access': None
    }
    with open(html_path) as f:
        pdfkit.from_file(f, pdf_path, options=options, configuration=config)
        # pdfkit.from_file(f, pdf_path, options=options)



def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


def get_date():
    "Get today's date in German format"
    today = date.today()
    return today.strftime("%d.%m.%Y")