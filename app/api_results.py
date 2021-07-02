from json import JSONDecodeError

from app import requests_helper
from app.models import Api


def get_api_results():
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
        except AttributeError:
            apiwip += 1
        except JSONDecodeError:
            Api.set_response(x, "{}")
    apisuccess = "{:.2f}".format((apipass / apitotal) * 100)

    apiResult = dict()
    apiResult['Pass'] = apipass
    apiResult['Fail'] = apifail
    apiResult['Wip'] = apiwip
    apiResult['Total'] = apitotal
    apiResult['SuccPert'] = apisuccess

    return apiResult