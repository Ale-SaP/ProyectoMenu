import json
from django.core.management.base import BaseCommand
from usermenu.models import (
    Organization,
    OrgConfig,
    Catalog,
    Category,
    Product,
    ProductCategory,
    Client,
    Order,
    Detail,
    PaymentMethod,
    PaymentStatus,
    Receipt,
    Sector,
    SectorCategory,
)


"""python manage.py import_json
    --organization ./mock-data/organization.json
    --org_config ./mock-data/org_config.json
    --catalog ./mock-data/catalog.json
    --category ./mock-data/category.json
    --product ./mock-data/product.json
    --sector ./mock-data/sector.json
    --sector_category ./mock-data/sector_category.json
    --product_category ./mock-data/product_category.json
    --payment_method ./mock-data/payment_method.json

    --payment_status ./mock-data/payment_status.json
    --receipt ./mock-data/receipt.json
    --client ./mock-data/client.json
    --order ./mock-data/order.json
    --detail ./mock-data/detail.json
"""

class Command(BaseCommand):
    help = 'Import data from JSON files into the database'

    def add_arguments(self, parser):
        parser.add_argument('--organization', type=str, help='Path to organization JSON file')
        parser.add_argument('--org_config', type=str, help='Path to org_config JSON file')
        parser.add_argument('--catalog', type=str, help='Path to catalog JSON file')
        parser.add_argument('--category', type=str, help='Path to category JSON file')
        parser.add_argument('--product', type=str, help='Path to product JSON file')
        parser.add_argument('--product_category', type=str, help='Path to product_category JSON file')
        parser.add_argument('--client', type=str, help='Path to client JSON file')
        parser.add_argument('--order', type=str, help='Path to order JSON file')
        parser.add_argument('--detail', type=str, help='Path to detail JSON file')
        parser.add_argument('--payment_method', type=str, help='Path to payment_method JSON file')
        parser.add_argument('--payment_status', type=str, help='Path to payment_status JSON file')
        parser.add_argument('--receipt', type=str, help='Path to receipt JSON file')
        parser.add_argument('--sector', type=str, help='Path to sector JSON file')
        parser.add_argument('--sector_category', type=str, help='Path to sector_category JSON file')

    def handle(self, *args, **kwargs):
        if kwargs['organization']:
            self.import_organization(kwargs['organization'])

        if kwargs['org_config']:
            self.import_org_config(kwargs['org_config'])

        if kwargs['catalog']:
            self.import_catalog(kwargs['catalog'])

        if kwargs['category']:
            self.import_category(kwargs['category'])

        if kwargs['product']:
            self.import_product(kwargs['product'])

        if kwargs['product_category']:
            self.import_product_category(kwargs['product_category'])

        if kwargs['client']:
            self.import_client(kwargs['client'])

        if kwargs['order']:
            self.import_order(kwargs['order'])

        if kwargs['detail']:
            self.import_detail(kwargs['detail'])

        if kwargs['payment_method']:
            self.import_payment_method(kwargs['payment_method'])

        if kwargs['payment_status']:
            self.import_payment_status(kwargs['payment_status'])

        if kwargs['receipt']:
            self.import_receipt(kwargs['receipt'])

        if kwargs['sector']:
            self.import_sector(kwargs['sector'])

        if kwargs['sector_category']:
            self.import_sector_category(kwargs['sector_category'])

    def import_organization(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            organization = json.load(f)
            for data in organization:
                org, created = Organization.objects.get_or_create(
                    defaults={
                        'name': data['name']
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created Organization: {org.name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Organization already exists: {org.name}"))

    def import_org_config(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            configs = json.load(f)
            for data in configs:
                org = Organization.objects.get(id_organization=data['id_organization'])
                config, created = OrgConfig.objects.get_or_create(
                    id_organization=org,
                    defaults={
                        'nombre_tienda': data.get('nombre_tienda'),
                        'contenido_inicial': data.get('contenido_inicial'),
                        'logo_url': data.get('logo_url'),
                        'descripcion_logo': data.get('descripcion_logo'),
                        'texto_superior': data.get('texto_superior'),
                        'horario_atencion': data.get('horario_atencion'),
                        'telefono_contacto': data.get('telefono_contacto'),
                        'creation_date': data.get('creation_date'),
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created OrgConfig for: {org.name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"OrgConfig already exists for: {org.name}"))

    def import_catalog(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            catalog = json.load(f)
            for data in catalog:
                org = Organization.objects.get(id_organization=data['id_organization'])
                catalog, created = Catalog.objects.get_or_create(
                    defaults={
                        'name': data['name'],
                        'status': data.get('status'),
                        'creation_date': data.get('creation_date'),
                        'id_organization': org,
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created Catalog: {catalog.name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Catalog already exists: {catalog.name}"))

    def import_category(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            category = json.load(f)
            for data in category:
                category, created = Category.objects.get_or_create(
                    name=data['name'],
                    defaults={
                        'creation_date': data.get('creation_date'),
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created Category: {category.name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Category already exists: {category.name}"))

    def import_product(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            product = json.load(f)
            for data in product:
                catalog = Catalog.objects.get(id_catalog=data['id_catalog'])
                product, created = Product.objects.get_or_create(
                    name=data['name'],
                    defaults={
                        'description': data.get('description'),
                        'price': data.get('price'),
                        'status': data.get('status'),
                        'image_link_alt': data.get('image_link_alt'),
                        'image_link': data.get('image_link'),
                        'creation_date': data.get('creation_date'),
                        'id_catalog': catalog,
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created Product: {product.name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Product already exists: {product.name}"))

    def import_product_category(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            relations = json.load(f)
            for data in relations:
                product = Product.objects.get(id_product=data['id_product'])
                category = Category.objects.get(id_category=data['id_category'])
                pc, created = ProductCategory.objects.get_or_create(
                    id_product=product,
                    id_category=category,
                    defaults={
                        'creation_date': data.get('creation_date'),
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(
                        f"Linked Product '{product.name}' with Category '{category.name}'"))
                else:
                    self.stdout.write(self.style.WARNING(
                        f"Product '{product.name}' already linked with Category '{category.name}'"))

    def import_client(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            client = json.load(f)
            for data in client:
                client, created = Client.objects.get_or_create(
                    name=data['name'],
                    defaults={
                        'creation_date': data.get('creation_date'),
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created Client: {client.name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Client already exists: {client.name}"))

    def import_order(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            order = json.load(f)
            for data in order:
                client = Client.objects.get(id_client=data['id_client'])
                order, created = Order.objects.get_or_create(
                    id_order=data["id_order"],
                    defaults={
                        'order_date': data['order_date'],
                        'creation_date': data.get('creation_date'),
                        'id_client': client,
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created Order: {order.uuid}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Order already exists: {order.uuid}"))

    def import_detail(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            detail = json.load(f)
            for data in detail:
                order = Order.objects.get(id_order=data['id_order'])
                product = Product.objects.get(id_product=data['id_product'])
                detail, created = Detail.objects.get_or_create(
                    id_order=order,
                    id_product=product,
                    defaults={
                        'quantity': data['quantity'],
                        'creation_date': data.get('creation_date'),
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(
                        f"Created Detail for Order '{order.uuid}' and Product '{product.name}'"))
                else:
                    self.stdout.write(self.style.WARNING(
                        f"Detail already exists for Order '{order.uuid}' and Product '{product.name}'"))

    def import_payment_method(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            methods = json.load(f)
            for data in methods:
                method, created = PaymentMethod.objects.get_or_create(
                    method_name=data['method_name'],
                    defaults={
                        'creation_date': data.get('creation_date'),
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created PaymentMethod: {method.method_name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"PaymentMethod already exists: {method.method_name}"))

    def import_payment_status(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            statuses = json.load(f)
            for data in statuses:
                status, created = PaymentStatus.objects.get_or_create(
                    status_name=data['status_name'],
                    defaults={
                        'creation_date': data.get('creation_date'),
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created PaymentStatus: {status.status_name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"PaymentStatus already exists: {status.status_name}"))

    def import_receipt(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            receipt = json.load(f)
            for data in receipt:
                order = Order.objects.get(id_order=data['id_order'])
                payment_method = PaymentMethod.objects.get(method_name=data['payment_method_name'])
                payment_status = PaymentStatus.objects.get(status_name=data['payment_status_name'])
                receipt, created = Receipt.objects.get_or_create(
                    defaults={
                        'receipt_date': data['receipt_date'],
                        'creation_date': data.get('creation_date'),
                        'id_order': order,
                        'id_payment_method': payment_method,
                        'id_payment_status': payment_status,
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created Receipt: {receipt.uuid}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Receipt already exists: {receipt.uuid}"))

    def import_sector(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            sector = json.load(f)
            for data in sector:
                org = Organization.objects.get(id_organization=data['id_organization'])
                sector, created = Sector.objects.get_or_create(
                    name=data['name'],
                    id_organization=org,
                    defaults={
                        'creation_date': data.get('creation_date'),
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created Sector: {sector.name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Sector already exists: {sector.name}"))

    def import_sector_category(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            relations = json.load(f)
            for data in relations:
                sector = Sector.objects.get(id_sector=data['id_sector'])
                category = Category.objects.get(id_category=data['id_category'])
                sc, created = SectorCategory.objects.get_or_create(
                    id_sector=sector,
                    id_category=category,
                    defaults={
                        'creation_date': data.get('creation_date'),
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(
                        f"Linked Sector '{sector.name}' with Category '{category.name}'"))
                else:
                    self.stdout.write(self.style.WARNING(
                        f"Sector '{sector.name}' already linked with Category '{category.name}'"))
