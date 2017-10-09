from django.db import models;
from django.contrib.auth.models import User;
from annoying.fields import AutoOneToOneField;

class PledgeFilter(models.Model):
    user = AutoOneToOneField(User, on_delete=models.CASCADE);
    not_been_active_in_the_last_n_days = models.PositiveIntegerField(default=0);
    paid_at_least_n_times = models.PositiveIntegerField(default=0);
    paid_at_least_n_amount_in_total = models.FloatField(default=0);

class WorkerFilter(models.Model):
    user = AutoOneToOneField(User, on_delete=models.CASCADE);
    not_been_active_in_the_last_n_days = models.PositiveIntegerField(default=0);
