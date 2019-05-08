from django.db import models

# Create your models here.
class Active(models.Model):
    name = models.CharField(max_length=60)
    ticker = models.CharField(max_length=10)

class Trade(models.Model):
    id = models.BigAutoField(primary_key=True)
    active = models.ForeignKey('Active', on_delete=models.CASCADE)
    datetime_buss = models.DateTimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    business = models.IntegerField()
    tot_ctrcts_papers = models.IntegerField()
