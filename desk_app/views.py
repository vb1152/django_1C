from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, QueryDict
from django.urls import reverse

# all my imports
import requests
import django_tables2 as tables

import time
import datetime
from datetime import timedelta

from .models import User, ICparams, ICparamsForm, ICgroups, IC_scu, SimpleTable, Prices_type, PriceListTable, Producers, ProducersForJSgrid 
from .models import SalesForAbc, SalesForAbcForm, SafetyStock


from collections import defaultdict 
from django.core import serializers
from django.contrib import messages
from django.db.models import Sum, F
from django.core.exceptions import ObjectDoesNotExist

from .logic import *

# Create your views here.
#@login_required
def index(request):
    '''Функція головної сторінки. На головній сторінці відображаються всі кнопки управління.
        
    ''' 

    #TODO Побудувати модель за прикладом фласк апп. колонки ід, назва групи, код групи, guid групи, guid батьк групи 
    # читання зверху вниз. 

    #Логіка index view
    #При першому заповненні бази даних. 

    #Почати завантаження тільки по кнопці, щоб кожного разу при загрузці index база не починала оновлюватися знову.  
    #Якщо чиста база, 
    #Пошук із параметром isgroup true  і запис в базу інфо нульової групи «товари». 

    #Далі пошук через запити із parent key дочірніх груп нульової групи, запис інфо в базу. 
    #далі пошук їх дочірніх елементів, і т.д. 


    #Далі запит тільки номенклатури, без папок. 
    #По кожній номенклатурі: якщо в базі груп наявна група, яка є батьківським елементом цієї номенклатури, запис цієї номенклатури в базу. 

    #Після формування списку номенклатури, в залежності від можливостей, якщо є можливість завантажити всі ціни діючого прайсу, тоді ціни додати до існуючої номенклатури, роблячи менше запитів через odata, а більше працюючи вже із наявними даними. Якщо запиту на ціни немає, тоді робити окремі запити ціни на кожен товар. 

    #Стан завантаження: інформаційні повідомлення -  спробувати показувати через django message. 

    return render(request, 'desk_app/index.html')

@login_required
def IC(request):

    if request.method == 'POST':
        # udate existing data about IC connection in db 
        if ICparams.objects.first():
            instace_param = ICparams.objects.first()
            form = ICparamsForm(request.POST, instance=instace_param)

            if form.is_valid():

                url = form.cleaned_data['url']
                port_IC = form.cleaned_data['port_IC']
                base_IC_name = form.cleaned_data['base_IC_name']
                odata_url = form.cleaned_data['odata_url']
                sessionIC_login = form.cleaned_data['sessionIC_login'].encode('UTF-8')
                sessionIC_password = form.cleaned_data['sessionIC_password']
                form.save()

                return HttpResponseRedirect(reverse("desk_app:IC"), )
            else: 
                return HttpResponse("Якась помилка. Спробуйте знову.")        
        # if not data about IC connection in db  
        else: 
            form = ICparamsForm(request.POST)

            if form.is_valid():
                instance = form.save(commit=False)
                url = form.cleaned_data['url']
                port_IC = form.cleaned_data['port_IC']
                base_IC_name = form.cleaned_data['base_IC_name']
                odata_url = form.cleaned_data['odata_url']
                sessionIC_login = form.cleaned_data['sessionIC_login'].encode('UTF-8')
                sessionIC_password = form.cleaned_data['sessionIC_password']
                instance.save()
                
                return HttpResponseRedirect(reverse("desk_app:IC"), )
            else:
                return HttpResponse("Якась помилка. Спробуйте знову.")


    form_IC = ICparamsForm()

    print(ICparams.objects.first())
    
    return render(request, 'desk_app/IC.html', {
        "message": "Користувач не авторизований",
        "form_IC": form_IC.as_p,
    })
    # TODO 
    # заповнювати форму із діючими показниками підключення (які вже збережені в базі). 
    # Використати https://django.fun/tutorials/django-i-formy-bootstrap-4/ 



