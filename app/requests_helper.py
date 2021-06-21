from pip._vendor import requests
from app import db
from app.models import Api


def perform_request(requesttype, requesturl):
    if requesttype == 'Get':
        try:
            response = requests.get(requesturl)
            # log_response(response.json(), response.reason, response.status_code)
            return response
        except:
            response = requests.get(requesturl)
            # log_response(response.json(), response.reason, response.status_code)
            return response


def log_response(responsejson, responsereason, responsestatuscode):
    # logresponse = Api(apiresponse=str(responsejson), apireason=str(responsereason), statuscode=int(responsestatuscode))
    # db.session.update(logresponse)
    Api.apiresponse = responsejson
    Api.apireason = responsereason
    Api.statuscode = responsestatuscode
    db.session.commit()
