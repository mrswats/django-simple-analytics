# Generated by Django 3.2.14 on 2022-08-25 05:50
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies: list[tuple[str, str]] = []

    operations = [
        migrations.CreateModel(
            name="VisitPerPage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("page", models.CharField(max_length=100)),
                ("date", models.DateField()),
                ("view_count", models.BigIntegerField(default=1)),
                ("exists", models.BooleanField(default=True)),
                ("method", models.CharField(default="GET", max_length=10)),
                ("username", models.CharField(max_length=50)),
            ],
            options={
                "verbose_name_plural": "Visits per Page",
            },
        ),
    ]
