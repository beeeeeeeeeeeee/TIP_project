# Generated by Django 4.0.10 on 2023-04-27 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Suburb',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suburb_name', models.CharField(max_length=60)),
                ('post_code', models.CharField(max_length=4)),
                ('num_cust', models.IntegerField()),
            ],
        ),
    ]