# function creates new catalog Товари in db
@login_required
def load_data_from_IC(request):
    # TODO 23.06.2021 
    # Ще раз перевірити процедуру запису груп товарів в базу. У нас за запитом odata 
    # http://localhost/base/odata/standard.odata/Catalog_Номенклатура?$format=json&$filter=IsFolder%20eq%20true&$select=Ref_Key,Parent_Key,Code,Description,Артикул
    # видається список із 700 груп. При тому, що діючих груп - 620. 
    # Можна просто записати всі групи по черзі в базу, а видавати на показ - тільки дерево груп в групи товари. 
    # Додатково: 
    # процедуру завантаження можна оформити таким чином. 
    #  - запис всіх груп в базу 
    #  - потім присвоєння батьківських груп (яка група якій підпорядковується)
    #  - видалення груп, які знаходяться поза деревом груп Товари.  
    # Працювати на кінцевий результат, без technical debt. 


    print("loading data з 1с ")

    # dev stage. Якщо товарні групи завантажені в базу, інше завантаження не відбувається. 
    all_groups_count = ICgroups.objects.all().count()
    if all_groups_count > 0: 
        return JsonResponse({"comment": f'На даний час в базі записано {all_groups_count} груп. Заповнення не вимагається.'},
                             status=200)
    else: 


        #connecting to IC 
        #url = ICparams.objects.first()
        url = ICparams.objects.filter()[:1].get()
        print(url)
        session = requests.Session()
        session.auth = (url.sessionIC_login.encode('UTF-8'), url.sessionIC_password)
        response = session.get(url)

        # if connection to IC is successful 
        if response.status_code == 200:

            # working with db and loading data
            # get only folders from IC 
            groups_all = get_data_from_IS("/Catalog_Номенклатура?$format=json&$filter=IsFolder eq true&$select=Description,Ref_Key,Parent_Key,IsFolder,Code")

            # очистити всю базу даних перед записом. 
            ICgroups.objects.all().delete()
            
            # if goods_folder doesnt exist in db, create it
            guid_Tovaru = 'ab2bf0a5-7426-11e1-b2e4-0013d43ff493'
            try:
                goods_folder = ICgroups.objects.get(group_guid=guid_Tovaru)
            except ICgroups.DoesNotExist:
                # find in Catalog_Номенклатура data about Товары folder and save it to db  
                for i in groups_all:
                    if i['Ref_Key'] == guid_Tovaru and i['IsFolder'] == True:
                        description = i['Description']
                        code_9dig = i['Code']
                        guid_group = i['Ref_Key']
                        guid_parent = i['Parent_Key']
                        is_folder_data = i['IsFolder']
                        print("група: ", description, code_9dig, guid_group, guid_parent, is_folder_data)
                        group = ICgroups(group_name=description, group_code=code_9dig, group_guid=guid_group, 
                                        is_folder=is_folder_data)
                        group.save()
            
            # get data about Товары folder from db 
            goods_folder = ICgroups.objects.get(group_guid=guid_Tovaru)
            # get children of Товары folder from IC 
            groups1 = get_data_from_IS("/Catalog_Номенклатура?$format=json&$filter=Parent_Key eq guid'" + goods_folder.group_guid + "' and IsFolder eq true")

            # save data about children groups of Товары folder in db 
            for i in groups1:
                if i['Parent_Key'] == guid_Tovaru and i['IsFolder'] == True:
                    description = i['Description']
                    code_9dig = i['Code']
                    guid_group = i['Ref_Key']
                    guid_parent = ICgroups.objects.get(group_guid=i['Parent_Key'])
                    is_folder_data = i['IsFolder']

                    group = ICgroups(group_name=description, 
                                        group_code=code_9dig, 
                                        group_guid=guid_group, 
                                        parent_guid=guid_parent,
                                        is_folder=is_folder_data)
                    group.save()

            # get data from db about groups of 1 order 
            groups1_from_db = list(ICgroups.objects.filter(parent_guid=goods_folder.id).values_list('group_guid', flat=True))
            
            groups2_list_guid = [] # create new list to save guids from groups 2 level to use it in next for loop 
            # for every group in all list of groups 
            # if group.parent guid is in 
            for groups2 in groups_all:
                if groups2['Parent_Key'] in groups1_from_db:
                    #print('if', groups2['Description'])
                    description = groups2['Description']
                    code_9dig = groups2['Code']
                    guid_group = groups2['Ref_Key']
                    guid_parent = ICgroups.objects.get(group_guid=groups2['Parent_Key'])
                    is_folder_data = groups2['IsFolder']

                    groups2_list_guid.append(guid_group)

                    group = ICgroups(group_name=description, 
                                        group_code=code_9dig, 
                                        group_guid=guid_group, 
                                        parent_guid=guid_parent,
                                        is_folder=is_folder_data)
                    group.save()
                    
            groups3_list_guid = []
            for groups3 in groups_all:
                if groups3['Parent_Key'] in groups2_list_guid:
                    #print('if2', groups3['Description'])
                    description = groups3['Description']
                    code_9dig = groups3['Code']
                    guid_group = groups3['Ref_Key']
                    guid_parent = ICgroups.objects.get(group_guid=groups3['Parent_Key'])
                    is_folder_data = groups3['IsFolder']

                    groups3_list_guid.append(guid_group)

                    group = ICgroups(group_name=description, 
                                        group_code=code_9dig, 
                                        group_guid=guid_group, 
                                        parent_guid=guid_parent,
                                        is_folder=is_folder_data)
                    group.save()

            groups4_list_guid = []
            for groups4 in groups_all:
                if groups4['Parent_Key'] in groups3_list_guid:
                    #print('if3', groups4['Description'])
                    description = groups4['Description']
                    code_9dig = groups4['Code']
                    guid_group = groups4['Ref_Key']
                    guid_parent = ICgroups.objects.get(group_guid=groups4['Parent_Key'])
                    is_folder_data = groups4['IsFolder']

                    groups4_list_guid.append(guid_group)

                    group = ICgroups(group_name=description, 
                                        group_code=code_9dig, 
                                        group_guid=guid_group, 
                                        parent_guid=guid_parent,
                                        is_folder=is_folder_data)
                    group.save()

            print(len(groups4_list_guid))
            
            # find groups 5 
            groups5_list_guid = []
            for groups5 in groups_all:
                if groups5['Parent_Key'] in groups4_list_guid:
                    #print('if4', groups5['Description'])
                    description = groups5['Description']
                    code_9dig = groups5['Code']
                    guid_group = groups5['Ref_Key']
                    guid_parent = ICgroups.objects.get(group_guid=groups5['Parent_Key'])
                    is_folder_data = groups5['IsFolder']

                    groups5_list_guid.append(guid_group)

                    group = ICgroups(group_name=description, 
                                        group_code=code_9dig, 
                                        group_guid=guid_group, 
                                        parent_guid=guid_parent,
                                        is_folder=is_folder_data)
                    group.save()

            print(len(groups5_list_guid))        
    #                groups2 = get_data_from_IS("&$filter=Parent_Key eq guid'" + i['Ref_Key'] + "' and IsFolder eq true")

    #                for b in groups2:
    #                    print(b['Description'])
    #                    if b['Parent_Key'] == i['Ref_Key'] and b['IsFolder'] == True:
    #                        description = b['Description']
    #                        code_9dig = b['Code']
    #                        guid_group = b['Ref_Key']
    #                        guid_parent = ICgroups.objects.get(group_guid=b['Parent_Key'])
    #                        is_folder_data = b['IsFolder']

    #                        group = ICgroups(group_name=description, 
    #                                            group_code=code_9dig, 
    #                                            group_guid=guid_group, 
    #                                            parent_guid=guid_parent,
    #                                            is_folder=is_folder_data)
    #                        group.save()
                        
    #                        groups3 = get_data_from_IS("&$filter=Parent_Key eq guid'" + b['Ref_Key'] + "' and IsFolder eq true")

    #                        for c in groups3:
    #                            print(c['Description'])
    #                            if c['Parent_Key'] == b['Ref_Key'] and c['IsFolder'] == True:
    #                                description = c['Description']
    #                                code_9dig = c['Code']
    #                                guid_group = c['Ref_Key']
    #                                guid_parent = ICgroups.objects.get(group_guid=c['Parent_Key'])
    #                                is_folder_data = c['IsFolder']

    #                                group = ICgroups(group_name=description, 
    #                                                    group_code=code_9dig, 
    #                                                    group_guid=guid_group, 
    #                                                    parent_guid=guid_parent,
    #                                                    is_folder=is_folder_data)
    #                                group.save()

    #                                groups4 = get_data_from_IS("&$filter=Parent_Key eq guid'" + c['Ref_Key'] + "' and IsFolder eq true")

    #                                for d in groups4:
    #                                    print(d['Description'])
    #                                    if d['Parent_Key'] == c['Ref_Key'] and d['IsFolder'] == True:
    #                                        description = d['Description']
    #                                        code_9dig = d['Code']
    #                                        guid_group = d['Ref_Key']
    #                                        guid_parent = ICgroups.objects.get(group_guid=d['Parent_Key'])
    #                                        is_folder_data = d['IsFolder']

    #                                        group = ICgroups(group_name=description, 
    #                                                            group_code=code_9dig, 
    #                                                            group_guid=guid_group, 
    #                                                            parent_guid=guid_parent,
    #                                                            is_folder=is_folder_data)
    #                                        group.save()

            # висновки. Дуже довге завантаження через постійні деталізовані запити одата. 
            # спробувати просто працювати із списком повних груп - можливо так буде швидщше. 

            all_groups_count = ICgroups.objects.all().count()
                    
            #&$filter=Parent_Key eq guid'ab2bf0a5-7426-11e1-b2e4-0013d43ff493' and IsFolder eq true
            # TODO отримали 27 дочірніх папок по запросу, їх зберегти, отримати їх дочірні елементи. 
                   
            return JsonResponse({"comment": f'Назви, коди та структуру групи Товари оновлено! В базі {all_groups_count} груп'},
                                status=200)
        else:
            return JsonResponse({"comment": 'Щось пішло не так. '}, status=404)

    #return JsonResponse([email.serialize() for email in emails], safe=False)
    #return HttpResponse("message OK", status=200)


