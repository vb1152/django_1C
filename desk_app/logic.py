from .models import SalesForAbc
from django.db.models import F
from .models import ICparams
import requests
import json

# function to get data from IC
# http://localhost:80/base/odata/standard.odata/Catalog_Номенклатура?$format=json
def get_data_from_IS(end_url):
    #connecting to IC 
    url = ICparams.objects.filter()[:1].get()
    # http://localhost:80/base/odata/standard.odata
    session = requests.Session()
    session.auth = (url.sessionIC_login.encode('UTF-8'), url.sessionIC_password)
    response = session.get(url)
    if response.status_code == 200:
        #metadata = "/Catalog_Номенклатура?$format=json"
        # Catalog_Номенклатура?$format=json
        # print url link for odata access  
        # print(str(url) + end_url)
        nom_response = session.get(str(url) + end_url)
        response_dict = json.loads(nom_response.text)
        
        return response_dict['value']
    else:
        return {'error': 'No connection'}


# func to get data about scu from IC 
def ic_data_scu(guid):
    name_from_ic = get_data_from_IS(f"/Catalog_Номенклатура?$filter=Ref_Key eq guid'{guid}'&$format=json")
    
    return name_from_ic[0]['Description']
