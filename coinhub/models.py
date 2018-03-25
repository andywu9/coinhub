from django.db import models
from django.urls import reverse
import requests
import datetime


# Hold the main page table data for quick overview of market
class CurrentCoinInfo(models.Model):
    circulating_supply = models.DecimalField(max_digits=19,
                                             decimal_places=2, default=0)
    market_cap = models.DecimalField(max_digits=19,
                                     decimal_places=2, default=0)
    name = models.CharField(primary_key=True, max_length=30, default="")
    price = models.DecimalField(max_digits=19, decimal_places=10, default=0)
    price_change_day = models.DecimalField(max_digits=19,
                                           decimal_places=2, default=0)
    price_change_hour = models.DecimalField(max_digits=19,
                                            decimal_places=2, default=0)
    price_change_week = models.DecimalField(max_digits=19,
                                            decimal_places=2, default=0)
    rank = models.IntegerField(default=-1)
    symbol = models.CharField(max_length=6, default="")
    volume = models.DecimalField(max_digits=19, decimal_places=2, default=0)


# Hold the historical data that is shown as a small graph on main page
class GraphData(models.Model):
    circulating_supply = models.DecimalField(max_digits=19, decimal_places=2,
                                             default=0)
    historical_price = models.DecimalField(max_digits=19, decimal_places=10,
                                           default=0)
    market_cap = models.DecimalField(max_digits=19, decimal_places=2,
                                     default=0)
    name = models.CharField(max_length=30, default="")
    time_collected = models.DateTimeField(default=datetime.datetime.now(),
                                          blank=True)
    volume = models.DecimalField(max_digits=19, decimal_places=2,
                                 default=0)

    class Meta:
        unique_together = ('time_collected', 'name')