@login_required
def load_scu_from_IC(request):
    '''Функція запису номенклатури в базу даних''' 
    
    scu_count = IC_scu.objects.all().count()

    if scu_count > 0:
        return JsonResponse({"comment": f'В базі вже записано {scu_count} товарів. Повторне завантаження не вимагається. '},
                                    status=200)
    else:
        #get all scu from IC 
        scu_all = get_data_from_IS("/Catalog_Номенклатура?$format=json&$filter=IsFolder eq false&$select=Ref_Key,Parent_Key,Code,Description,Артикул")
        print(len(scu_all))

        # get all groups ref_keys from db, as list
        groups_refs = list(ICgroups.objects.all().values_list('group_guid', flat=True))
        
        for scu in scu_all:
            if scu['Parent_Key'] in groups_refs:
                scu_name = scu['Description']
                print(scu_name)
                scu_code = scu['Code']
                scu_guid = scu['Ref_Key']
                scu_parent_guid = ICgroups.objects.get(group_guid=scu['Parent_Key'])
                scu_article = scu['Артикул']

                scu_item = IC_scu(scu_name=scu_name, scu_code=scu_code, scu_guid=scu_guid, 
                                    scu_parent_guid=scu_parent_guid, scu_article=scu_article)
                scu_item.save()                    
        
        

        scu_count = IC_scu.objects.all().count()

        return JsonResponse({"comment": f'В базі записано {scu_count} товарів'},
                                        status=200)
