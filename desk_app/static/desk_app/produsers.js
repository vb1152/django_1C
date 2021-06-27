// script to create dinamic jsGrid table 


$(document).ready(function() {
    console.log('ajax run produsers');
    $("#jsGrid").jsGrid({
        height: "auto",
        width: "100%",

        filtering: true,
        inserting: true,
        editing: true,
        sorting: true,
        paging: true,
        autoload: true,
        heading: true, //'true' show heading of the table

        pageSize: 10,
        pageButtonCount: 3,

        deleteConfirm: "Бажаєте видалити запис про постачальника?",

        controller: {
            
            loadData: function(filter) {
                var d = $.Deferred();
                console.log('ajax GET produsers');
                console.log(filter);
                $.ajax({
                    type: "GET",
                    url: "/produsers_api",
                    data: filter
                }).done(function(result) {
                    console.log('result produsers');
                    d.resolve($.map(result, function(item) {
                        //console.log('item')
                        //console.log(item.id)
                        return $.extend(item.fields, { 
                                                        id: item.id,
                                                        Name_1C: item.producer_name, 
                                                        Short_name: item.short_prod_name, 
                                                        Contact: item.contact_data,
                                                        Email: item.email_order,
                                                        Info: item.info_field
                                                    });
                    }));
                });

                return d.promise();
            },
            
            insertItem: function(item) {
                return $.ajax({
                    type: "POST",
                    url: "/produsers_api",
                    data: item,
                    headers:{
                        "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()
                    },
                });
            },

            updateItem: function(item) {
                var csrftoken = $("[name=csrfmiddlewaretoken]").val(); //save csrftoken in var 
                //console.log(csrftoken);
                return $.ajax({
                    type: "PUT",
                    url: "/produsers_api/" + item.id,
                    data: item,
                    headers:{
                        "X-CSRFToken": csrftoken
                    },

                });
            },

            deleteItem: function(item) {
                return $.ajax({
                    type: "DELETE",
                    url: "/produsers_api/" + item.id,
                    headers:{
                        "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()
                    },
                });
            }
        },

        fields: [
            { name: "Name_1C", type: "text", width: 200 },
            { name: "Short_name", type: "text", width: 70 },
            { name: "Contact", type: "text", width: 150 },
            { name: "Email", type: "text", width: 100, filtering: false},
            { name: "Info", type: "text", width: 200},
            { type: "control" }
        ]
    });

});