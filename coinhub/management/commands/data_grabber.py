from django.core.management.base import BaseCommand, CommandError
from coinhub import pullData as myModel

# Run via cron job similar to the form shown below
# * * * * * python manage.py data_grabber --url https://api.coinmarketcap.com/v1/ticker/
class Command(BaseCommand):
    help = 'Collects data from an exchange'

    def add_arguments(self, parser):
        parser.add_argument('--url', type=str)

    def handle(self, *args, **options):
            exchange_url = options['url']
            my_puller = myModel.CoinDataPuller(exchange_url)
            my_puller.collect_new_data()
            my_puller.save()