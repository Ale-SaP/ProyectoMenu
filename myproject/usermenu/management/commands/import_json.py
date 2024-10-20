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

class Command(BaseCommand):
    help = 'Import data from JSON files into the database'

    def add_arguments(self, parser):
        parser.add_argument('--organizations', type=str, help='Path to organizations JSON file')
        parser.add_argument('--org_configs', type=str, help='Path to org_configs JSON file')
        parser.add_argument('--catalogs', type=str, help='Path to catalogs JSON file')
        parser.add_argument('--categories', type=str, help='Path to categories JSON file')
        parser.add_argument('--products', type=str, help='Path to products JSON file')
        parser.add_argument('--product_categories', type=str, help='Path to product_categories JSON file')
        parser.add_argument('--clients', type=str, help='Path to clients JSON file')
        parser.add_argument('--orders', type=str, help='Path to orders JSON file')
        parser.add_argument('--details', type=str, help='Path to details JSON file')
        parser.add_argument('--payment_methods', type=str, help='Path to payment_methods JSON file')
        parser.add_argument('--payment_statuses', type=str, help='Path to payment_statuses JSON file')
        parser.add_argument('--receipts', type=str, help='Path to receipts JSON file')
        parser.add_argument('--sectors', type=str, help='Path to sectors JSON file')
        parser.add_argument('--sector_categories', type=str, help='Path to sector_categories JSON file')

    def handle(self, *args, **kwargs):
        if kwargs['organizations']:
            self.import_organizations(kwargs['organizations'])

        if kwargs['org_configs']:
            self.import_org_configs(kwargs['org_configs'])

        if kwargs['catalogs']:
            self.import_catalogs(kwargs['catalogs'])

        if kwargs['categories']:
            self.import_categories(kwargs['categories'])

        if kwargs['products']:
            self.import_products(kwargs['products'])

        if kwargs['product_categories']:
            self.import_product_categories(kwargs['product_categories'])

        if kwargs['clients']:
            self.import_clients(kwargs['clients'])

        if kwargs['orders']:
            self.import_orders(kwargs['orders'])

        if kwargs['details']:
            self.import_details(kwargs['details'])

        if kwargs['payment_methods']:
            self.import_payment_methods(kwargs['payment_methods'])

        if kwargs['payment_statuses']:
            self.import_payment_statuses(kwargs['payment_statuses'])

        if kwargs['receipts']:
            self.import_receipts(kwargs['receipts'])

        if kwargs['sectors']:
            self.import_sectors(kwargs['sectors'])

        if kwargs['sector_categories']:
            self.import_sector_categories(kwargs['sector_categories'])

    def import_organizations(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            organizations = json.load(f)
            for data in organizations:
                org, created = Organization.objects.get_or_create(
                    uuid=data['uuid'],
                    defaults={
                        'name': data['name']
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created Organization: {org.name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Organization already exists: {org.name}"))

    def import_org_configs(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            configs = json.load(f)
            for data in configs:
                org = Organization.objects.get(uuid=data['organization_uuid'])
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

    def import_catalogs(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            catalogs = json.load(f)
            for data in catalogs:
                org = Organization.objects.get(uuid=data['organization_uuid'])
                catalog, created = Catalog.objects.get_or_create(
                    uuid=data['uuid'],
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

    def import_categories(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            categories = json.load(f)
            for data in categories:
                category, created = Category.objects.get_or_create(
                    uuid=data['uuid'],
                    defaults={
                        'name': data['name'],
                        'creation_date': data.get('creation_date'),
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created Category: {category.name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Category already exists: {category.name}"))

    def import_products(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            products = json.load(f)
            for data in products:
                catalog = Catalog.objects.get(uuid=data['catalog_uuid'])
                product, created = Product.objects.get_or_create(
                    uuid=data['uuid'],
                    defaults={
                        'name': data['name'],
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

    def import_product_categories(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            relations = json.load(f)
            for data in relations:
                product = Product.objects.get(uuid=data['product_uuid'])
                category = Category.objects.get(uuid=data['category_uuid'])
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

    def import_clients(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            clients = json.load(f)
            for data in clients:
                client, created = Client.objects.get_or_create(
                    uuid=data['uuid'],
                    defaults={
                        'name': data['name'],
                        'creation_date': data.get('creation_date'),
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created Client: {client.name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Client already exists: {client.name}"))

    def import_orders(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            orders = json.load(f)
            for data in orders:
                client = Client.objects.get(uuid=data['client_uuid'])
                order, created = Order.objects.get_or_create(
                    uuid=data['uuid'],
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

    def import_details(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            details = json.load(f)
            for data in details:
                order = Order.objects.get(uuid=data['order_uuid'])
                product = Product.objects.get(uuid=data['product_uuid'])
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

    def import_payment_methods(self, file_path):
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

    def import_payment_statuses(self, file_path):
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

    def import_receipts(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            receipts = json.load(f)
            for data in receipts:
                order = Order.objects.get(uuid=data['order_uuid'])
                payment_method = PaymentMethod.objects.get(method_name=data['payment_method_name'])
                payment_status = PaymentStatus.objects.get(status_name=data['payment_status_name'])
                receipt, created = Receipt.objects.get_or_create(
                    uuid=data['uuid'],
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

    def import_sectors(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            sectors = json.load(f)
            for data in sectors:
                org = Organization.objects.get(uuid=data['organization_uuid'])
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

    def import_sector_categories(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            relations = json.load(f)
            for data in relations:
                sector = Sector.objects.get(name=data['sector_name'])
                category = Category.objects.get(uuid=data['category_uuid'])
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
