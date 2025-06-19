from django.db import models
from django.urls import reverse

class Sale(models.Model):
    product = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.product} - {self.quantity} units"

    def get_absolute_url(self):
        return reverse('sales:index')
