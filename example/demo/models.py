# coding=utf8


from django.db import models
from django.utils import timezone

from django_echarts.datasets.managers import AxisValuesQuerySet


class Device(models.Model):
    mac = models.CharField(max_length=50, unique=True, verbose_name="MAC地址", )
    name = models.CharField(max_length=50, default='-', verbose_name="设备名称")
    device_type = models.CharField(max_length=50, verbose_name="设备类型")
    latitude = models.FloatField(null=True, blank=True, verbose_name="经度")
    longitude = models.FloatField(null=True, blank=True, verbose_name="纬度")
    address = models.CharField(max_length=50, null=True, blank=True, verbose_name="Install Address")
    battery_life = models.IntegerField(verbose_name='电量(%)', default=100)
    online = models.NullBooleanField(default=None, verbose_name="在线状态")
    parent_gateway_mac = models.CharField(max_length=50, blank=True, null=True)
    parent_rtu_mac = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.mac


class DataRecord(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    record_time = models.DateTimeField(default=timezone.now)
    val1 = models.IntegerField()
    val2 = models.IntegerField()

    def __str__(self):
        return 'Data Record {0}'.format(self.device.mac)


class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    author = models.CharField(max_length=50)
    post_time = models.DateTimeField(default=timezone.now)
    read_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class TemperatureRecord(models.Model):
    high = models.FloatField()
    low = models.FloatField()
    create_time = models.DateTimeField(default=timezone.now)

    objects = models.Manager.from_queryset(AxisValuesQuerySet)()

    def __str__(self):
        return 'Temperature Record'
