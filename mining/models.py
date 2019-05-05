from django.db import models

from unixtimestampfield.fields import UnixTimeStampField

# Create your models here.
class Active(models.Model):
    name = models.CharField(max_length=60)
    ticker = models.CharField(max_length=10)

class Trade(models.Model):
    id = models.BigAutoField(primary_key=True)
    active = models.ForeignKey('Active', on_delete=models.CASCADE)
    time_stamp = UnixTimeStampField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    business = models.IntegerField()
    total_trades = models.IntegerField()