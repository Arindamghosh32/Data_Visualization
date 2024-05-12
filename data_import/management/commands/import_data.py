from django.db import models
from django.utils import timezone
import logging
import json
from django.core.management.base import BaseCommand
from users.models import Users
from datetime import datetime


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



class Command(BaseCommand):
    help = 'Import data from JSON file to MySQL database'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']

        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        total_records = len(data)
        logger.info(f'Total Records in json file: {total_records}')

        records_processed = 0

        for item in data:
            # Convert empty strings to None for certain fields
            item['end_year'] = item['end_year'] if item['end_year'] else None
            item['start_year'] = item['start_year'] if item['start_year'] else None
            item['impact'] = item['impact'] if item['impact'] else None
            item['intensity'] = item['intensity'] if item['intensity'] else None
            item['likelihood'] = item['likelihood'] if item['likelihood'] else None
            item['relevance'] = item['relevance'] if item['relevance'] else None

            # Parse date strings only if they are not empty
            if item['added']:
                try:
                    item['added'] = datetime.strptime(item['added'], '%B, %d %Y %H:%M:%S')
                except ValueError:
                    item['added'] = None  # Handle invalid date format gracefully
            else:
                item['added'] = None

            if item['published']:
                try:
                    item['published'] = datetime.strptime(item['published'], '%B, %d %Y %H:%M:%S')
                except ValueError:
                    item['published'] = None  # Handle invalid date format gracefully
            else:
                item['published'] = None

            Users.objects.create(**item)
            records_processed += 1
            logger.info(f'Record {records_processed}/{total_records} processed')

        logger.info('Data import completed')
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
