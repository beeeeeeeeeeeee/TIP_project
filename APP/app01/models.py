from django.db import models


# Create your models here.

class User(models.Model):
    uid = models.BigAutoField(verbose_name="User ID", primary_key=True)
    first_name = models.CharField(verbose_name="First Name", max_length=128)
    last_name = models.CharField(verbose_name="Last Name", max_length=128)
    email = models.EmailField(verbose_name="email", max_length=128, null=True, blank=True)

    gender_choices = (
        ("Male", "Male"),
        ("Female", "Female"),
    )
    gender = models.CharField(verbose_name="Gender", choices=gender_choices, null=True, blank=True, default="Upright",
                              max_length=8)
    phone_number = models.CharField(verbose_name="Phone Number", max_length=32, unique=True)

    def __str__(self):
        return "UID:" + str(self.uid) + ", " + self.first_name + " " + self.last_name + ", " + self.phone_number


class Address(models.Model):
    aid = models.BigAutoField(verbose_name="Address ID", primary_key=True)
    address = models.CharField(verbose_name="Address", max_length=256)
    suburb = models.CharField(verbose_name="Suburb", max_length=64)
    postcode = models.CharField(verbose_name="Postcode", max_length=8)
    lat = models.DecimalField(verbose_name="Latitude", max_digits=15, decimal_places=12)
    long = models.DecimalField(verbose_name="Longitude", max_digits=15, decimal_places=12)

    def __str__(self):
        return "AID:" + str(self.aid) + ", " + self.address + ", " + self.suburb + ", " + self.postcode


class Piano(models.Model):
    pid = models.BigAutoField(verbose_name="Piano ID", primary_key=True)
    brand = models.CharField(verbose_name="Brand", max_length=256)
    model = models.CharField(verbose_name="Model", max_length=64)
    sub_model = models.CharField(verbose_name="Sub Model", max_length=64, null=True, blank=True)
    colour = models.CharField(verbose_name="colour", max_length=64, null=True, blank=True)

    # type_choices = (
    #     (0, "Upright"),
    #     (1, "Grand"),
    # )
    # type = models.SmallIntegerField(verbose_name="Piano Type", choices=type_choices, null=True, blank=True)
    type_choices = (
        ("Upright", "Upright"),
        ("Grand", "Grand"),
    )
    type = models.CharField(verbose_name="Piano Type", choices=type_choices, null=True, blank=True, default="Upright",
                            max_length=8)

    def __str__(self):
        return "PID:" + str(self.pid) + ", " + self.brand + ", " + self.model


class CPA(models.Model):
    cid = models.BigAutoField(verbose_name="CID", primary_key=True)
    # uid = models.ForeignKey(to="User", to_field="uid", verbose_name="User ID")
    uid = models.ForeignKey(to="User", to_field="uid", null=True, blank=True, on_delete=models.SET_NULL,
                            verbose_name="User ID")
    # when del id data in Address,Piano, set the value to null
    aid = models.ForeignKey(to="Address", to_field="aid", null=True, blank=True, on_delete=models.SET_NULL,
                            verbose_name="AID")
    pid = models.ForeignKey(to="Piano", to_field="pid", null=True, blank=True, on_delete=models.SET_NULL,
                            verbose_name="PID")
    sn = models.CharField(verbose_name="SN Number", max_length=256, null=True, blank=True)
    sales = models.CharField(verbose_name="Sales ID", max_length=8, null=True, blank=True)
    co_sales = models.CharField(verbose_name="Co_Sales ID", max_length=8, null=True, blank=True)
    sold_date = models.DateField(verbose_name="Sold Date", null=True, blank=True)

    choices = (
        ("Yes", "Yes"),
        ("No", "No"),
    )
    active = models.CharField(verbose_name="Active", choices=choices, default="Yes", max_length=8)
    directly_sold = models.CharField(verbose_name="Directly Sold", choices=choices, default="Yes", max_length=8)

    def __str__(self):
        return '%s %s %s, SN:%s, Sold Date:%s' % (self.uid, self.aid, self.pid, self.sn, self.sold_date)


class Tuning(models.Model):
    tid = models.BigAutoField(verbose_name="Tuning ID", primary_key=True)
    mid = models.CharField(verbose_name="Machinist ID", max_length=8)
    # when del cid data in CPA, set the value to null
    cid = models.ForeignKey(to="CPA", to_field="cid", null=True, blank=True, on_delete=models.SET_NULL)
    tuning_date = models.DateField(verbose_name="Tuning Date", null=True, blank=True)
    piano_condition = models.CharField(verbose_name="Piano Condition", max_length=256, null=True, blank=True)
