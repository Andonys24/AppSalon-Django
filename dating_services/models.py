from django.db import models
from authentication.models import CustomUser


# Create your models here.
class Services(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Quotes(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField()
    hour = models.TimeField()


class ServicesQuotes(models.Model):
    quote = models.ForeignKey(Quotes, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
