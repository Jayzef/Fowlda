# Generated by Django 5.1.1 on 2024-09-30 14:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_arquivo_options_arquivo_tempo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversao',
            name='arquivo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.arquivo', verbose_name='Arquivo'),
        ),
    ]