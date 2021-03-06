from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import DateTimeField
from django.forms import ModelForm
from django import forms

import django_tables2 as tables

# Create your models here.
class User(AbstractUser):
    pass

class ICparams(models.Model):
    url = models.CharField(max_length=64, help_text = "Назва хосту. Напр.: http://localhost")
    port_IC = models.CharField(max_length=8, blank=True, 
                help_text="Номер порту (:80 або :443)")
    base_IC_name = models.CharField(max_length=64, help_text="Назва бази 1С. Напр.: /base ")
    odata_url = models.CharField(max_length=64, help_text="/odata/standard.odata")
    
    sessionIC_login = models.CharField(max_length=64, help_text="Логін доступу в 1С. Напр.: Админ")
    sessionIC_password = models.CharField(max_length=64, help_text="Пароль доступу в 1С")

    def __str__(self):
        #http://localhost:80/base/odata/standard.odata/
        return f"{self.url}{self.port_IC}{self.base_IC_name}{self.odata_url}"


class ICparamsForm(ModelForm):
    class Meta:
        model = ICparams
        fields = ('url', 'port_IC', 'base_IC_name', 'odata_url', 'sessionIC_login', 'sessionIC_password')


class ICgroups(models.Model):
    group_name = models.CharField(max_length=70, blank=True) #Description
    group_code = models.CharField(max_length=9) # code 
    group_guid = models.CharField(max_length=36, unique=True) # guid code 
    parent_guid_str = models.CharField(max_length=36, default='str') # parentguid code
    parent_guid = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name="children") # guid parent code
    is_folder = models.BooleanField()
    in_stock = models.BooleanField(default=False) # field to show that group is under main group Товары
    
    # https://stackoverflow.com/questions/4725343/django-self-recursive-foreignkey-filter-query-for-all-childs
    def get_all_children(self, include_self=True):
        r = []
        if include_self:
            r.append({'name': self.group_name, 'object': self})
        for c in ICgroups.objects.filter(parent_guid=self):
            _r = c.get_all_children(include_self=True)
            if 0 < len(_r):
                r.extend(_r)
        return r

class Producers(models.Model):
    producer_guid = models.CharField(max_length=36, unique=True) # guid code from 1C
    producer_name = models.CharField(max_length=100, blank=True) # Description from 1C
    short_prod_name = models.CharField(max_length=100, blank=True) # Custom name from user 
    contact_data = models.CharField(max_length=200, blank=True) # name, telephone etc
    email_order = models.EmailField(blank=True)
    info_field = models.TextField(max_length=300, blank=True)
    active = models.BooleanField(default=False) # значить постачальник в даний час співпрацює з магазином. 
    min_sum = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=None) # мін сумма замовлення
    file_name = models.CharField(max_length=100, blank=True, null=True, default=None) # назва файлу для заповнення замовлення 
    barcode_col = models.CharField(max_length=2, blank=True) # колонка із штрихкодами 
    order_col = models.CharField(max_length=2, blank=True) # колонка із куди записувати замовлення

#for showing table in django 
class ProducersForJSgrid(tables.Table):
    name = tables.Column()
    short_name = tables.Column()
    contact_data = tables.Column()
    email = tables.Column()
    info = tables.Column()

    class Meta:
        attrs = {"class": "produsers"}

class IC_scu(models.Model):
    scu_name = models.CharField(max_length=70, blank=True) #Description
    scu_code = models.CharField(max_length=9) 
    scu_guid = models.CharField(max_length=36, unique=True) # guid code 
    scu_parent_guid = models.ForeignKey(ICgroups, on_delete=models.CASCADE, related_name="scu_parentgroup_guid")
    unit_measure = models.CharField(max_length=2, blank=True)
    scu_article = models.CharField(max_length=5)
    scu_barcode = models.CharField(max_length=13, blank=True, null=True)
    ret_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    who_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    scu_produser = models.ForeignKey(Producers, on_delete=models.CASCADE, related_name="scu_produser_rel_name", blank=True, null=True)


class Prices(models.Model): # class for storing prices of prices
    scu = models.ForeignKey(IC_scu, on_delete=models.CASCADE, related_name="scu_prices")
    ret_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    who_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

class Prices_type(models.Model):
    price_name = models.CharField(max_length=15) # Desription 
    price_code = models.CharField(max_length=36, unique=True) # guid code 

# class for showing table in django 
class SimpleTable(tables.Table):
    class Meta:
        model = IC_scu
        fields = ("scu_article", "scu_name", "who_price", "ret_price")

#  Class to show price list (doesnt get data from db)
class PriceListTable(tables.Table):
        name = tables.Column()
        articul = tables.Column(attrs={'td': {'class': lambda value: 'is_group' if value == '—' else '' }})
        barcode = tables.Column()
        wh_price = tables.Column()
        rt_price = tables.Column()
        abc = tables.Column()

        class Meta:
            attrs = {"class": "pricelist"}
        


class SalesForAbc(models.Model):
    scu = models.ForeignKey(IC_scu, on_delete=models.CASCADE, related_name="scu_guid_data")
    quantity = models.DecimalField(null=True, max_digits=10, decimal_places=2) # sales in some period of tume
    cost = models.DecimalField(null=True, max_digits=10, decimal_places=2) # sum of sales 
    abc_result = models.CharField(max_length=3) # result of ABC analysis A, B, C, CC, CCC
    start_salesData = models.DateField(blank=True)
    end_salesData = models.DateField(blank=True)

# form for dates in getting sales for abc analisys
class SalesForAbcForm(ModelForm):
    class Meta:
        model = SalesForAbc
        fields = ['start_salesData', 'end_salesData']
        widgets = {'start_salesData': forms.DateInput(format=('%Y-%m-%d'), 
                                                    attrs={'class':'form-control', 'placeholder':'Choose start date', 'type':'date'}),
                   'end_salesData': forms.DateInput(format=('%Y-%m-%d'), 
                                                    attrs={'class':'form-control', 'placeholder':'Choose end date', 'type':'date'}), 
                    }
        labels = {'start_salesData': 'Start', 'end_salesData': 'End'}

# клас для відображення стахових запасів товару 
class SafetyStock(models.Model):
    scu = models.ForeignKey(IC_scu, on_delete=models.CASCADE, related_name="scu_safety_stock") # товар 
    provider = models.ForeignKey(Producers, on_delete=models.CASCADE, related_name="produser_safety_stock", blank=True)# постачальник товару
    safe_stock = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2) # страховий запаси
    multipl = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2) # кратність
    only_max = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2) # максимальне замовлення
    stock_max = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2) # максимальний залишок 

class DataForProgressbar(models.Model): # class to save info about data legth before loading for a progressbar
    name = models.CharField(max_length=15) # Desription 
    count = models.PositiveSmallIntegerField(null=True) 

class EventsDateTime(models.Model):
    description = models.CharField(max_length=30)
    datetime_data = DateTimeField()

class FoldersForFiles(models.Model): # model to save path to clean files from produsers and ready files with orders
    clean_files = models.CharField(max_length=100)
    ready_files = models.CharField(max_length=100)