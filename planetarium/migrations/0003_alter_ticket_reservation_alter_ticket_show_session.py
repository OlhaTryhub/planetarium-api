# Generated by Django 4.2.4 on 2023-08-10 18:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("planetarium", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticket",
            name="reservation",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tickets",
                to="planetarium.reservation",
            ),
        ),
        migrations.AlterField(
            model_name="ticket",
            name="show_session",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="tickets",
                to="planetarium.showsession",
            ),
        ),
    ]