#@login_required
#def show_pricelist(request):
#    print("show_pricelist")
#    pass

def simple_list(request):
    print("siple list")
    queryset = IC_scu.objects.all()
    # print(len(queryset))
    table = SimpleTable(queryset)
    return render(request, 'desk_app/ic_scu_list.html', {'table': table})

def price_list_all(request):

    # TODO 
    # http://js-grid.com/getting-started/ працює із list of dicts with values 
    # переробити всю логіку функції, щоб на виході був список вигляду 
    #[
    #    { "Name": "Otto Clay", "Age": 25, "Country": 1, "Address": "Ap #897-1459 Quam Avenue", "Married": false },
    #    { "Name": "Connor Johnston", "Age": 45, "Country": 2, "Address": "Ap #370-4647 Dis Av.", "Married": true },
    #    { "Name": "Lacey Hess", "Age": 29, "Country": 3, "Address": "Ap #365-8835 Integer St.", "Married": false },
    #    { "Name": "Timothy Henson", "Age": 56, "Country": 1, "Address": "911-5143 Luctus Ave", "Married": true },
    #    { "Name": "Ramona Benton", "Age": 32, "Country": 3, "Address": "Ap #614-689 Vehicula Street", "Married": false }
    #];


    # get Товары item id to use it in the future
    tovaru_id = ICgroups.objects.filter(group_name='Товары')
   
    # get all groups form db 
    groups_list =  list(ICgroups.objects.all().values('id', 'group_name', 'parent_guid_id'))#.exclude(group_name='Товары'))
    
    #for index, data in enumerate(groups_list):
    #    if index < 10:
    #        print(data)

    #https://stackoverflow.com/questions/47202838/djangogetting-list-of-values-from-query-set
    # get list of parent_id's from scu 
    scu_parent_id =  IC_scu.objects.all().values_list('scu_parent_guid',  flat=True).distinct()

    
    # https://stackoverflow.com/questions/1247133/recursive-looping-to-n-levels-in-python
    # ідея взята звідси. 
    itemdict = defaultdict(list)
    for item in groups_list:
        itemdict[item['parent_guid_id']].append({item['id']: item['group_name']})

    #print(type(itemdict))
    #print(itemdict)
    # https://stackoverflow.com/questions/1247133/recursive-looping-to-n-levels-in-python

        
    # create list of lists
    data_to_grid = []
    # function to get list of scu by its parent code 
    def get_scu_list(parent_code):
        result = IC_scu.objects.filter(scu_parent_guid=parent_code).values_list('scu_parent_guid', 'scu_name', 'scu_article', 'scu_barcode', 'who_price', 'ret_price', 'scu_guid_data__abc_result')
        
        return result 

    # recursion function to get all children for item from list of dicts
    def printitem(id_item, depth=0):        
        for child in itemdict[id_item]:
            # print(child) -> {3272: 'Группа Бакалея. Хлеб'}
            # [key for key in child.keys()][0] -> Кондитерка. Разное
            
            child_id = [key for key in child.keys()][0]
            name = child[child_id]
                        
            # append data to list  
            data_to_grid.append([child_id, name])
            #data_to_grid.append(child)
            # if group has children scu 
            if child_id in scu_parent_id:
                # get list of child elements from db
                child_scu = get_scu_list(child_id)
                for scu in child_scu:
                    # append scu after group to the list
                    data_to_grid.append(list(scu))
                               
            printitem([key for key in child.keys()][0], depth+1)        
    # 3271 - 
    printitem(tovaru_id[0].id)

    # code just for printing for debugging purpose
    for index, data in enumerate(data_to_grid):
        if index < 10:
            print(data)
    
    # create list with dicts for table html
    data_witk_keys = []
    for item in data_to_grid:
        data_witk_keys.append({#"id_item":item[0], 
                    "name": item[1],
                    "articul": "" if len(item) == 2 else item[2], 
                    "barcode": "" if len(item) == 2 else item[3],
                    "wh_price": "" if len(item) == 2 else item[4],
                    "rt_price": "" if len(item) == 2 else item[5],
                    "abc": "" if len(item) == 2 else item[6]
                     })
        #print('item', item)

    for index, dat in enumerate(data_witk_keys):
        if index < 10:
            print(dat)   
    print(type(data_witk_keys))    
    # повертаємось на головну сторінку 
    #return JsonResponse({"comment": 'ок.'}, status=200)  
    #context={'data_witk_keys': data_witk_keys}
    
    #return render(request, 'desk_app/price_list.html', context)
    #return HttpResponse(data_witk_keys, content_type = "application/json", status = 200)

    # працююча відповідь для заповнення даних js-grid на головній сторінці
    #return JsonResponse(data_witk_keys, safe=False)
    
    # працююча відповідь для заповнення даних js-grid на сторінці Прайс
    table = PriceListTable(data_witk_keys)
    return render(request, "desk_app/price_list.html", {"table": table})
    
# TODO далі працюю над завантаженням даних по продажам і подальший аналіз. 
# https://master1c8.ru/platforma-1s-predpriyatie-8/rukovodstvo-razrabottchika/glava-17-mehanizm-internet-servisov/standartny-interfeys-odata-registr-nakopleniya/
# э можливість завантажувати продажі за період або за кожен окремий день.. 
# Також є можливість завантажувати залишки на конкретний період. 
# Продажі можна використовувати для аналізу (АБС тощо) 
# Залишки для замовленнь. 
# Замовлення можна зберігати в базі для збереження замовлення в 1с та створення 
# замовлення в 1с, а з нього вже - приходних накладних. 


