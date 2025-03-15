# Generated by Django 5.1.7 on 2025-03-13 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0004_alter_vendorlocation_company_gst_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='vendorlocation',
            name='unique_gst_across_vendors',
        ),
        migrations.AddConstraint(
            model_name='vendorlocation',
            constraint=models.UniqueConstraint(fields=('company_gst',), name='unique_gst_across_vendors'),
        ),
    ]
