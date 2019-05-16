from django.db import models

# Create your models here.
class Active(models.Model):
    name = models.CharField(max_length=60)
    ticker = models.CharField(max_length=10)

class Trade(models.Model):
    id = models.BigAutoField(primary_key=True)
    active = models.ForeignKey('Active', on_delete=models.CASCADE)
    datetime_buss = models.DateTimeField()
    buyer = models.IntegerField()
    seller = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    qtd = models.IntegerField()
    tot_qtd = models.IntegerField()
    tot_buss = models.IntegerField()    
