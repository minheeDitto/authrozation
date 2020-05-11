from django.db import models
from datetime import datetime


# Create your models here.


class shouquanma(models.Model):
    authorization_code = models.CharField(max_length=16,verbose_name="授权码",default="")
    is_active = models.CharField(default=0,verbose_name="激活时间",max_length=10)
    expire = models.IntegerField(default=0,verbose_name="过期时间")
    online = models.BooleanField(default=0,verbose_name="是否在线")
    device_id = models.CharField(max_length=100,default="",verbose_name="设备id")
    heart_time = models.DateTimeField(default=datetime.now,verbose_name="心跳时间")
    active_time = models.DateTimeField(default=datetime.now,verbose_name="激活时间")
    expire_time = models.DateTimeField(default=datetime.now,verbose_name="到期时间")
    initial_time = models.DateTimeField(default=datetime.now,verbose_name="初始化时间")

    class Meta:
        db_table = "code"

    def __str__(self):
        return str(self.id)




