import simplejson as json
from django.core import serializers
from django.shortcuts import render
from django.db.models import F
from coinhub import models


# home view takes the information from the backend and sends it to the
# front end
def home(request):

    # Obtain data from the back end
    json_serializer = serializers.get_serializer("json")()
    coins = json_serializer.serialize(
        models.CurrentCoinInfo.objects.all().order_by('rank'), ensure_ascii=True)
    historical_data = models.GraphData.objects.annotate(
        idmod2=F('id') % 2).filter(idmod2=0).order_by('time_collected').values()
    conversion = models.CurrentCoinInfo.objects.all().values()
    exchange = models.ExchangeInfo.objects.all().values()

    # find the symbol for each coin so we can find the associated best exchange
    value_change_pairs = {}
    for item in conversion:
        value_change_pairs[item["name"]] = item["symbol"]

    # store best buy/sell prices for display
    exchange_data = {}
    for ex in exchange:
        exchange_data[ex["name"][:3]] = [ex["buy_price"], ex["buy_ex"], ex["sell_price"], ex["sell_ex"]]


    graph_data = {}
    for row in historical_data:
        if row['name'] in graph_data:
            graph_data[row['name']].append(row)
        else:
            graph_data[row['name']] = [row]

    # send the information to the front end
    return render(request, 'pages/home.html',
                  {"coins": coins,
                   "historical": json.dumps(graph_data, default=str),
                   "value_change": json.dumps(value_change_pairs, default=str),
                   "exchange_data": json.dumps(exchange_data, default=str)})
