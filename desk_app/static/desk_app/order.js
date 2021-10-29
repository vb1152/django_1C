// script to create dinamic jsGrid table 


$(document).ready(function() {
    console.log('ajax run orders');
    
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
                console.log('ajax GET orders');
                console.log(filter);
                $.ajax({
                    type: "GET",
                    url: "/make_order_api",
                    data: filter
                }).done(function(result) {
                    console.log('result orders');
                    d.resolve($.map(result, function(item) {
                        console.log(item)
                        //console.log(item.id)
                        return $.extend(item.fields, { 
                                                        id: item.scu__id,
                                                        scu__scu_name: item.scu__scu_name,
                                                        scu__scu_barcode: item.scu__scu_barcode, 
                                                        order: item.order,
                                                        scu__who_price: item.scu__who_price

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

        onDataLoaded: function (data, args) {
            console.log(data.data)

            items = data.data

            items.forEach(function(item) {
                console.log(item)
            });


        },

        onRefreshed: function(args) {
            //https://jsfiddle.net/tabalinas/6qru8gne/
            //console.log(args.grid)
            var items = args.grid.option("data");
            var total = { Name: "Total", "Sum": 0, IsTotal: true };
            console.log(items)
            
            items.forEach(function(item) {
                total.Sum += item.Sum;
                console.log(total.Sum)
            });
            
            var $totalRow = $("<tr>").addClass("total-row");
            
            args.grid._renderCells($totalRow, total);
            
            args.grid._content.append($totalRow);
        },

        fields: [
                { name: "scu__scu_name", title: "Назва", type: "text", width: 150, filtering: false },
                { name: "scu__scu_barcode", title: "Штрихкод", type: "text", width: 50, filtering: false },
                { name: "order", title: "Замовл", type: "number", width: 20 },
                { name: "scu__who_price", title: "Ціна", type: "number", width: 20 },
                { name: "order_times_prise", title: "Всього", type: "number", width: 20},
                { type: "control" }

        ]
    });

});

//.done(function(result) {
//    console.log(result)
//    console.log(result.comment)
//    console.log(result.order)

       

//})
//.then(function() {
    

    // Get the <span> element that closes the modal
//    var span = document.getElementsByClassName("close")[0];
    // When the user clicks on <span> (x), close the modal
//    span.onclick = function() {
//        console.log("close modal by span")
//    modal.style.display = "none";
//    }

     // When the user clicks anywhere outside of the modal, close it
//    window.onclick = function(event) {
//        if (event.target == modal) {

//            console.log("close modal")
//            modal.style.display = "none";
//        }
 //       }
        
// })



//alert(value.id)
//натиск на кнопку - формується ще дві кнопки. Відкрити і відправити.
// Відкривається xls файл і, редагується і відправляється. після успішної відправки - з
// справа додається запис із замовленням (лінк), за яким можна відкрити саме замовлення і подивитися його деталі 

//$.ajax({
//    url: "/make_order_api",
//    data: {
//        id: value.id
//    },
//    
//})
//.fail(function(response) {
//    console.log(response.status);
//    alert(response.responseJSON.comment);
//})

//console.log("then")
//modal.style.display = "block";


//.done(function(result) {
//    console.log(result)
//    console.log(result.comment)
//    console.log(result.order)
    
       

//})
