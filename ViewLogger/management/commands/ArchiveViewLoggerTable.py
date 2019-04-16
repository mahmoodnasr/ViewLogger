from django.core.management.base import BaseCommand
import os
from django.conf import settings
import simplejson, datetime
from django.db import connection


def RESET(days,lastID):
    with connection.cursor() as cursor:
        query = "DELETE FROM ViewLogger_log WHERE done_on < "+days
        cursor.execute(query)
        resetQ = 'ALTER TABLE ViewLogger_log AUTO_INCREMENT = '+str(lastID)
        cursor.execute(resetQ)
        row = cursor.fetchone()
    return row


class DateTimeJsonEncoder(simplejson.JSONEncoder):
    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M:%S.%f"

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            try:
                return obj.strftime("%s %s" % (self.DATE_FORMAT, self.TIME_FORMAT))
            except:
                return None

        return super(DateTimeJsonEncoder, self).default(obj)


class Command(BaseCommand):
    help = 'Archive ViewLogger_log table data and empty its content in days ' \
           'Example : "python manage.py ArchiveViewLoggerTable --before=7"' \
           'This command will archive the data exist in table except the past 7 days'

    def add_arguments(self, parser):
        parser.add_argument('--before', nargs='?', type=int, default=7)

    def handle(self, *args, **options):
        from ViewLogger.models import Log
        from ViewLogger.api import fetchChangesAPI
        days = (datetime.datetime.now() - datetime.timedelta(days=options["before"])).strftime('%Y-%m-%d')
        changes = Log.objects.filter(done_on__lt=days).order_by('id')
        count = len(changes)
        if changes.exists():
            lastID = changes[0].id
            first = changes.values_list("done_on", flat=True)[0].date()
            last = changes.values_list("done_on", flat=True).last().date()
            res = fetchChangesAPI(changes)
            json = res["changes"]
            dir = settings.VIEWLOGGER_ARCHIVE_DIR if hasattr(settings, 'VIEWLOGGER_ARCHIVE_DIR') else os.path.join(
                settings.BASE_DIR, "ViewLoggerArchive")
            if not os.path.exists(dir):
                os.makedirs(dir)
            date = datetime.datetime.now()
            dist = dir + "/From_%s_To_%s(%s).json" % (str(first), str(last),str(date)[11:19])
            f = open(dist, "w")
            f.write(simplejson.dumps(json, cls=DateTimeJsonEncoder))
            f.close()
            changes.delete()
            print(RESET(days,lastID))
            print("Done - %s Records"%count)
        else:
            return "There are no records"
