from pip._vendor import requests
from app import db
from app.models import Api


def perform_request(requesttype, requesturl, requestdata):
    if requesttype == 'Get':
        try:
            response = requests.get(requesturl, requestdata)
            return response
        except:
            response = requests.get(requesturl, requestdata).text
            return response
    elif requesttype == 'Post':
        try:
            response = requests.post(requesturl, requestdata)
            return response
        except:
            response = requests.post(requesturl, requestdata).text
            return response
    elif requesttype == 'Put':
        try:
            response = requests.put(requesturl, requestdata)
            return response
        except:
            response = requests.put(requesturl, requestdata).text
            return response
    elif requesttype == 'Delete':
        try:
            response = requests.delete(requesturl)
            return response
        except:
            response = requests.delete(requesturl).status_code
            return response


def log_response(responsejson, responsereason, responsestatuscode):
    Api.apiresponse = responsejson
    Api.apireason = responsereason
    Api.statuscode = responsestatuscode
    db.session.commit()
