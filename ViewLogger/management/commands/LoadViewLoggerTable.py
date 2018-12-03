import os
from django.core.management.base import BaseCommand
from django.conf import settings
import simplejson


def validateURL(url):
    dir = settings.VIEWLOGGER_ARCHIVE_DIR if hasattr(settings, 'VIEWLOGGER_ARCHIVE_DIR') else os.path.join(
        settings.BASE_DIR, "ViewLoggerArchive")
    finalURL = ""
    if '.' in url:
        if url.split(".")[-1] not in ["JSON", 'json', "Json"]:
            return 0, "Please make sure to put the right file extension in ( %s )" % (url)
        else:
            finalURL = url
    else:
        finalURL = url + ".json"
    dist = dir + "/%s" % (str(finalURL))
    exists = os.path.isfile(dist)
    if not exists:
        return 0, "File is not exist. Please put it in VIEWLOGGER_ARCHIVE_DIR url you determined ."
    else:
        return 1, dist


class Command(BaseCommand):
    help = '''
        Load archived ViewLogger_log file(s) exist in the VIEWLOGGER_ARCHIVE_DIR url you determined and save it the ViewLogger_log table again.
        If you want to load more than one file separate file names with comma.
    '''

    def add_arguments(self, parser):
        parser.add_argument('--file', nargs='?', type=str, default="")
        parser.add_argument('--files', nargs='?', type=str, default="")

    def handle(self, *args, **options):
        from ViewLogger.models import Log
        urlList = []
        JSONFile = []
        if options["file"]:
            urlList.append(options['file'])
        elif options["files"]:
            for url in options["files"].split(","):
                urlList.append(url)
        for url in urlList:
            valid, message = validateURL(url)
            if not valid:
                return message
            else:
                with open(message) as f:
                    JSONFile.append(simplejson.load(f))
        print "Files => ", len(JSONFile)
        for file in JSONFile:
            for records in file:
                log = Log()
                log.request_body = records["request_body"]
                log.url = records["url"]
                log.view_name = records["view_name"]
                log.done_by = records["done_by"]
                log.done_on = records["done_on"]
                log.view_kwargs = records["view_kwargs"]
                log.view_args = records["view_args"]
                log.request_method = records["request_method"]
                log.save()
        print "Done"
