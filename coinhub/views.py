# Django
from django.shortcuts import render
from django.contrib.auth import logout
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import datetime
import json
import requests

# call Coinapi for historical price collection
def collect_data_historical(symbol_id, asset_id_base, asset_id_quote, period_id,
                            time_start, time_end = '', ):
    url = 'https://rest.coinapi.io/v1/ohlcv/' + symbol_id + '_SPOT_' + asset_id_base + \
    '_' + asset_id_quote + '/history?period_id=' + period_id + '&time_start=' + \
    time_start + '&time_end=' + time_end 
    response = make_request(url)
    add_data(response)
    return response

# call coin marketcap for current market data
def collect_data_current():
    url = "https://api.coinmarketcap.com/v1/ticker/"
    response = make_request(url)
    return response

def make_request(url):
    return requests.get(url, verify=False)

#view json return from coinmarketcap api
def Data(request):
    current_time = datetime.datetime.utcnow()
    start_time = current_time - datetime.timedelta(minutes = 15, 
        seconds = current_time.second % 10, microseconds = current_time.microsecond)
    end_time = current_time - datetime.timedelta(microseconds = current_time.microsecond)
    response = collect_data_current()
    return HttpResponse(response, content_type='application/json')