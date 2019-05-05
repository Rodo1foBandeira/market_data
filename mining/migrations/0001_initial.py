# Generated by Django 2.2.1 on 2019-05-04 22:58

from django.db import migrations, models
import django.db.models.deletion
import unixtimestampfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Active',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('ticker', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('time_stamp', unixtimestampfield.fields.UnixTimeStampField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('business', models.IntegerField()),
                ('total_trades', models.IntegerField()),
                ('active', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mining.Active')),
            ],
        ),
    ]