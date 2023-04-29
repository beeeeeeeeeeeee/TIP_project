# Generated by Django 4.1.7 on 2023-03-28 03:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Address",
            fields=[
                (
                    "aid",
                    models.BigAutoField(
                        primary_key=True, serialize=False, verbose_name="Address ID"
                    ),
                ),
                ("address", models.CharField(max_length=256, verbose_name="Address")),
                ("suburb", models.CharField(max_length=64, verbose_name="Suburb")),
                ("postcode", models.CharField(max_length=8, verbose_name="Postcode")),
                (
                    "lat",
                    models.DecimalField(
                        decimal_places=12, max_digits=15, verbose_name="Latitude"
                    ),
                ),
                (
                    "long",
                    models.DecimalField(
                        decimal_places=12, max_digits=15, verbose_name="Longitude"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CPA",
            fields=[
                (
                    "cid",
                    models.BigAutoField(
                        primary_key=True, serialize=False, verbose_name="CID"
                    ),
                ),
                ("uid", models.BigIntegerField(verbose_name="User ID")),
                (
                    "sn",
                    models.CharField(
                        blank=True, max_length=256, null=True, verbose_name="SN Number"
                    ),
                ),
                (
                    "sales",
                    models.CharField(
                        blank=True, max_length=8, null=True, verbose_name="Sales ID"
                    ),
                ),
                (
                    "co_sales",
                    models.CharField(
                        blank=True, max_length=8, null=True, verbose_name="Sales ID"
                    ),
                ),
                (
                    "sold_date",
                    models.DateField(blank=True, null=True, verbose_name="Sold Date"),
                ),
                (
                    "active",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No")],
                        default="Yes",
                        max_length=8,
                        verbose_name="Active",
                    ),
                ),
                (
                    "directly_sold",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No")],
                        default="Yes",
                        max_length=8,
                        verbose_name="Directly Sold",
                    ),
                ),
                (
                    "aid",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="app01.address",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Piano",
            fields=[
                (
                    "pid",
                    models.BigAutoField(
                        primary_key=True, serialize=False, verbose_name="Piano ID"
                    ),
                ),
                ("brand", models.CharField(max_length=256, verbose_name="Brand")),
                ("model", models.CharField(max_length=64, verbose_name="Model")),
                (
                    "sub_model",
                    models.CharField(
                        blank=True, max_length=64, null=True, verbose_name="Sub Model"
                    ),
                ),
                (
                    "colour",
                    models.CharField(
                        blank=True, max_length=64, null=True, verbose_name="colour"
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        blank=True,
                        choices=[("Upright", "Upright"), ("Grand", "Grand")],
                        default="Upright",
                        max_length=8,
                        null=True,
                        verbose_name="Piano Type",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Tuning",
            fields=[
                (
                    "tid",
                    models.BigAutoField(
                        primary_key=True, serialize=False, verbose_name="Tuning ID"
                    ),
                ),
                ("mid", models.CharField(max_length=8, verbose_name="Machinist ID")),
                (
                    "tuning_date",
                    models.DateField(blank=True, null=True, verbose_name="Tuning Date"),
                ),
                (
                    "piano_condition",
                    models.CharField(
                        blank=True,
                        max_length=256,
                        null=True,
                        verbose_name="Piano Condition",
                    ),
                ),
                (
                    "cid",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="app01.cpa",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="cpa",
            name="pid",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="app01.piano",
            ),
        ),
    ]