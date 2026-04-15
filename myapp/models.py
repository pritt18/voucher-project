from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=1)

    def __str__(self):
        return self.name


class AlphaGroup(models.Model):
    name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class Voucher(models.Model):
    voucher_no = models.CharField(max_length=50)
    voucher_date = models.DateField()
    remarks = models.TextField()

    total_a = models.FloatField(default=0)
    total_b = models.FloatField(default=0)

    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.voucher_no