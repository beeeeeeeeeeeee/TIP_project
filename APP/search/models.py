from django.db import models

# Create your models here.
class Address(models.Model):
    aid = models.AutoField(primary_key=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    suburb = models.CharField(max_length=255)
    postcode = models.IntegerField()
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'address'

    def __str__(self):
        return f'{self.aid} {self.address} {self.suburb} {self.postcode} {self.latitude} {self.longitude}'

class Customer(models.Model):
    cid = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer'

    def __str__(self):
        return f'{self.cid} {self.firstname} {self.lastname} {self.email} {self.phone}'

class Product(models.Model):
    pid = models.AutoField(primary_key=True)
    brand = models.CharField(max_length=255, blank=True, null=True)
    model = models.CharField(max_length=255, blank=True, null=True)
    submodel = models.CharField(max_length=255, blank=True, null=True)
    colour = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product'

    def __str__(self):
        return f'{self.pid} {self.brand} {self.model} {self.submodel} {self.colour} {self.type}'

class Tuning(models.Model):
    tid = models.AutoField(primary_key=True)
    mid = models.IntegerField()
    cid = models.ForeignKey(Customer, models.DO_NOTHING, db_column='cid')
    tuning_date = models.DateField(blank=True, null=True)
    piano_condition = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tuning'
        
    def __str__(self):
        return f'{self.tid} {self.mid} {self.cid} {self.tuning_date} {self.piano_condition}'


class Cpa(models.Model):
    cid = models.IntegerField(blank=True, null=True)
    aid = models.IntegerField(blank=True, null=True)
    pid = models.IntegerField(blank=True, null=True)
    sn = models.CharField(max_length=255, blank=True, null=True)
    sales = models.IntegerField(blank=True, null=True)
    co_sales = models.IntegerField(blank=True, null=True)
    sold_date = models.DateField(blank=True, null=True)
    active = models.CharField(max_length=255, blank=True, null=True)
    directly_sold = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cpa'
    
    def __str__(self):
        return f'{self.cid} {self.aid} {self.pid} {self.sn} {self.sales} {self.co_sales} {self.sold_date} {self.active} {self.directly_sold}'