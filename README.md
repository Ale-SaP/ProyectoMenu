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

## Filosofía y estructura

La idea general de el proyecto es ofrecer la mejor experiencia de usuario y simplificar el desarrollo lo máximo posible.

Separamos los componentes más grandes en cada pantalla en diferentes partes (mayormente) independientes en la carpeta Templates.
Utilizamos HTMX para realizar las cargas condicionales y parciales de estos archivos, haciendo peticiones a endpoints (`views.py`) y recibiendo HTML.
Esto nos permite realizar algo similar al Lazy Loading de React, en donde cada parte de la página se pide por separado y se ensambla/toma su lugar en la página, esta concurrencia de paquetes de menor tamaño acelera la carga en redes más lentas. Los paquetes estáticos (css, js, svgs) se encuentran en la carpeta static, pero deben ser compilados.

## Contenido actual

### HTML
- index.html: controla la estructura general de la página y el encabezado, también hace las peticiones para el resto de las partes cuando carga.
- content.html: por cada elemento de la base de datos en una categoría específica se genera una fila en la página.
- modal_content.html: cada vez que se hace click en el carrito de compras de un item generado por content.html se devuelve un modal con los datos de ese producto.
- shopping_cart.html: maneja la tabla con los items a comprar una vez terminamos las compras.

### CSS
- buttons.css: da estilo a los botones que se ocupan en toda la página.
- fonts.css: da estilo a los textos en la página dependiendo de las resoluciones.

### JS
- cart.js: permite añadir items al carrito, eliminarlos o cambiar la cantidad. Incluye el html de cada fila.
- modal.js: incluye las funcionalidades para abrir o cerrar los modals de modal_content.
