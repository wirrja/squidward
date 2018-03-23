# Generated by Django 2.0.1 on 2018-03-23 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GrayToDb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.IntegerField(db_index=True)),
                ('pptp_id', models.IntegerField()),
                ('pptp_ip', models.GenericIPAddressField(protocol='IPv4')),
            ],
        ),
        migrations.CreateModel(
            name='HappinessState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.IntegerField()),
                ('section', models.CharField(max_length=24)),
                ('message', models.CharField(max_length=50)),
                ('state', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SquidFullData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.IntegerField(db_index=True)),
                ('duration', models.IntegerField()),
                ('pptpip', models.GenericIPAddressField(protocol='IPv4')),
                ('size', models.BigIntegerField()),
                ('resource', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='WhiteToDB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.IntegerField(db_index=True)),
                ('pptp_id', models.IntegerField()),
                ('pptp_ip', models.GenericIPAddressField(protocol='IPv4')),
            ],
        ),
    ]
