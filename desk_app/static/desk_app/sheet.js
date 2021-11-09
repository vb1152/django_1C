// script to create dinamic jsGrid table 


$(document).ready(function() {
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
                    url: "/sheet_api",
                    data: filter
                }).done(function(result) {
                    d.resolve($.map(result, function(item) {
                        return $.extend(item.fields, { 
                                                        Назва: item.Назва, 
                                                        ПочЗал: item.КоличествоOpeningBalance, 
                                                        Приход: item.КоличествоReceipt,
                                                        Расход: item.КоличествоExpense,
                                                        КінЗал: item.КоличествоClosingBalance,
                                                        Клас: item.class
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
            { name: "Назва", type: "text", width: 150 },
            { name: "ПочЗал", type: "number", width: 15 },
            { name: "Приход", type: "number", width: 15 },
            { name: "Расход", type: "number", width: 15 },
            { name: "КінЗал", type: "number", width: 15 },
            { name: "Клас", type: "text", width: 10 },

            { type: "control" }
        ]
    });

});