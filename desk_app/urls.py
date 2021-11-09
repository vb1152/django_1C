from django.urls import path, re_path

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

    path("abc_api", views.abc_api, name="abc_api"),
    path("sheet_api", views.sheet_api, name="sheet_api"),
    path("load_scu", views.load_scu, name="load_scu"),
    path("simple_list", views.simple_list, name="simple_list"),
    path("load_barcode", views.load_barcode, name="load_barcode"),
    path("load_prices", views.load_prices, name="load_prices"),
    path("price_list_all", views.price_list_all, name="price_list_all"), 
    path("produsers", views.produsers, name="produsers"),
    path("abc", views.abc, name = "abc"), 
    
    # API Routs for produsers stock table
    path("stock_api", views.stock_api, name="stock_api"),
    path("stock_api/<int:id>", views.stock_api, name="stock_api"),
    path("progress_api", views.progress_api, name="progress_api"),
    path("stock", views.stock, name="stock"),
    path("sheet", views.sheet, name = "sheet"), 

    # rout to get list of manufacturers from db for /stock table
    path("manuf_api", views.manuf_api, name = "manuf_api"), 

    path("delete_data", views.delete_data, name = "delete_data"),
    path("load_all_data", views.load_all_data, name = "load_all_data"), # rout all data from 1C 
    path("load_price_from_xml", views.load_price_from_xml, name="load_price_from_xml"), 
    path("delete_prices_xml", views.delete_prices_xml, name="delete_prices_xml"),
    path("data", views.data, name="data"),
    path("data_api", views.data_api, name="data_api"),
    path("check_new_folders", views.check_new_folders, name = "check_new_folders"),
    path("delete_barcode", views.delete_barcode, name = "delete_barcode"),
    path("delete_scu", views.delete_scu, name = "delete_scu"),
    path("orders", views.orders, name="orders"),
    path("make_order_api", views.make_order_api, name="make_order_api"),
    path("open_order_file_api", views.open_order_file_api, name="open_order_file_api"),
    path('send_order_file_api', views.send_order_file_api, name='send_order_file_api'),
    
    re_path(r'^groups/$', views.show_groups)
    
   


    
]    
