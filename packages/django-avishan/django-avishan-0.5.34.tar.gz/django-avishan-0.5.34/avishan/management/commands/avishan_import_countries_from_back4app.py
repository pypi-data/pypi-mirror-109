import requests
import json
import urllib

from avishan.models import Country
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Imports countries from back4app'

    def handle(self, *args, **kwargs):
        length = 50
        skip = 0
        for _ in range(5):
            url = f'https://parseapi.back4app.com/classes/Continentscountriescities_Country?' \
                  f'skip={skip}&limit={length}&order=code'
            headers = {
                'X-Parse-Application-Id': '1ki6GGgah5AgrQDxPmBvWaBZEqRKg3WpCFqufYqN',
                # This is your app's application id
                'X-Parse-REST-API-Key': 'fbe0MZpyF4Gwt2EFp5GUnSfSEJUC40FdSMfGepHp'  # This is your app's REST API key
            }
            data = json.loads(
                requests.get(url, headers=headers).content.decode('utf-8'))  # Here you have the data that you need
            for item in data['results']:
                try:
                    country = Country.objects.get(alpha_2_code=item['code'])
                except Country.DoesNotExist:
                    continue
                country.back4app_object_id = item['objectId']
                country.save()
                print(f"{country.name} updated")
            skip += length