@login_required
def produsers(request):
    ''' Function to work with produsers data: load from 1C, render to user '''
    # показати всю таблицю через джей ес грід всю таблицю з можливістю редагування! 

    if request.method == 'POST':
        # to update data about produsers from IC
        if request.POST.get("update_all_prod_data"):
            guid_list = Producers.objects.all().values_list('producer_guid', flat=True)
            # scu_refs = list(IC_scu.objects.all().values_list('scu_guid', flat=True))

            produsers_all = get_data_from_IS("/Catalog_Контрагенты?$format=json&$filter=IsFolder eq false&$select=Ref_Key,Description")
            
            new_produsers = [] # list of new produsers names
            for produser in produsers_all:
                # if produser is new, save it to db 
                if produser['Ref_Key'] not in guid_list:
                    produser_name = produser['Description']
                    produser_guid = produser['Ref_Key']
                    #print(produser_name)
                    produser_data = Producers(producer_guid=produser_guid, producer_name=produser_name)
                    produser_data.save()

                    new_produsers.append('produser_name') # add data to list of new produsers names
                else:
                    # if produser is not new, update its name in db  
                    Producers.objects.filter(producer_guid=produser['Ref_Key']).update(producer_name=produser['Description'])

            # return HttpResponseRedirect(reverse("desk_app:produsers"))  
            if len(new_produsers) > 0:
                messages.add_message(request, messages.INFO, f'В базу додано {len(new_produsers)} постачальників.',  extra_tags='0')

            return render(request, "desk_app/produsers.html")
        
    # check if some produsers is in db. If not - load data from 1C 
    check = Producers.objects.all().count()
    print(check)
    if check == 0: 
        messages.add_message(request, messages.INFO, 'В базі немає постачальників. Завантажити?',  extra_tags='0')
    else:
        messages.add_message(request, messages.INFO, f'В базі {check} постачальників.',  extra_tags='1')
    
    return render(request, "desk_app/produsers.html")#, {'table': data})


@login_required
def produsers_api(request, **kwargs):
    if request.method == 'GET':# and request.is_ajax():
        print('ajax!! ')
        
        table = Producers.objects.all() \
            .filter(producer_name__contains = request.GET.get('Name_1C')) \
            .filter(short_prod_name__contains = request.GET.get('Short_name')) \
            .filter(contact_data__contains = request.GET.get('Contact')) \
            .filter(info_field__contains = request.GET.get('Info')) \
            .values('id', 'producer_name', 'short_prod_name', 'contact_data', 'email_order', 'info_field')

        return JsonResponse(list(table), safe=False)

    if request.method == 'PUT':
        new_data = QueryDict(request.body) # https://stackoverflow.com/questions/34024650/django-wsgirequest-object-has-no-attribute-put

        produser = Producers.objects.get(id=kwargs['id'])
        produser.short_prod_name = new_data['Short_name']
        produser.contact_data = new_data["Contact"]
        produser.email_order = new_data["Email"]
        produser.info_field = new_data["Info"]
        #client.married = True if request.PUT.get("married") == 'true' else False
        
        produser.save()
        return HttpResponse(status = 200)

    if request.method == 'POST':
        new_produser = Producers(short_prod_name = request.POST.get('Short_name'), 
                                contact_data = request.POST.get('Contact'), 
                                email_order = request.POST.get('Email'), 
                                info_field = request.POST.get('Info'))
        new_produser.save()
        return HttpResponse(status = 200)

    if request.method == 'DELETE':
        del_produser = Producers.objects.get(id=kwargs['id'])
        del_produser.delete()

        return HttpResponse(status = 200)

        #b = Blog(name='Beatles Blog', tagline='All the latest Beatles news.')
        #>>> b.save()

#@login_required
def load_barcode(request):
    # TODO ідея: може не завантажувати в базу данних додатку всю номенклатуру, а тільки те що в ассортименті 

    #get all scu from IC 
    barcode_all = get_data_from_IS("/InformationRegister_Штрихкоды?$format=json&$select=Штрихкод,Владелец")

    print(barcode_all[:3])
    # get all groups ref_keys from db, as list
    scu_refs = list(IC_scu.objects.all().values_list('scu_guid', flat=True))

    # get starting time
    start = time.time()

    counter = 0
    for barcode in barcode_all:
        if barcode['Владелец'] in scu_refs:
            print(barcode['Штрихкод'])
            scu = IC_scu.objects.get(scu_guid = barcode['Владелец'])
            if scu.scu_barcode != barcode['Штрихкод']:
                scu.scu_barcode = barcode['Штрихкод']
                scu.save()
                counter += 1
            
    # get time taken to run the for loop code 
    elapsed_time_fl = (time.time() - start) 
    print(elapsed_time_fl)
    print(counter)

    # повертаємось на головну сторінку 
    return JsonResponse({"comment": f'Оновлено {counter} штрихкодів.'},
                                        status=200)

