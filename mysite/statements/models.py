from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class IncomeStatement(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    FishRevenue = models.IntegerField()
    FishCost = models.IntegerField()
    FishProfit = models.IntegerField()
    SupplyRevenue = models.IntegerField()
    SupplyCost = models.IntegerField()
    SupplyProfit = models.IntegerField()
