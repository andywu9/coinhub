from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView

from .models import User


import datetime
import json
import pprint
import pymongo
import requests

from pymongo import MongoClient

#add data to MongoDB database
def add_data(data):
    client = MongoClient()
    database = client.data
    tables = database.tables
    my_data = json.loads(data.text)
    tables.insert_many(my_data)

# call Coinapi and send response to add to database
def collect_data_historical(symbol_id, asset_id_base, asset_id_quote, period_id,
                            time_start, time_end = '', ):

    url = 'https://rest.coinapi.io/v1/ohlcv/' + symbol_id + '_SPOT_' + asset_id_base + \
    '_' + asset_id_quote + '/history?period_id=' + period_id + '&time_start=' + \
    time_start + '&time_end=' + time_end 
    response = make_request(url)
    add_data(response)
    return response

def collect_data_current():
    url = "https://api.coinmarketcap.com/v1/ticker/"
    response = make_request(url)
    add_data(response)
    return response
    

def make_request(url):
    return requests.get(url, verify=False)

def Data(request):
    current_time = datetime.datetime.utcnow()
    start_time = current_time - datetime.timedelta(minutes = 15, seconds = current_time.second % 10, microseconds = current_time.microsecond)
    end_time = current_time - datetime.timedelta(microseconds = current_time.microsecond)
    response = collect_data_current()
    return HttpResponse(response, content_type='application/json')


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):

    fields = ['name', ]

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'
