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
        heading: true, //'true' show heading of the table

        pageSize: 10,
        pageButtonCount: 3,

        deleteConfirm: "Бажаєте видалити товар із замовлення?",

        controller: {
            
            loadData: function(filter) {
                var d = $.Deferred();
                $.ajax({
                    type: "GET",
                    url: "/make_order_api",
                    data: filter
                }).done(function(result) {
                    d.resolve($.map(result, function(item) {
                        return $.extend(item.fields, { 
                                                        id: item.scu__id,
                                                        scu__scu_name: item.scu__scu_name,
                                                        scu__scu_barcode: item.scu__scu_barcode, 
                                                        order: item.order,
                                                        scu__who_price: item.scu__who_price

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

        onDataLoaded: function (data, args) {
            items = data.data
            
        },

        onRefreshed: function(args) {
            //https://jsfiddle.net/tabalinas/6qru8gne/
            var items = args.grid.option("data");
            var total = { Name: "Total", "Sum": 0, IsTotal: true };
            
            items.forEach(function(item) {
                total.Sum += item.Sum;
            });
            var $totalRow = $("<tr>").addClass("total-row");
            args.grid._renderCells($totalRow, total);
            args.grid._content.append($totalRow);
        },

        fields: [
                { name: "scu__scu_name", title: "Name", type: "text", width: 150, filtering: false },
                { name: "scu__scu_barcode", title: "Barcode", type: "text", width: 50, filtering: false },
                { name: "order", title: "Order", type: "number", width: 20 },
                { name: "scu__who_price", title: "Price", type: "number", width: 20 },
                { name: "order_times_prise", title: "Total", type: "number", width: 20},
                { type: "control" }

        ]
    });

});