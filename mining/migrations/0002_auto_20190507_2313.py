# Generated by Django 2.2.1 on 2019-05-07 23:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mining', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trade',
            old_name='total_trades',
            new_name='tot_ctrcts_papers',
        ),
    ]