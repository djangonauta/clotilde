# Generated by Django 5.2.1 on 2025-05-19 16:20

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Automacao',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=255)),
                ('inicio', models.DateTimeField(auto_now_add=True)),
                ('fim', models.DateTimeField(blank=True, null=True)),
                ('status', models.IntegerField(choices=[(1, 'Iniciada'), (2, 'Finalizada'), (3, 'Erro')], default=1)),
                ('stack_trace', models.TextField(blank=True)),
                ('enviada', models.BooleanField(default=False)),
            ],
        ),
    ]
