from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from areas.models import ProductionLine
from datetime import date, datetime
from products.models import Product
import django
from categories.models import Category
from django.db.models import Sum
from areas.models import ProductionLine
from datetime import datetime
# Create your models here.
hours = ([(str(x), str(x)) for x in range(1, 25)])


class ReportQueryset(models.QuerySet):
    def filter_by_day(self, day):
        return self.filter(day=day)

    def aggregate_plan(self):
        return self.aggregate(Sum('plan'))

    def aggregate_execution(self):
        return self.aggregate(Sum('execution'))


class ReportManager(models.Manager):
    def get_queryset(self):
        return ReportQueryset(self.model, using=self._db)

    def filter_by_day(self, day):
        return self.get_queryset().filter_by_day(day)

    def aggregate_plan(self):
        return self.get_queryset().aggregate_plan()

    def aggregate_execution(self):
        return self.get_queryset().aggregate_execution()


class Report(models.Model):
    day = models.DateField(default=django.utils.timezone.now)
    start_hour = models.CharField(max_length=2, choices=hours)
    end_hour = models.CharField(max_length=2, choices=hours)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    plan = models.PositiveIntegerField()
    execution = models.PositiveIntegerField()
    production_line = models.ForeignKey(
        ProductionLine, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ReportManager()

    def __str__(self):
        return "{}-{}, {}".format(self.start_hour, self.end_hour, self.production_line)

    def get_absolute_url(self):
        return reverse('reports:update', kwargs={'production_line': self.production_line, 'pk': self.pk})

    @property
    def get_user(self):
        return self.request.user

    class Meta:
        ordering = ('-timestamp',)


class ProblemReportedManager(models.Manager):
    def problem_reported_by_day(self, day, line):
        return super().get_queryset().filter(report__day=day, report__production_line=line)

    def problems_from_today(self):
        now = datetime.now().strftime("%Y-%m-%d")
        return super().get_queryset().filter(report__day=now)


class ProblemReported(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    problem_id = models.CharField(
        max_length=12, unique=True, blank=True, null=True)
    breakdown = models.PositiveIntegerField()
    public = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    report = models.ForeignKey(Report, on_delete=models.CASCADE, blank=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ProblemReportedManager()

    def __str__(self):
        return "{}-{}".format(self.category.name, self.description[:20])

    class Meta:
        verbose_name = "Problem reported"
        verbose_name_plural = "Problems reported"
