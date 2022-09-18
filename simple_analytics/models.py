from django.db import models


class VisitPerPage(models.Model):
    page = models.CharField(max_length=100)
    date = models.DateField()
    view_count = models.BigIntegerField(default=1)
    exists = models.BooleanField(default=True)
    method = models.CharField(max_length=10, default="GET")
    username = models.CharField(max_length=50)
    origin = models.CharField(max_length=250, default="")
    user_agent = models.TextField(default="")

    def __str__(self) -> str:
        return f"{self.page} [{self.date.strftime('%Y-%m-%d')}] - {self.view_count}"

    class Meta:
        verbose_name_plural = "Visits per Page"
