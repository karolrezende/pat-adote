# Generated by Django 5.2.1 on 2025-07-01 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telaInicial', '0002_adocao'),
    ]

    operations = [
        migrations.AddField(
            model_name='postagem',
            name='adotado',
            field=models.BooleanField(default=False),
        ),
    ]
