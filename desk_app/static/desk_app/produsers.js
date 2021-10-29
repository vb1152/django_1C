// script to create dinamic jsGrid table 


$(document).ready(function() {
    console.log('ajax run produsers');

    $('#clean_files').on( "click", function() {
        //console.log( $( this ).text() );
        $.ajax({
            type: "POST",
            url: "/produsers",
            data: {
                clean_files: "clean_files",
                data_clean: $('[name="clean_files"]').val()
              },
            headers:{
                "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()
            }
        }).done(function(result) {
            console.log(result)
            document.querySelector('.status_text').innerHTML = result.comment
        });
    });

    $('#ready_files').on( "click", function() {
        //console.log( $( this ).text() );
        $.ajax({
            type: "POST",
            url: "/produsers",
            data: {
                ready_files: "ready_files",
                data_ready: $('[name="ready_files"]').val()
              },
            headers:{
                "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()
            }
        }).done(function(result) {
            console.log(result)
            document.querySelector('.status_text').innerHTML = result.comment
        });
    });

    




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
                //console.log(filter);
                $.ajax({
                    type: "GET",
                    url: "/produsers_api",
                    data: filter
                }).done(function(result) {
                    console.log('result produsers');
                    d.resolve($.map(result, function(item) {
                        //console.log(item)
                        //console.log(item.id)
                        return $.extend(item.fields, { 
                                                        id: item.id,
                                                        Name_1C: item.producer_name, 
                                                        Active: item.active, 
                                                        Short_name: item.short_prod_name, 
                                                        Contact: item.contact_data,
                                                        Email: item.email_order,
                                                        Info: item.info_field, 
                                                        min_sum: item.min_sum,
                                                        file_name: item.file_name,
                                                        barcode_col: item. barcode_col,
                                                        order_col: item.order_col

                                                    });
                    }));
                    //console.log(d)
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
            { name: "Name_1C", type: "text", title: "Full name", width: 100 },
            { name: "Active", type: "checkbox", title: "Act", sorting: true, width: 15},
            { name: "Short_name", type: "text", width: 50 },
            { name: "Contact", type: "text", width: 50 },
            { name: "Email", type: "text", width: 100, filtering: false},
            { name: "Info", type: "text", width: 50},
            { name: "min_sum", type: 'number', width: 45, title: "Min sum", align: "left", },
            { name: "file_name", title: "Файл", type: "text", title: "File", width: 100},
            { name: "barcode_col", title: "Barc col", type: "text", width: 20}, 
            { name: "order_col", title: "Ord col", type: "text", width: 20},
            { type: "control" }
        ]
    });

});