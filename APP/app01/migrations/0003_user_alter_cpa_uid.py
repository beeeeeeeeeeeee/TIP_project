# Generated by Django 4.1.7 on 2023-04-10 06:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app01", "0002_alter_cpa_aid_alter_cpa_co_sales_alter_cpa_pid"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "uid",
                    models.BigAutoField(
                        primary_key=True, serialize=False, verbose_name="User ID"
                    ),
                ),
                (
                    "first_name",
                    models.CharField(max_length=128, verbose_name="First Name"),
                ),
                (
                    "last_name",
                    models.CharField(max_length=128, verbose_name="Last Name"),
                ),
                (
                    "email",
                    models.CharField(
                        blank=True, max_length=128, null=True, verbose_name="email"
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[("Male", "Male"), ("Female", "Female")],
                        default="Upright",
                        max_length=8,
                        null=True,
                        verbose_name="Gender",
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(max_length=32, verbose_name="Phone Number"),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="cpa",
            name="uid",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="app01.user",
                verbose_name="User ID",
            ),
        ),
    ]
