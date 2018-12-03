import os
import commands
from django.core.management.base import BaseCommand
from django.conf import settings
from ViewLogger import Common


def is_exe(fpath):
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)


class Command(BaseCommand):
    help = '''
        Search in ViewLogger Archives files. You can search with keywords ( url , view_name , done_by , done_on , view_kwargs , view_args , request_method , request_body )
    '''

    def add_arguments(self, parser):
        parser.add_argument('--url', nargs='?', type=str, default="")
        parser.add_argument('--view_name', nargs='?', type=str, default="")
        parser.add_argument('--done_by', nargs='?', type=str, default="")
        parser.add_argument('--done_on', nargs='?', type=str, default="")
        parser.add_argument('--view_kwargs', nargs='?', type=str, default="")
        parser.add_argument('--view_args', nargs='?', type=str, default="")
        parser.add_argument('--request_method', nargs='?', type=str, default="")
        parser.add_argument('--request_body', nargs='?', type=str, default="")

    def handle(self, *args, **options):
        dir = settings.VIEWLOGGER_ARCHIVE_DIR if hasattr(settings, 'VIEWLOGGER_ARCHIVE_DIR') else os.path.join(
            settings.BASE_DIR, "ViewLoggerArchive")
        filesList = [x for x in os.listdir(dir)]
        alloptions = ""
        if options['url']: alloptions += '''|  select(.url | contains("%s")) ''' % (options['url'])
        if options['view_name']: alloptions += '''|  select(.view_name | contains("%s")) ''' % (options['view_name'])
        if options['done_by']: alloptions += '''|  select(.done_by | contains("%s")) ''' % (options['done_by'])
        if options['done_on']: alloptions += '''|  select(.done_on | contains("%s")) ''' % (options['done_on'])
        if options['view_kwargs']:
            for option in options['view_kwargs'].split(","):
                key = option.split("=")[0]
                val = option.split("=")[-1]
                if key != "":
                    alloptions+=""" | select(.view_kwargs.%s| contains("%s")) """%(key,val)
        if options['view_args']:
            for option in options['view_args'].split(","):
                key = option.split("=")[0]
                val = option.split("=")[-1]
                if key != "":
                    alloptions+=""" | select(.view_args.%s| contains("%s")) """%(key,val)
        if options['request_method']: alloptions += '''|  select(.request_method | contains("%s")) ''' % (options['request_method'])
        if options['request_body']:
            for option in options['request_body'].split(","):
                key = option.split("=")[0]
                val = option.split("=")[-1]
                if key != "":
                    alloptions+=""" | select(.request_body.%s = "%s") """%(key,val)
        bin = '%s/ViewLogger/bin/jq-linux64' % (settings.BASE_DIR)
        if not is_exe(bin):
            stat, output = commands.getstatusoutput('chmod +x %s') % (bin)

        for file in filesList:
            print "File = ",file
            cmd = """%s/ViewLogger/bin/jq-linux64 '.[] %s' %s""" % (
                settings.BASE_DIR, alloptions, dir + "/" + file)
            print Common.run(cmd)
