# Generated by Django 3.0.6 on 2021-10-19 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20211018_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='project',
            name='tags',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='thread',
            name='description',
            field=models.TextField(),
        ),
    ]
