from app.models import Stats
from app import db
from datetime import datetime
from pytz import timezone
import sys


def updateStats(apiPass, apiFail, apiTotal, apiWip):

    if Stats.query.count() == 0:
        stat = Stats(apipass=apiPass, apifail=apiFail, apitotal=apiTotal, apiwip=apiWip,
                     apisuccess="{:.2f}".format((apiPass / apiTotal) * 100))
        db.session.add(stat)
        db.session.commit()
    elif Stats.query.count() < 5:
        print('Count is ' + str(Stats.query.count()), file=sys.stderr)
        stat = Stats(apipass=apiPass, apifail=apiFail, apitotal=apiTotal, apiwip=apiWip,
                     apisuccess="{:.2f}".format((apiPass / apiTotal) * 100), last_updated=datetime.now(timezone('America/New_York')).strftime('%Y-%m-%d %H:%M:%S'))
        db.session.add(stat)
        db.session.commit()
    else:
        stat = Stats(apipass=apiPass, apifail=apiFail, apitotal=apiTotal, apiwip=apiWip,
                     apisuccess="{:.2f}".format((apiPass / apiTotal) * 100), last_updated=datetime.now(timezone('America/New_York')).strftime('%Y-%m-%d %H:%M:%S'))
        db.session.add(stat)
        db.session.commit()

        deleteRpw = Stats.query.first()
        db.session.delete(deleteRpw)
        db.session.commit()


