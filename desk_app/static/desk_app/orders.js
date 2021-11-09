$(document).ready(function(){
    $('.modal').on('change', 'style-display', function(){
        $(this).removeData();
    });
    
    $.ajax({
        type: "GET",
        url: "/manuf_api"
    }).done(function(manuf_list) {
        $.each(manuf_list, function(key, value) {
            var r= $('<button type="button" class="btn btn-outline-secondary">'+value.producer_name+'</button>').click(function(){
                
                $.ajax({ //make order for a produser. send produsers id to /make_order_api
                    url: "/make_order_api",
                    data: {
                        id: value.id
                    },
                    
                })
                .fail(function(response) {
                    alert(response.responseJSON.comment);
                })
                
                .done(function(result) {
                    //show modal
                    modal.style.display = "block";
                    
                    // When the user clicks anywhere outside of the modal, close it
                    window.onclick = function(event) {
                        if (event.target == modal) {
                            modal.style.display = "none";
                            
                            // remove data from a modal when its closed
                            $('#myDynamicTable').html("");
                            $('#open_button').off('click');
                            $('#send_button').off('click');
                            
                        };
                    };

                    $('#modal_footer').text(result.path_to_file);
                    $('#email').text(result.email)

                    //$('.modal-body').text(result.comment)
                    $('#open_button').click(function(){ //call back end function to open excel file
                        $.ajax({
                            type: 'GET',
                            url: "/open_order_file_api",
                        });
                    })

                    $('#send_button').click(function(){ //call back end function to open send files
                        $.ajax({
                            type: 'GET',
                            url: "/send_order_file_api",
                        })
                        .done (function(result) {
                            $('#result_send_order').text(result.comment);
                            result_send_order
                        });
                    });
                    $('#modal_header').text('Order ' + result.prod_name)

                    //function to add table to 
                    addTable(result.order, result.headers);

                    $('#orderResult').text('The minimum amount of the suppliers order ' + result.min_sum + 
                                            '. The total amount of the order: ' + result.order_sum)
                })
            })

            $(".btn-group-vertical").append(r);
        });
    });
    // Get the modal
    var modal = document.getElementById("myModal");
    
});

function addTable(data, header, sum) {
    var myTableDiv = document.getElementById("myDynamicTable");
  
    var table = document.createElement('table');
    let headerRow = document.createElement('tr');
    //https://www.fwait.com/how-to-create-table-from-an-array-of-objects-in-javascript/
    header.forEach(headerText => {
        let header = document.createElement('th');
        let textNode = document.createTextNode(headerText);
        header.appendChild(textNode);
        headerRow.appendChild(header);
    });
    table.appendChild(headerRow);
    //table.border = '1';
  
    var tableBody = document.createElement('TBODY');
    table.appendChild(tableBody);


    for (let one_scu of data) {
        var tr = document.createElement('TR');
        table.appendChild(tr);
        
        for (const [ key, value ] of Object.entries(one_scu) ) {
            var td = document.createElement('TD');

            if (key == 'scu__scu_name') {
                td.width = '400';
                td.align='left';
            } else {
                td.width = '100';
                td.align='center';
            };
            
            td.appendChild(document.createTextNode(value));
            tr.appendChild(td);
        }
    }
  
    myTableDiv.appendChild(table);
  };