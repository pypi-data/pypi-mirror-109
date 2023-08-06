import requests
import json
import urllib

from avishan.models import Country, City
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Imports countries from back4app'

    def handle(self, *args, **kwargs):
        length = 50
        for country in Country.objects.all():
            if country.back4app_object_id is None:
                continue

            skip = 0

            while True:
                where = urllib.parse.quote_plus("""
                {
                    "country": {
                        "__type": "Pointer",
                        "className": "Continentscountriescities_Country",
                        "objectId": "%s"
                    }
                }
                """ % country.back4app_object_id)
                url = 'https://parseapi.back4app.com/classes/Continentscountriescities_City' \
                      f'?skip={skip}&limit=50&where=%s' % where
                headers = {
                    'X-Parse-Application-Id': '1ki6GGgah5AgrQDxPmBvWaBZEqRKg3WpCFqufYqN',
                    'X-Parse-REST-API-Key': 'fbe0MZpyF4Gwt2EFp5GUnSfSEJUC40FdSMfGepHp'
                }
                data = json.loads(requests.get(url, headers=headers).content.decode('utf-8'))
                if len(data['results']) == 0:
                    break
                for item in data['results']:
                    try:
                        city = City.objects.get(back4app_object_id=item['objectId'])
                    except City.DoesNotExist:
                        city = City.objects.create(back4app_object_id=item['objectId'],
                                                   country=country)
                    city.title = item['name']
                    city.latitude = item['location']['latitude']
                    city.longitude = item['location']['longitude']
                    city.save()
                skip += length
            print(f'{country.name} {skip}')
