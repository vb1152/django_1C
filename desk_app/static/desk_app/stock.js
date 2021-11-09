// script to create dinamic jsGrid table 

$(document).ready(function() {
    //code to use decimal numbers
    //https://github.com/tabalinas/jsgrid/issues/621 - 
    function DecimalField(config) {
        jsGrid.fields.number.call(this, config);
    }
    DecimalField.prototype = new jsGrid.fields.number({
        filterValue: function() {
            return this.filterControl.val()
                ? parseFloat(this.filterControl.val() || 0, 10)
                : undefined;
        },
        insertValue: function() {
            return this.insertControl.val()
                ? parseFloat(this.insertControl.val() || 0, 10)
                : undefined;
        },
        editValue: function() {
            return this.editControl.val()
                ? parseFloat(this.editControl.val() || 0, 10)
                : undefined;
        }
    });
    jsGrid.fields.decimal = jsGrid.DecimalField = DecimalField;

    // rout to get list of manufacturers from db 
    $.ajax({
        type: "GET",
        url: "/manuf_api"
    }).done(function(manuf_list) {
        manuf_list.unshift({ id: 0, producer_name: "" });

    $("#jsGrid").jsGrid({
        
        height: "auto",
        width: "100%",
        
        autosearch: true,
        filtering: true,
        inserting: true,
        editing: true,
        sorting: true,
        paging: false,
        autoload: true,

        pageSize: 10,
        pageButtonCount: 5,

        deleteConfirm: "Do you really want to delete Safety stock data?",
        
        //add data to a class attribute  
        rowClass: function(item, itemIndex) { 
            if (!("articul" in item)) {
                return "group";
            } else if ("class" in item) {
                if (item.class == "A") {return "A"} 
                else if (item.class == "B"){return "B"}
                else if (item.class == "C"){return "C"}
            }
        },

        controller: {
            loadData: function(filter) {
                var d = $.Deferred();
                $.ajax({
                    type: "GET",
                    url: "/stock_api",
                    dataType: "json",
                    data: filter
                }).done(function(result) {
                    
                    d.resolve($.map(result, function(item) {
                        return $.extend(item.fields, {  id: item.id,
                                                        name: item.scu_name, 
                                                        articul: item.scu_article, 
                                                        barcode: item.scu_barcode,
                                                        class: item.scu_guid_data__abc_result,
                                                        sfs: item.scu_safety_stock__safe_stock,
                                                        mlt: item.scu_safety_stock__multipl,
                                                        maxOrd: item.scu_safety_stock__only_max,
                                                        maxSTK: item.scu_safety_stock__stock_max,                                                        
                                                        manuf: item.scu_safety_stock__provider
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
                    url: "/stock_api/" + item.id,
                    data: item,
                    headers: {
                        "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() //get csrftoken in var
                    },
                });
            },

            deleteItem: function(item) { //delete insurance reserves from db
                return $.ajax({
                    type: "DELETE",
                    url: "/stock_api/" + item.id,
                    data: item,
                    headers: {
                        "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() //get csrftoken in var
                    },

                })
                .done(function(result){
                    alert(result.comment)
                });
                },
        },

        fields: [
            { name: "name", type: "text", width: 100, editing: false },
            { name: "articul", type: "text", width: 5, editing: false },
            { name: "barcode", type: "text", width: 30, editing: false },
            { name: "class", type: "text", width: 5, editing: false }, // АБС клас товару 
            { name: "sfs", type: "decimal", width: 20, filtering: false}, // страховий запас 
            { name: "mlt", type: "decimal", width: 20, filtering: false }, // кратність 
            { name: "maxOrd", type: "decimal", width: 20, filtering: false }, // максимальне замовлення 
            { name: "maxSTK", type: "decimal", width: 20, filtering: false }, //максимально можливий залишок


            { name: "manuf", autosearch: true, type: "select", selectedIndex: -1,
                width: 50, items: manuf_list, editing: true, valueField: "id", textField: "producer_name", 
            },
              
            { type: "control" }
        ]
    });
    });
});