from django.db import models

# Create your models here.
class Catches(models.Model):

    id = models.CharField(
        primary_key = True,
        max_length = 36
    )

    buyer_id = models.IntegerField() # this will be a foreign key when using multiple tables

    buyer_name = models.CharField(max_length = 20) # verify this...

    fisher_id = models.CharField(max_length = 8) # maybe also foreign key

    date = models.DateTimeField()

    total_price = models.FloatField()

    def __str__(self):
        return self.id