# TODO завантажити діючі ціни на номенклатуру, на яка вже є в прайсі. 
@login_required
def load_prices(request):
    print('load_prices')
    # Save types of prices to a db (Оптовая, закупочная, Розница... )
    if Prices_type.objects.all().count() == 0:
        prices_types = get_data_from_IS("/Catalog_ТипыЦенНоменклатуры?$format=json")
        
        for price_type in prices_types:
            price_name = price_type['Description']
            price_code = price_type['Ref_Key']
            print(price_name)
            price_type_data = Prices_type(price_name=price_name, price_code=price_code)
            price_type_data.save()                    
    
    
    #get all scu from IC 
    prices_all = get_data_from_IS("/InformationRegister_ЦеныНоменклатуры_RecordType/SliceLast()?$format=json")

    # get all groups ref_keys from db, as list
    groups_refs = list(IC_scu.objects.all().values_list('scu_guid', flat=True))
    
    # get types of prices from db
    price_type = Prices_type.objects.all().values()
    
#    <QuerySet [{'id': 1, 'price_name': 'Закупочная', 'price_code': 'bdfa6d90-e24a-11e3-8378-001e676f0254'}, 
#    {'id': 2, 'price_name': 'Плановая', 'price_code': 'ab2bf0a1-7426-11e1-b2e4-0013d43ff493'}, 
#    {'id': 3, 'price_name': 'Розница', 'price_code': 'ab2bf0a2-7426-11e1-b2e4-0013d43ff493'}, 
#    {'id': 4, 'price_name': 'Оптовая', 'price_code': '7cce3081-3dec-11e2-b3ce-0013d43ff493'}]>

    #print(price_type)
    counter = 0

    # get starting time
    start = time.time()

    for price in prices_all:
        if price['Номенклатура_Key'] in groups_refs:
            
            if price_type.get(price_code=price['ТипЦен_Key'])['price_name'] == 'Оптовая':
                print('оптовая')
                IC_scu.objects.filter(scu_guid = price['Номенклатура_Key']).update(who_price=price['Цена'])
                counter+=1

            elif price_type.get(price_code=price['ТипЦен_Key'])['price_name'] == 'Розница':
                print('Розница')
                IC_scu.objects.filter(scu_guid = price['Номенклатура_Key']).update(ret_price=price['Цена'])        
                counter+=1
        if counter % 100 == 0:
            print(counter)         
    # get time taken to run the for loop code 
    elapsed_time_fl = (time.time() - start) 
    print(elapsed_time_fl)
    
    return JsonResponse({"comment": f'Оновлено {counter} цін.'},
                                        status=200)


