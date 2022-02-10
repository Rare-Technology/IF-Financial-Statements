# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_user'


class FishdataBuyer(models.Model):
    installation = models.ForeignKey('FishdataInstallation', models.DO_NOTHING)
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)
    gender = models.IntegerField()
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fishdata_buyer'


class FishdataBuyingunit(models.Model):
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    label = models.CharField(max_length=20)
    notes = models.TextField()
    collect_weight = models.BooleanField()
    weight_units = models.CharField(max_length=10)
    weight_si = models.FloatField(blank=True, null=True)
    collect_count = models.BooleanField()
    collect_volume = models.BooleanField()
    volume_units = models.CharField(max_length=10)
    volume_si = models.FloatField(blank=True, null=True)
    collect_category = models.BooleanField()
    buyer = models.ForeignKey(FishdataBuyer, models.DO_NOTHING, blank=True, null=True)
    range = models.ForeignKey('FishdataRange', models.DO_NOTHING, blank=True, null=True)
    order = models.IntegerField()
    fishbase_type = models.ForeignKey('FishdataFishbasespeciestype', models.DO_NOTHING, blank=True, null=True)
    gear_type = models.ForeignKey('FishdataGeartype', models.DO_NOTHING, blank=True, null=True)
    count_max = models.FloatField(blank=True, null=True)
    count_min = models.FloatField(blank=True, null=True)
    price_max = models.FloatField(blank=True, null=True)
    price_min = models.FloatField(blank=True, null=True)
    weight_max = models.FloatField(blank=True, null=True)
    weight_min = models.FloatField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fishdata_buyingunit'


