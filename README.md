# Proyecto Menú/E-commerce

## Cómo correrlo en local?

### Requerimientos
- MYSQL Server 8.0 o posterior
- Python 3.10 o posterior
- DBeaver (opcional)

### Pasos
- Navegue hasta el directorio base de `myproject` 
- Instale las dependencias del proyecto de Django con `pip install -r requirements.txt`
- Mediante el gestor de bases de datos de elección o sobre la terminal de SQLServer, ejecute las primeras 2 queries en el archivo <b>BD-structure.sql</b> para instanciar la base de datos y el usuario
- Ejecute `python manage.py makemigrations` y seguido `python manage.py migrate`
- Para cargar la base de datos con los datos de muestra es
  - ```python manage.py import_json --organization ./mock-data/organization.json --org_configs  ./mock-data/org_configs.json --menus ./mock-data/menus.json --products ./mock-data/products.json --categories ./mock-data/categories.json --menu_product ./mock-data/menu_product.json --product_category ./mock-data/product_category.json```
- Ejecuta `python manage.py collectstatic` para generar los archivos estáticos
- Por último, para levantar en localhost ejecute `python manage.py runserver`
