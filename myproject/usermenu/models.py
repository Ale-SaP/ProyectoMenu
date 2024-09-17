# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Category(models.Model):
    id_category = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    svg_path = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Menu(models.Model):
    id_menu = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    creation_date = models.DateField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    id_org = models.ForeignKey('Organization', models.DO_NOTHING, db_column='id_org')

    class Meta:
        managed = False
        db_table = 'menu'


class MenuProduct(models.Model):
    id_menu = models.OneToOneField(Menu, models.DO_NOTHING, db_column='id_menu', primary_key=True)  # The composite primary key (id_menu, id_product) found, that is not supported. The first column is selected.
    id_product = models.ForeignKey('Product', models.DO_NOTHING, db_column='id_product')

    class Meta:
        managed = False
        db_table = 'menu_product'
        unique_together = (('id_menu', 'id_product'),)


class OrgConfigs(models.Model):
    id_org_configs = models.AutoField(primary_key=True)
    id_org = models.ForeignKey('Organization', models.DO_NOTHING, db_column='id_org')
    nombre_tienda = models.CharField(max_length=255, blank=True, null=True)
    contenido_inicial = models.IntegerField(blank=True, null=True)
    logo_url = models.CharField(max_length=255, blank=True, null=True)
    descripcion_logo = models.CharField(max_length=255, blank=True, null=True)
    texto_superior = models.CharField(max_length=255, blank=True, null=True)
    horario_atencion = models.CharField(max_length=255, blank=True, null=True)
    telefono_contacto = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'org_configs'


class Organization(models.Model):
    id_org = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    status = models.IntegerField()
    attendant = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'organization'


class Product(models.Model):
    id_product = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.IntegerField(blank=True, null=True)
    image_link_alt = models.CharField(max_length=255, blank=True, null=True)
    image_link = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product'


class ProductCategory(models.Model):
    id_category = models.OneToOneField(Category, models.DO_NOTHING, db_column='id_category', primary_key=True)  # The composite primary key (id_category, id_product) found, that is not supported. The first column is selected.
    id_product = models.ForeignKey(Product, models.DO_NOTHING, db_column='id_product')

    class Meta:
        managed = False
        db_table = 'product_category'
        unique_together = (('id_category', 'id_product'),)
