import json
from django.core.management.base import BaseCommand
from usermenu.models import (
    Organization,
    OrgConfigs,
    Menu,
    Product,
    MenuProduct,
    Category,
    ProductCategory
)

# Command to seed everything
# python manage.py import_json --organization ./mock-data/organization.json --org_configs  ./mock-data/org_configs.json --menus ./mock-data/menus.json --products ./mock-data/products.json --categories ./mock-data/categories.json --menu_product ./mock-data/menu_product.json --product_category ./mock-data/product_category.json

class Command(BaseCommand):
    help = 'Importa datos desde archivos JSON a la base de datos'

    def add_arguments(self, parser):
        parser.add_argument('--organization', type=str, help='Ruta al archivo JSON de organizaciones')
        parser.add_argument('--org_configs', type=str, help='Ruta al archivo JSON de configuraciones de organizaciones')
        parser.add_argument('--menus', type=str, help='Ruta al archivo JSON de menús')
        parser.add_argument('--products', type=str, help='Ruta al archivo JSON de productos')
        parser.add_argument('--categories', type=str, help='Ruta al archivo JSON de categorías')
        parser.add_argument('--menu_product', type=str, help='Ruta al archivo JSON de relación menús-productos')
        parser.add_argument('--product_category', type=str, help='Ruta al archivo JSON de relación productos-categorías')

    def handle(self, *args, **kwargs):
        if kwargs['organization']:
            self.import_organizations(kwargs['organization'])

        if kwargs['org_configs']:
            self.import_org_configs(kwargs['org_configs'])

        if kwargs['menus']:
            self.import_menus(kwargs['menus'])

        if kwargs['products']:
            self.import_products(kwargs['products'])

        if kwargs['categories']:
            self.import_categories(kwargs['categories'])

        if kwargs['menu_product']:
            self.import_menu_product(kwargs['menu_product'])

        if kwargs['product_category']:
            self.import_product_category(kwargs['product_category'])

    def import_organizations(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            organizations = json.load(f)
            for org_data in organizations:
                print(org_data)
                print(org_data["name"])
                org, created = Organization.objects.get_or_create(
                    name=org_data['name'],
                    defaults={
                        'location': org_data['location'],
                        'status': org_data['status'],
                        'attendant': org_data.get('attendant', '')
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Organización creada: {org.name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Organización existente: {org.name}"))

    def import_org_configs(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            configs = json.load(f)
            for config_data in configs:
                org = Organization.objects.get(id_org=config_data['id_org'])
                config, created = OrgConfigs.objects.get_or_create(
                    id_org=org,
                    defaults={
                        'nombre_tienda': config_data.get('nombre_tienda', ''),
                        'contenido_inicial': config_data.get('contenido_inicial', ''),
                        'logo_url': config_data.get('logo_url', ''),
                        'descripcion_logo': config_data.get('descripcion_logo', ''),
                        'texto_superior': config_data.get('texto_superior', ''),
                        'horario_atencion': config_data.get('horario_atencion', ''),
                        'telefono_contacto': config_data.get('telefono_contacto', '')
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Configuración creada para: {org.name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Configuración existente para: {org.name}"))

    def import_menus(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            menus = json.load(f)
            for menu_data in menus:
                org = Organization.objects.get(id_org=menu_data['id_org'])
                menu, created = Menu.objects.get_or_create(
                    name=menu_data['name'],
                    id_org=org,
                    defaults={
                        'creation_date': menu_data.get('creation_date'),
                        'status': menu_data.get('status', True)
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Menú creado: {menu.name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Menú existente: {menu.name}"))

    def import_products(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            products = json.load(f)
            for product_data in products:
                product, created = Product.objects.get_or_create(
                    name=product_data['name'],
                    defaults={
                        'description': product_data.get('description', ''),
                        'price': product_data['price'],
                        'status': product_data.get('status', True)
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Producto creado: {product.name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Producto existente: {product.name}"))

    def import_categories(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            categories = json.load(f)
            for category_data in categories:
                category, created = Category.objects.get_or_create(
                    name=category_data['name'],
                    defaults={
                        'svg_path': category_data.get('svg_path', '')
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Categoría creada: {category.name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Categoría existente: {category.name}"))

    def import_menu_product(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            menu_products = json.load(f)
            for mp_data in menu_products:
                menu = Menu.objects.get(id_menu=mp_data['id_menu'])
                product = Product.objects.get(id_product=mp_data['id_product'])
                mp, created = MenuProduct.objects.get_or_create(
                    id_menu=menu,
                    id_product=product
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Relacion Menú-Producto creada: {menu.name} - {product.name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Relacion Menú-Producto existente: {menu.name} - {product.name}"))

    def import_product_category(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            product_categories = json.load(f)
            for pc_data in product_categories:
                category = Category.objects.get(id_category=pc_data['id_category'])
                product = Product.objects.get(id_product=pc_data['id_product'])
                pc, created = ProductCategory.objects.get_or_create(
                    id_category=category,
                    id_product=product
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Relacion Producto-Categoría creada: {product.name} - {category.name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Relacion Producto-Categoría existente: {product.name} - {category.name}"))