# Generated by Django 5.1.4 on 2024-12-17 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Desaceleracao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DecimalField(decimal_places=2, max_digits=12)),
            ],
        ),
    ]
