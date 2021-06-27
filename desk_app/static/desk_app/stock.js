// script to create dinamic jsGrid table 

$(document).ready(function() {
    // rout to get list of manufacturers from db 
    $.ajax({
        type: "GET",
        url: "/manuf_api"
    }).done(function(manuf_list) {
        console.log(manuf_list)
        manuf_list.unshift({ id: 0, producer_name: "" });

    //console.log('ajax run');
    $("#jsGrid").jsGrid({
        height: "auto",
        width: "100%",

        filtering: true,
        inserting: true,
        editing: true,
        sorting: true,
        paging: false,
        autoload: true,

        pageSize: 10,
        pageButtonCount: 5,

        deleteConfirm: "Do you really want to delete client?",
        
        //add data to a class attribute  
        rowClass: function(item, itemIndex) { 
            if (!("articul" in item)) {
                return "group";
            } else if ("class" in item) {
                //console.log(item.class)
                if (item.class == "A") {return "A"} 
                else if (item.class == "B"){return "B"}
                else if (item.class == "C"){return "C"}
            }
        },

        controller: {
            loadData: function(filter) {
                var d = $.Deferred();
                //console.log('ajax GET stock');
                $.ajax({
                    type: "GET",
                    url: "/stock_api",
                    dataType: "json",
                    data: filter
                }).done(function(result) {
                    //console.log('result');
                    //console.log(result.scu_list);
                    //rowClass(item);
                    d.resolve($.map(result, function(item) {
                        //console.log(manuf_list.find(x => x.id == '1').producer_name)
                        //console.log(item.scu_produser__producer_name)
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

            deleteItem: function(item) {
                return $.ajax({
                    type: "DELETE",
                    url: "/clients/api/" + item.id
                });
            },
            
        },

        fields: [
            { name: "name", type: "text", width: 100, editing: false },
            { name: "articul", type: "text", width: 5, editing: false },
            { name: "barcode", type: "text", width: 30, editing: false },
            { name: "class", type: "text", width: 5, editing: false }, // АБС клас товару 
            { name: "sfs", type: "number", width: 10, filtering: false }, // страховий запас 
            { name: "mlt", type: "number", width: 10, filtering: false }, // кратність 
            { name: "maxOrd", type: "number", width: 10, filtering: false }, // максимальне замовлення 
            { name: "maxSTK", type: "number", width: 10, filtering: false }, //максимально можливий залишок


            { name: "manuf", selectedIndex: -1, autosearch: true, type: "select",
                width: 50, items: manuf_list, editing: true, valueField: "id", textField: "producer_name",
                filterValue: function() { 
                    return this.items[this.filterControl.val()][this.textField]}
            },
            
            { type: "control" }
        ]
    });

    });

});