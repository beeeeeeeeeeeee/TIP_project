from django.db import models


# Create your models here.
class Department(models.Model):
    """
    department table
    """
    title = models.CharField(max_length=32, verbose_name="department title")

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    name = models.CharField(max_length=16, verbose_name="Name")
    password = models.CharField(max_length=64, verbose_name="Password")
    age = models.IntegerField(verbose_name="Age")
    account = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Account")

    create_time = models.DateField(verbose_name="Entry Time")

    depart = models.ForeignKey(to='Department', to_field="id", on_delete=models.CASCADE, verbose_name="Department")
    # depart = models.ForeignKey(to='Department', to_field="id", null=True, blank=True, on_delete=models.SET_NULL)

    gender_choices = ((1, "M"), (2, "F"))
    gender = models.SmallIntegerField(choices=gender_choices, verbose_name="Gender")


class PrettyNum(models.Model):
    mobile = models.CharField(max_length=32, verbose_name="Phone No.")
    price = models.IntegerField(verbose_name="Price", default=0)
    level_choices = ((1, "Level 1"), (2, "Level 2"), (3, "Level 3"), (4, "Level 4"))
    level = models.SmallIntegerField(choices=level_choices, verbose_name="Level", default=1)
    status_choices = ((1, "Sold"), (2, "Available"))
    status = models.SmallIntegerField(choices=status_choices, verbose_name="Status")


class Admin(models.Model):
    username = models.CharField(verbose_name="User Name", max_length=32)
    password = models.CharField(verbose_name="Password", max_length=64)

    def __str__(self):
        return self.username


class Task(models.Model):
    level_choices = (
        (1, "Emergency"),
        (2, "Important"),
        (3, "Temporary")
    )
    level = models.SmallIntegerField(verbose_name="Level", choices=level_choices, default=1)
    title = models.CharField(verbose_name="Title", max_length=64)
    detail = models.TextField(verbose_name="Detail")
    user = models.ForeignKey(verbose_name="Leader", to="Admin", on_delete=models.CASCADE)


class Order(models.Model):
    oid = models.CharField(verbose_name="Order No.", max_length=64)
    title = models.CharField(verbose_name="Product Name", max_length=32)
    price = models.IntegerField(verbose_name="Price")
    status_choices = (
        (1, "Paid"),
        (2, "Unpaid")
    )
    status = models.SmallIntegerField(verbose_name="Status", choices=status_choices, default=1)
    admin = models.ForeignKey(verbose_name="Admin", to="Admin", on_delete=models.CASCADE)


class Boss(models.Model):
    name = models.CharField(verbose_name="Name", max_length=32)
    age = models.IntegerField(verbose_name="Age")
    img = models.CharField(verbose_name="Head", max_length=128)


class City(models.Model):
    name = models.CharField(verbose_name="City Name", max_length=32)
    count = models.IntegerField(verbose_name="Population")
    # in mysql, FileField is also CharField, but it can save automatically to media/city
    logo = models.FileField(verbose_name="Logo", max_length=128, upload_to="city/")


class Address(models.Model):
    aid = models.BigIntegerField(verbose_name="Address ID", db_index=True, primary_key=True)
    address = models.CharField(verbose_name="Address", max_length=256)
    suburb = models.CharField(verbose_name="Suburb", max_length=64)
    postcode = models.CharField(verbose_name="Postcode", max_length=8)
    lat = models.DecimalField(max_digits=11, decimal_places=8)
    long = models.DecimalField(max_digits=11, decimal_places=8)


class Address1(models.Model):
    address = models.CharField(verbose_name="Address", max_length=256)
    unit = models.CharField(verbose_name="Unit or Apartment No.", max_length=256, null=True, blank=True)
    suburb = models.CharField(verbose_name="Suburb", max_length=64)
    postcode = models.CharField(verbose_name="Postcode", max_length=8)
    lat = models.DecimalField(max_digits=11, decimal_places=8)
    long = models.DecimalField(max_digits=11, decimal_places=8)


class Address2(models.Model):
    address = models.CharField(verbose_name="Address", max_length=256)
    unit = models.CharField(verbose_name="Unit or Apartment No.", max_length=256, null=True, blank=True)
    suburb = models.CharField(verbose_name="Suburb", max_length=64)
    postcode = models.CharField(verbose_name="Postcode", max_length=8)
    lat = models.DecimalField(max_digits=11, decimal_places=8)
    long = models.DecimalField(max_digits=11, decimal_places=8)
