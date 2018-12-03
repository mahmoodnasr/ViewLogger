from django.core.management.base import BaseCommand
import os
from django.conf import settings
import simplejson, datetime
from django.db import connection


def RESET_AUTO_INCREMENT():
    with connection.cursor() as cursor:
        cursor.execute("TRUNCATE TABLE ViewLogger_log;")
        cursor.execute("ALTER TABLE ViewLogger_log AUTO_INCREMENT = 1;")
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
    help = 'Archive ViewLogger_log table data and empty its content'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        from ViewLogger.models import Log
        from ViewLogger.api import fetchChangesAPI
        changes = Log.objects.all().order_by('id')
        first = changes.values_list("done_on", flat=True)[0].date()
        last = changes.values_list("done_on", flat=True).last().date()
        res = fetchChangesAPI(changes)
        json = res["changes"]
        dir = settings.VIEWLOGGER_ARCHIVE_DIR if hasattr(settings, 'VIEWLOGGER_ARCHIVE_DIR') else os.path.join(
            settings.BASE_DIR, "ViewLoggerArchive")
        if not os.path.exists(dir):
            os.makedirs(dir)
        dist = dir + "/From_%s_To_%s.json" % (str(first), str(last))
        if os.path.exists(dist):
            dist.replace(".json","_1")
        f = open(dist, "w")
        f.write(simplejson.dumps(json, cls=DateTimeJsonEncoder))
        f.close()
        changes.delete()
        print RESET_AUTO_INCREMENT()
        print "Done"
