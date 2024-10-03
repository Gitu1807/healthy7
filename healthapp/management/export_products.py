# /home/visionacademy/healthy7/healthapp/management/commands/export_products.py

import csv
from django.core.management.base import BaseCommand
from healthapp.models import Product

class Command(BaseCommand):
    help = 'Export products to CSV file'

    def handle(self, *args, **kwargs):
        file_path = 'products.csv'
        with open(file_path, 'w', newline='') as csvfile:
            fieldnames = ['name', 'price', 'cat', 'cdetail', 'cimage', 'is_active']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for product in Product.objects.all():
                writer.writerow({
                    'name': product.name,
                    'price': product.price,
                    'cat': product.get_cat_display(),
                    'cdetail': product.cdetail,
                    'cimage': product.cimage.url if product.cimage else '',
                    'is_active': product.is_active,
                })

        self.stdout.write(self.style.SUCCESS(f'Successfully exported products to {file_path}'))
