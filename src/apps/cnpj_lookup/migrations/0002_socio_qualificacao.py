# Generated by Django 4.2 on 2023-04-30 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cnpj_lookup', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='socio',
            name='qualificacao',
            field=models.CharField(default=None, max_length=200),
            preserve_default=False,
        ),
    ]
