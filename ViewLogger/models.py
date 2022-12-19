from django.db import models
try:
    from django.db.models import JSONField
except ImportError:
    try:
        from jsonfield.fields import JSONField
    except ImportError:
        raise ImportError("Can't find a JSONField implementation, please install jsonfield if django < 4.0")



class Log(models.Model):
    id = models.AutoField(primary_key=True)
    view_name = models.CharField(max_length=255)
    request_method = models.CharField(max_length=5)
    request_body = JSONField(default=dict)
    url = models.CharField(max_length=255)
    view_args = JSONField(default=list)
    view_kwargs = JSONField(default=dict)
    done_by = models.CharField(max_length=255)
    done_on = models.DateTimeField(auto_now_add=True)
    duration = models.DecimalField(null = True, default = 0,max_digits = 5, decimal_places=5)

    def __unicode__(self):
        return self.id

    class Meta:
        app_label = "ViewLogger"
