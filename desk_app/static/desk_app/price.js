// script to create dinamic jsGrid table 
$(function() {
    $("#jsGrid").jsGrid({
        height: "auto",
        width: "100%",

        filtering: true,
        inserting: true,
        editing: true,
        sorting: true,
        paging: true,
        autoload: true,

        pageSize: 10,
        pageButtonCount: 5,

        deleteConfirm: "Do you really want to delete client?",

        controller: {
            loadData: function(filter) {
                var d = $.Deferred();
                $.ajax({
                    type: "GET",
                    url: "/price_list_all",
                    data: filter
                }).done(function(result) {
                    d.resolve($.map(result, function(item) {
                        return $.extend(item.fields, { 
                                                        name: item.name, 
                                                        articul: item.articul, 
                                                        barcode: item.barcode,
                                                        wh_price: item.wh_price,
                                                        rt_price: item.rt_price,
                                                        class: item.class
                                                    });
                    }));
                });

                return d.promise();
            },

            insertItem: function(item) {
                return $.ajax({
                    type: "POST",
                    url: "/clients/api",
                    data: item
                });
            },

            updateItem: function(item) {
                return $.ajax({
                    type: "PUT",
                    url: "/clients/api/" + item.id,
                    data: item
                });
            },

            deleteItem: function(item) {
                return $.ajax({
                    type: "DELETE",
                    url: "/clients/api/" + item.id
                });
            }
        },

        fields: [
            { name: "id", type: "text", width: 30 },
            { name: "name", type: "text", width: 150 },
            { name: "articul", type: "text", width: 70 },
            { name: "barcode", type: "text", width: 150 },
            { name: "wh_price", type: "number", width: 50, filtering: false },
            { name: "rt_price", type: "number", width: 50, filtering: false },
            { name: "class", type: "text", width: 10},  
            { type: "control" }
        ]
    });

});