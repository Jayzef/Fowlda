# Generated by Django 5.1.1 on 2024-10-01 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_arquivo_chave_alter_arquivo_tempo'),
    ]

    operations = [
        migrations.AddField(
            model_name='arquivo',
            name='docx_file',
            field=models.FileField(blank=True, null=True, upload_to='app/static/files/docx'),
        ),
    ]
