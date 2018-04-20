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

    # Reformat database to match usage in front-end.
    # Reorganizes data by grouping rows by coin name
    # and referencing that group with the coin's name as a key

    print(coins)
    print(historical_data)

    graph_data = {}
    for row in historical_data:
        if row['name'] in graph_data:
            graph_data[row['name']].append(row)
        else:
            graph_data[row['name']] = [row]

    # send the information to the front end
    return render(request, 'pages/home.html',
                  {"coins": coins,
                   "historical": json.dumps(graph_data, default=str)})
