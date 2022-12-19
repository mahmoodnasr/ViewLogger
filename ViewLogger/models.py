from django.db import models
from jsonfield import JSONField


class Log(models.Model):
    id = models.AutoField(primary_key=True)
    view_name = models.CharField(max_length=255)
    request_method = models.CharField(max_length=5)
    request_body = JSONField(default={})
    url = models.CharField(max_length=255)
    view_args = JSONField(default=[])
    view_kwargs = JSONField(default={})
    done_by = models.CharField(max_length=255)
    done_on = models.DateTimeField(auto_now_add=True)
    duration = models.CharField(max_length=50,default=None,null=True)
    response_status = models.CharField(max_length=50,default=None,null=True)

    def __unicode__(self):
        return self.id
    class Meta:
        app_label = "ViewLogger"