@login_required
def IC_connection(request, IC_connection):
    # Filter request based on IC_connection parameter 
    if IC_connection == 'check': 
        # get data from db about 
        if ICparams.objects.first():
            
            url = ICparams.objects.first()
            data = ICparams.objects.filter()[:1].get()
            session = requests.Session()
            session.auth = (data.sessionIC_login.encode('UTF-8'), data.sessionIC_password)
            response = session.get(url)
            #print('get url ', 
            if response.status_code == 200:
                return HttpResponse(status=200)
        else:
            print('Параметри підключення до 1С не знайдені.')
            return HttpResponse('Параметри підключення до 1С не знайдені.', status=404)
    
    # інші параметри для передачі на цей rout - можна в подальшому використати. інакше 
    # використання в urls IC_connection/<str:IC_connection> немає сенсу. 
    #elif IC_connection == 'load_data': 
    #    return 'data loaded'           

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("desk_app:index"))
        else:
            return render(request, "desk_app/login.html", {
                "message": "Невірний логін або пароль!"
            })
    else:
        return render(request, "desk_app/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("desk_app:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "desk_app/register.html", {
                "message": "Паролі мають співпадати."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "desk_app/register.html", {
                "message": "Цей логін вже зайнятий іншим користувачем."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("desk_app:index"))
    else:
        return render(request, "desk_app/register.html")

# старий abc rout, який записує в кожний рядок дату початку - кінця даних для абс аналізу 
# TODO зробити окремий table виключно для таких дат на один рядок данних, для економії пам"яті 
@login_required
def abc(request):
    
    form_dates = SalesForAbcForm()

    # fill form with data from current ABC analysis
    try: 
        form_dates.fields['start_salesData'].initial = SalesForAbc.objects.all().values('start_salesData').first()['start_salesData']
        form_dates.fields['end_salesData'].initial = SalesForAbc.objects.all().values('end_salesData').first()['end_salesData']
    except:
        print("Немає дат в базі даних. Потрібно ввести нові дати. ")

    if request.method == 'POST':
        form = SalesForAbcForm(request.POST)

        if form.is_valid():
            #instance = form.save(commit=False)
            
            start_date = form.cleaned_data['start_salesData']
            end_date = form.cleaned_data['end_salesData']

            print('start_date', start_date.isoformat())
            print('end_date', str(end_date))

            sales_all = get_data_from_IS(f"/AccumulationRegister_Продажи/Turnovers(EndPeriod=datetime'{end_date}T23:59:59',StartPeriod=datetime'{start_date}T00:00:00',Dimensions='Номенклатура')?&$format=json")

            # очистити всю базу даних перед записом. 
            SalesForAbc.objects.all().delete()
            
            for sale in sales_all:
                try:
                    scu = IC_scu.objects.get(scu_guid=sale['Номенклатура_Key'])
                except ObjectDoesNotExist:
                    continue
                sale_row = SalesForAbc(scu=scu, quantity=sale['КоличествоTurnover'],
                                        cost=sale['СтоимостьTurnover'],
                                        start_salesData=start_date, 
                                        end_salesData=end_date)
                sale_row.save()
                            
            # count and save to db ABC classes of every scu 
            data = SalesForAbc.objects.aggregate(Sum('cost'))
            count_ABC = SalesForAbc.objects.all().values('id', 'cost').order_by('-cost')
            a = 0
            for item in count_ABC:
                pers = item['cost']/data['cost__sum'] * 100
                a = a + pers
                if a < 70: 
                    SalesForAbc.objects.filter(id=item['id']).update(abc_result="A")
                elif a >= 70 and a < 90:
                    SalesForAbc.objects.filter(id=item['id']).update(abc_result="B")
                else:
                    SalesForAbc.objects.filter(id=item['id']).update(abc_result="C")

            #return HttpResponse("message OK", status=200)
            # TODO після завантаження даних для абс аналізу видається лише повідомлення. Краще завантажувати всю сторінку. 
            return render(request, 'desk_app/abc.html', {"form_dates": form_dates})

    return render(request, 'desk_app/abc.html', {"form_dates": form_dates})


@login_required
def abc_api(request):
    '''
    Function to response to ajax request from abc.html with ABC analysis
    '''
    if request.method == 'GET' and request.is_ajax():

        table = SalesForAbc.objects.all() \
                .filter(scu__scu_name__contains = request.GET.get('Name')) \
                .filter(abc_result__contains = request.GET.get('Class')) \
                .values(Name=F('scu__scu_name'), Sales=F('quantity'), Sum=F('cost'), Class = F('abc_result')).order_by('-cost')
       
        return JsonResponse(list(table), safe=False)

@login_required
def sheet(request):
    return render(request, 'desk_app/sheet.html')

def sheet_api(request):
    '''
    Функція формування відомості по товарам в роздрібних складах (на прикл. відомості з 1С)
    Дата початку: сьогодні - 7 днів. Продажі за вчора мають бути проведені. 
    Дата кінця: сьогодні - 1 день. 
    '''

    d_start = datetime.date.today() - timedelta(days = 373) # дата формування + 6 днів 
    d_finish = datetime.date.today() - timedelta(days = 367) # дати формування
    
    d_start_abc = d_start - timedelta(days = 120)
    d_finish_abc = d_finish - timedelta(days = 30)
    print(d_start, d_finish)
    print(d_start_abc, d_finish_abc)
    
    # TODO завжди показувати продажі за останні 7 днів. разом із абс классами. Та страховими залишками у майбутньому. 
    sales_all = get_data_from_IS(f"/AccumulationRegister_ТоварыВРознице/BalanceAndTurnovers(EndPeriod=datetime'{d_finish}T23:59:59',StartPeriod=datetime'{d_start}T00:00:00',"
                                    "Dimensions='Номенклатура')?&$select=КоличествоOpeningBalance,"
                                    "КоличествоReceipt,КоличествоExpense,КоличествоClosingBalance,Номенклатура_Key&$format=json")
    #http://localhost/base/odata/standard.odata/AccumulationRegister_ТоварыВРознице/BalanceAndTurnovers(EndPeriod=datetime'2019-02-01T23:59:59',StartPeriod=datetime'2019-01-01T00:00:00',Dimensions='Номенклатура')?&$format=json

    count = 0
    names = 0
    for item in sales_all:
        try: # get name of item from db 
            name = IC_scu.objects.get(scu_guid=item['Номенклатура_Key'])
            item['Назва'] = name.scu_name
        except ObjectDoesNotExist: 
            #name_from_db = get_data_from_IS(f"/Catalog_Номенклатура?$filter=Ref_Key eq guid'{item['Номенклатура_Key']}'&$format=json")
            #item['Назва'] = name_from_db[0]['Description']       
            # if name of scu not in db - get name from IC database by odata отримати назву позиції з бази 1С 
            item['Назва'] = ic_data_scu(item['Номенклатура_Key'])
            names += 1 

        try: # get ABC class from db 
            class_ABC = SalesForAbc.objects.get(scu__scu_guid=item['Номенклатура_Key'])#.values('abc_result')#[0]['abc_result']
            item['class'] = class_ABC.abc_result
        except ObjectDoesNotExist: # if no data about class in db... 
            # check if it is new  
            # якщо на товар немає АБС класу, то це товар який не продавався за період, який аналізувався для АБС класів 
            # в такому разі якщо по цьому товару є залишок більше нуля перевірити його отримання. 
            # Напр. 1 місяць від "сьогоднішньої" дати.  
            # або визначити дату приходу або дату останнього продажу 
            # якщо за останні 1 + 3 місяці (без урахування останніх 30 днів ) продажів не було - це "Новий товар" 

            
            #sale_for1_item = get_data_from_IS(f"/AccumulationRegister_Продажи/Turnovers(EndPeriod=datetime'{d_finish_abc}T23:59:59',StartPeriod=datetime'{d_start_abc}T00:00:00',Dimensions='Номенклатура')?&$format=json&$filter=Номенклатура_Key eq guid'{item['Номенклатура_Key']}'")
            #if len(sale_for1_item) > 0:
            #    print('sale_for1_item', sale_for1_item)
            #    item['class'] = "ССС" 

            # якщо товар "старий" - за останні 1 + 3 місяці (без урахування останіх днів), були продажі - товар категорії ССС.    
            item['class'] = "ССС"
            
            #count += 1
            #item['class'] = "Новий товар"   



    
        #print(item['class'])
        #print(item['Назва'], item['Номенклатура_Key'], item['class'])
        

    print(names)
    print(count)
    print(sales_all[:5])
    return JsonResponse(sales_all, safe=False)

    # продовжити формування табблиці з відомості з роздрібних продажів із назвами позицій та їх АБС классами. 
    # А також в подальшому страховими запасами та можливістю їх коригування. 
    # також не забути про формування групп товарів в цьому дикт і
    #return JsonResponse(list(sales_all), safe=False)

@login_required
def stock_api(request, **kwargs):

    if request.method == 'PUT':
        new_data = QueryDict(request.body) # https://stackoverflow.com/questions/34024650/django-wsgirequest-object-has-no-attribute-put

        #print(kwargs)
        #print('id: ', kwargs['id'])
        #print(new_data)
        if new_data["articul"]: # перевірка, що редагуються дані товару, а не групи 
        
            scu = IC_scu.objects.get(id=kwargs['id'])

            # якщо страховий запас/або інша інфо на товар вже записаний в таблиці 
            if SafetyStock.objects.filter(scu_id=scu.id).exists(): 
                stock = SafetyStock.objects.get(scu_id=scu.id)
                stock.scu = scu
                stock.provider = Producers.objects.get(id=new_data['manuf'])
                stock.safe_stock = new_data['sfs']
                stock.multipl = new_data['mlt']
                stock.only_max = new_data['maxOrd']
                stock.stock_max = new_data['maxSTK']

                stock.save()
            else: 
                stock = SafetyStock()
                stock.scu = scu
                stock.provider = Producers.objects.get(id=new_data['manuf'])
                stock.safe_stock = new_data['sfs']
                stock.multipl = new_data['mlt']
                stock.only_max = new_data['maxOrd']
                stock.stock_max = new_data['maxSTK']
                stock.save()
            
            #print("get to reverse")
            return HttpResponse(status = 200)
            #return HttpResponseRedirect(reverse("desk_app:stock_api")) 
            # TODO на листі stock в колонці manuf показувати скорочену назву постачальника. 

    # get Товары item id to use it in the future
    tovaru_id = ICgroups.objects.filter(group_name='Товары')

    # get all groups form db 
    groups_list =  list(ICgroups.objects.all().values('id', 'group_name', 'parent_guid_id'))#.exclude(group_name='Товары'))
    
    # get list of parent_id's from scu 
    scu_parent_id =  IC_scu.objects.all().values_list('scu_parent_guid',  flat=True).distinct()

    # defaultdict(<class 'list'>, {None: [{3271: 'Товары'}], 3271: [{3272: 'Группа Бакалея. Хлеб'}, {3273: 'Фито группа.  Основная'},...
    itemdict = defaultdict(list)
    for item in groups_list:
        itemdict[item['parent_guid_id']].append({item['id']: item['group_name']})

    # create list of lists
    data_to_grid = []
    # function to get list of scu by its parent code 
    def get_scu_list(parent_code):
        result = IC_scu.objects.filter(scu_parent_guid=parent_code).values( 'id', 
                                                                            'scu_parent_guid', 'scu_name', 
                                                                            'scu_article', 'scu_barcode', 
                                                                            'scu_guid_data__abc_result', 
                                                                            'scu_safety_stock__safe_stock',
                                                                            'scu_safety_stock__provider',
                                                                            'scu_safety_stock__multipl',
                                                                            'scu_safety_stock__only_max',
                                                                            'scu_safety_stock__stock_max'
                                                                            )
        # print(result)
        return result     
        # TODO подальші дії: в списку постачальників обрати визначити інтерфейс графіку замовленнь - кнопки з назвами, 
        # чи ще щось. 


    # recursion function to get all children for item from list of dicts
    def printitem(id_item, depth=0):        
        for child in itemdict[id_item]:
            # print(child) -> {3272: 'Группа Бакалея. Хлеб'}
            # [key for key in child.keys()][0] -> Кондитерка. Разное
            
            child_id = [key for key in child.keys()][0]
            name = child[child_id]
                        
            # append data to list  
            data_to_grid.append({'id': child_id, 'scu_name': name})
            #data_to_grid.append(child)
            # if group has children scu 
            if child_id in scu_parent_id:
                # get list of child elements from db
                child_scu = get_scu_list(child_id)
                for scu in child_scu:
                    # append scu after group to the list
                    data_to_grid.append(scu)
                               
            printitem([key for key in child.keys()][0], depth+1)        
    # 3271 - 
    printitem(tovaru_id[0].id)    

    print(data_to_grid[:10])

    return JsonResponse(data_to_grid, safe=False)

def stock(request):
    return render(request, 'desk_app/stock.html')  

# rout to get list of manufacturers from db for /stock table
def manuf_api(request):
    result = list(Producers.objects.all().values('id', 'producer_name'))
    return JsonResponse(result, safe=False)
