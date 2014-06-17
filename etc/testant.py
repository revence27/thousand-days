# vim: expandtab ts=2
from thoureport.reports import *
from thoureport.models import *

msg = 'RED DI'
rep = ThouMessage.parse_report(msg,
                  {'RED':RedReport})
rep.save()
