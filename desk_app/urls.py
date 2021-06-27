from django.urls import path

from . import views


app_name = "desk_app"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("IC", views.IC, name="IC"),


    # API Routes
    path("IC_connection/<str:IC_connection>", views.IC_connection, name="IC_connection"),
    
    # API Routs for produsers table
    path("produsers_api", views.produsers_api, name="produsers_api"),
    path("produsers_api/<int:id>", views.produsers_api, name="produsers_api"),
    #url(r'^api/(?P<client_id>[0-9]+)/?$', Clients.as_view()),

    path("abc_api", views.abc_api, name="abc_api"),
    path("sheet_api", views.sheet_api, name="sheet_api"),
    
    # rout to listen buttom from index page to load data from IC
    path("load_data_from_IC", views.load_data_from_IC, name="load_data_from_IC"), 
    path("load_scu_from_IC", views.load_scu_from_IC, name="load_scu_from_IC"),
    
    #path("show_pricelist", views.show_pricelist, name="show_pricelist"),

    path("simple_list", views.simple_list, name="simple_list"),
    path("load_barcode", views.load_barcode, name="load_barcode"),
    path("load_prices", views.load_prices, name="load_prices"),
    path("price_list_all", views.price_list_all, name="price_list_all"), 
    path("produsers", views.produsers, name="produsers"),
    path("abc", views.abc, name = "abc"), 
    
    # API Routs for produsers stock table
    path("stock_api", views.stock_api, name="stock_api"),
    path("stock_api/<int:id>", views.stock_api, name="stock_api"),
    
    
    path("stock", views.stock, name="stock"),
    path("sheet", views.sheet, name = "sheet"), 

    # rout to get list of manufacturers from db for /stock table
    path("manuf_api", views.manuf_api, name = "manuf_api")
   


    
]    
