# Generated by Django 3.2.5 on 2021-10-26 04:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0005_auto_20211020_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manager', to=settings.AUTH_USER_MODEL),
        ),
    ]
