# Generated by Django 4.2.2 on 2023-06-20 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('galeria', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Importacoes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_transacoes', models.DateField()),
                ('data_importacao', models.DateTimeField()),
            ],
        ),
    ]