class FishdataCatch(models.Model):
    id = models.UUIDField(primary_key=True)
    date = models.DateTimeField()
    data = models.TextField()
    buyer = models.ForeignKey(FishdataBuyer, models.DO_NOTHING)
    buying_unit = models.ForeignKey(FishdataBuyingunit, models.DO_NOTHING)
    fisher = models.ForeignKey('FishdataFisher', models.DO_NOTHING, blank=True, null=True)
    id_fishing_gear = models.ForeignKey('FishdataGeartype', models.DO_NOTHING, blank=True, null=True)
    customsupplyquantity = models.FloatField(db_column='customSupplyQuantity', blank=True, null=True)  # Field name made lowercase.
    id_custom_supply = models.ForeignKey('FishdataCustomsupplies', models.DO_NOTHING, blank=True, null=True)
    id_fish_inventory = models.ForeignKey('FishdataFishinventory', models.DO_NOTHING, blank=True, null=True)
    caneditordelete = models.BooleanField(db_column='canEditOrDelete')  # Field name made lowercase.
    iscommercial = models.BooleanField(db_column='isCommercial')  # Field name made lowercase.
    wrong_fisher = models.CharField(max_length=256, blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fishdata_catch'


class FishdataCommunity(models.Model):
    region_code = models.CharField(max_length=50)
    installation = models.ForeignKey('FishdataInstallation', models.DO_NOTHING, blank=True, null=True)
    country = models.ForeignKey('FishdataCountry', models.DO_NOTHING)
    level4_id = models.CharField(max_length=256, blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fishdata_community'
        unique_together = (('installation', 'region_code'),)


class FishdataCountry(models.Model):
    id = models.CharField(primary_key=True, max_length=3)
    name = models.CharField(max_length=100)
    active = models.BooleanField()
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fishdata_country'


class FishdataCustomsupplies(models.Model):
    id_custom_supply = models.UUIDField(primary_key=True)
    custom_suply_name = models.CharField(max_length=100)
    measure_unit = models.CharField(max_length=100)
    buyer = models.ForeignKey(FishdataBuyer, models.DO_NOTHING, blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fishdata_customsupplies'


class FishdataExpense(models.Model):
    id = models.UUIDField(primary_key=True)
    expense_type = models.IntegerField()
    buyer = models.ForeignKey(FishdataBuyer, models.DO_NOTHING, blank=True, null=True)
    fisher = models.ForeignKey('FishdataFisher', models.DO_NOTHING, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    quantity = models.FloatField(blank=True, null=True)
    total_price = models.IntegerField()
    date = models.DateTimeField()
    price_exponent = models.IntegerField()
    name = models.CharField(max_length=100, blank=True, null=True)
    id_custom_supply = models.ForeignKey(FishdataCustomsupplies, models.DO_NOTHING, blank=True, null=True)
    isdonation = models.BooleanField(db_column='isDonation', blank=True, null=True)  # Field name made lowercase.
    ispayment = models.BooleanField(db_column='isPayment', blank=True, null=True)  # Field name made lowercase.
    isrecordaftertp = models.BooleanField(db_column='isRecordAfterTP', blank=True, null=True)  # Field name made lowercase.
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fishdata_expense'


class FishdataFishbasespeciestype(models.Model):
    fishbase_id = models.IntegerField()
    country = models.ForeignKey(FishdataCountry, models.DO_NOTHING)
    species = models.CharField(max_length=255)
    details_url = models.CharField(max_length=200)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fishdata_fishbasespeciestype'


class FishdataFisher(models.Model):
    fisher_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=100)
    last_modified_date = models.DateTimeField()
    community = models.ForeignKey(FishdataCommunity, models.DO_NOTHING)
    phone = models.CharField(max_length=255, blank=True, null=True)
    whatsapp = models.BooleanField(blank=True, null=True)
    expired = models.BooleanField(blank=True, null=True)
    level4_id = models.CharField(max_length=255, blank=True, null=True)
    municipality = models.CharField(max_length=255, blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fishdata_fisher'
        unique_together = (('fisher_id', 'community'),)


class FishdataFishersatisfactionrating(models.Model):
    id = models.UUIDField(primary_key=True)
    value = models.IntegerField()
    date = models.DateTimeField()
    buyer = models.ForeignKey(FishdataBuyer, models.DO_NOTHING)
    fisher = models.ForeignKey(FishdataFisher, models.DO_NOTHING)
    fishers_number = models.IntegerField()
    numberofhours = models.IntegerField(db_column='numberOfHours', blank=True, null=True)  # Field name made lowercase.
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fishdata_fishersatisfactionrating'


class FishdataFishinventory(models.Model):
    id_fish_inventory = models.UUIDField(primary_key=True)
    delivery_date = models.DateTimeField()
    total_paid_amount = models.IntegerField(blank=True, null=True)
    purchased_weight = models.FloatField(blank=True, null=True)
    purchased_quantity = models.FloatField(blank=True, null=True)
    purchased_volume = models.FloatField(blank=True, null=True)
    id_range_value = models.ForeignKey('FishdataRangevalue', models.DO_NOTHING, blank=True, null=True)
    total_received_amount = models.IntegerField(blank=True, null=True)
    weight_in_stock = models.FloatField(blank=True, null=True)
    quantity_in_stock = models.FloatField(blank=True, null=True)
    volume_in_stock = models.FloatField(blank=True, null=True)
    id_fish = models.ForeignKey(FishdataBuyingunit, models.DO_NOTHING)
    id_range = models.ForeignKey('FishdataRange', models.DO_NOTHING, blank=True, null=True)
    buyer = models.ForeignKey(FishdataBuyer, models.DO_NOTHING, blank=True, null=True)
    price_exponent = models.IntegerField()
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fishdata_fishinventory'


class FishdataFishsales(models.Model):
    id_sale = models.UUIDField(primary_key=True)
    weight = models.FloatField(blank=True, null=True)
    quantity = models.FloatField(blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)
    price_exponent = models.IntegerField()
    isunsold = models.BooleanField(db_column='isUnsold')  # Field name made lowercase.
    note = models.TextField()
    id_fish_inventory = models.ForeignKey(FishdataFishinventory, models.DO_NOTHING)
    date = models.DateTimeField()
    total_price = models.IntegerField(blank=True, null=True)
    unit_price = models.IntegerField(blank=True, null=True)
    buyer = models.ForeignKey(FishdataBuyer, models.DO_NOTHING, blank=True, null=True)
    unsoldreason = models.IntegerField(db_column='unsoldReason', blank=True, null=True)  # Field name made lowercase.
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fishdata_fishsales'


class FishdataGeartype(models.Model):
    label = models.CharField(max_length=128)
    country = models.ForeignKey(FishdataCountry, models.DO_NOTHING)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fishdata_geartype'


class FishdataImportoperationlog(models.Model):
    started_date = models.DateTimeField()
    import_from_date = models.DateTimeField()
    finished_date = models.DateTimeField(blank=True, null=True)
    op_type = models.CharField(max_length=1)
    pages = models.IntegerField()
    total_pages = models.IntegerField()
    processed = models.IntegerField()
    total = models.IntegerField()
    errors = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'fishdata_importoperationlog'


class FishdataInstallation(models.Model):
    name = models.CharField(max_length=50)
    country = models.ForeignKey(FishdataCountry, models.DO_NOTHING)
    language = models.ForeignKey('FishdataLanguage', models.DO_NOTHING)
    price_exponent = models.IntegerField()
    price_currency = models.CharField(max_length=3)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fishdata_installation'


class FishdataLanguage(models.Model):
    id = models.CharField(primary_key=True, max_length=3)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'fishdata_language'


class FishdataRange(models.Model):
    name = models.CharField(max_length=100)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fishdata_range'


class FishdataRangevalue(models.Model):
    label = models.CharField(max_length=20)
    notes = models.TextField()
    range = models.ForeignKey(FishdataRange, models.DO_NOTHING)
    order = models.IntegerField()
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fishdata_rangevalue'


class FishdataSelltransaction(models.Model):
    id = models.UUIDField(primary_key=True)
    date = models.DateTimeField()
    total_price = models.IntegerField()
    price_exponent = models.IntegerField()
    weight = models.FloatField(blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)
    buyer = models.ForeignKey(FishdataBuyer, models.DO_NOTHING)
    catch = models.ForeignKey(FishdataCatch, models.DO_NOTHING)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fishdata_selltransaction'


class FishdataSupplyinventory(models.Model):
    id_supplyinventory = models.UUIDField(db_column='id_supplyInventory', primary_key=True)  # Field name made lowercase.
    type_of_supply = models.IntegerField()
    total_paid_amount = models.FloatField(blank=True, null=True)
    id_custom_supply = models.ForeignKey(FishdataCustomsupplies, models.DO_NOTHING, blank=True, null=True)
    buyer = models.ForeignKey(FishdataBuyer, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fishdata_supplyinventory'


class FishdataSupplypurchases(models.Model):
    id_purchase = models.UUIDField(primary_key=True)
    purchase_date = models.DateTimeField()
    type_of_supply = models.IntegerField()
    total_paid_amount = models.IntegerField()
    price_exponent = models.IntegerField()
    id_custom_supply = models.ForeignKey(FishdataCustomsupplies, models.DO_NOTHING, blank=True, null=True)
    buyer = models.ForeignKey(FishdataBuyer, models.DO_NOTHING, blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fishdata_supplypurchases'
