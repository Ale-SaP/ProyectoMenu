# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
import uuid

# 1. Organization (Base Model)
class Organization(models.Model):
    id_organization = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'organization'


# 2. Catalog (Depends on Organization)
class Catalog(models.Model):
    id_catalog = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    status = models.IntegerField(blank=True, null=True)
    creation_date = models.DateTimeField(blank=True, null=True)
    id_organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,  # Changed from DO_NOTHING to CASCADE
        db_column='id_organization',
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'catalog'


# 3. Category (Independent)
class Category(models.Model):
    id_category = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    creation_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'category'


# 4. Client (Independent)
class Client(models.Model):
    id_client = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    creation_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'client'


# 5. PaymentMethod (Independent)
class PaymentMethod(models.Model):
    id_payment_method = models.AutoField(primary_key=True)
    method_name = models.CharField(max_length=255)
    creation_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'payment_method'


# 6. PaymentStatus (Independent)
class PaymentStatus(models.Model):
    id_payment_status = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=255)
    creation_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'payment_status'


# 7. Product (Depends on Catalog)
class Product(models.Model):
    id_product = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    image_link_alt = models.CharField(max_length=255, blank=True, null=True)
    image_link = models.CharField(max_length=255, blank=True, null=True)
    creation_date = models.DateTimeField(blank=True, null=True)
    id_catalog = models.ForeignKey(
        Catalog,
        on_delete=models.CASCADE,  # Changed from DO_NOTHING to CASCADE
        db_column='id_catalog',
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'product'


# 8. Sector (Depends on Organization)
class Sector(models.Model):
    id_sector = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    creation_date = models.DateTimeField(blank=True, null=True)
    id_organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,  # Changed from DO_NOTHING to CASCADE
        db_column='id_organization',
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'sector'


# 9. OrgConfig (Depends on Organization)
class OrgConfig(models.Model):
    id_org_config = models.AutoField(primary_key=True)
    nombre_tienda = models.CharField(max_length=255, blank=True, null=True)
    contenido_inicial = models.IntegerField(blank=True, null=True)
    logo_url = models.CharField(max_length=255, blank=True, null=True)
    descripcion_logo = models.CharField(max_length=255, blank=True, null=True)
    texto_superior = models.CharField(max_length=255, blank=True, null=True)
    horario_atencion = models.CharField(max_length=255, blank=True, null=True)
    telefono_contacto = models.CharField(max_length=50, blank=True, null=True)
    creation_date = models.DateTimeField(blank=True, null=True)
    id_organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,  # Changed from DO_NOTHING to CASCADE
        db_column='id_organization',
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'org_config'


# 10. Order (Depends on Client)
class Order(models.Model):
    id_order = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    order_date = models.DateField()
    creation_date = models.DateTimeField(blank=True, null=True)
    id_client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,  # Changed from DO_NOTHING to CASCADE
        db_column='id_client',
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'order'


# 11. Detail (Depends on Order and Product)
class Detail(models.Model):
    id_detail = models.AutoField(primary_key=True)
    quantity = models.IntegerField()
    creation_date = models.DateTimeField(blank=True, null=True)
    id_order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,  # Changed from DO_NOTHING to CASCADE
        db_column='id_order',
        blank=True,
        null=True
    )
    id_product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,  # Changed from DO_NOTHING to CASCADE
        db_column='id_product',
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'detail'


# 12. ProductCategory (Depends on Product and Category)
class ProductCategory(models.Model):
    id_product_category = models.AutoField(primary_key=True)
    creation_date = models.DateTimeField(blank=True, null=True)
    id_category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,  # Changed from DO_NOTHING to CASCADE
        db_column='id_category',
        blank=True,
        null=True
    )
    id_product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,  # Changed from DO_NOTHING to CASCADE
        db_column='id_product',
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'product_category'


# 13. Receipt (Depends on Order, PaymentMethod, PaymentStatus)
class Receipt(models.Model):
    id_receipt = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    receipt_date = models.DateField()
    creation_date = models.DateTimeField(blank=True, null=True)
    id_order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,  # Changed from DO_NOTHING to CASCADE
        db_column='id_order',
        blank=True,
        null=True
    )
    id_payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.CASCADE,  # Changed from DO_NOTHING to CASCADE
        db_column='id_payment_method',
        blank=True,
        null=True
    )
    id_payment_status = models.ForeignKey(
        PaymentStatus,
        on_delete=models.CASCADE,  # Changed from DO_NOTHING to CASCADE
        db_column='id_payment_status',
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'receipt'


# 14. SectorCategory (Depends on Sector and Category)
class SectorCategory(models.Model):
    id_sector_category = models.AutoField(primary_key=True)
    creation_date = models.DateTimeField(blank=True, null=True)
    id_sector = models.ForeignKey(
        Sector,
        on_delete=models.CASCADE,  # Changed from DO_NOTHING to CASCADE
        db_column='id_sector',
        blank=True,
        null=True
    )
    id_category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,  # Changed from DO_NOTHING to CASCADE
        db_column='id_category',
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'sector_category'
