import csv
"""import sys
from pathlib import Path"""
from django.core.management.base import BaseCommand
from todo.models import Car_Listing

class Command(BaseCommand):
    help = 'Import data from CSV files into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_files', nargs='+', type=str, help='C:\\Users\\super\\Capstone_project\\backend\\todo\\Scrapping\\result')
    
    def handle(self, *args, **options):
        csv_files = options['csv_files']

        for csv_file in csv_files:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  

                for row in reader:
                    Car_Listing.objects.create(
                        source=row[0],
                        make =row[1],
                        model =row[2],
                        year = row[3],
                        price = row[4],
                        mileage = row[5],
                        location = row[6],
                        listing_date = row[7],
                        link_to_buyer = row[8],
                        link_to_image = row[9],
                    )

            self.stdout.write(self.style.SUCCESS(f'Data from {csv_file} imported successfully'))
        
        
        