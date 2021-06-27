document.addEventListener('DOMContentLoaded', function() {
    
    console.log('layout run')
    
    fetch('/IC_connection/check')
    //.then(response => response.json())
    .then(function(response) {
        //console.log(response.status);
        if(response.status === 200) {

        //    console.log('if');
            document.querySelector('#ICstatus').innerHTML = '1С підключено.'

            }
        else {
            const stat = document.querySelector('#ICstatus')
            stat.innerHTML = '1С відключено.'
            stat.setAttribute("class", "alert alert-danger");
        }    
    });

    document.querySelector('#load_data').addEventListener('click', () => load_ICdata());
    document.querySelector('#load_scu').addEventListener('click', () => load_scu_data());
    document.querySelector('#load_barcode').addEventListener('click', () => load_barcode());
    document.querySelector('#load_prices').addEventListener('click', () => load_prices());
    //document.querySelector('#price_list_groups').addEventListener('click', () => change_div_id());
    
   
    
});

function load_ICdata() {
    fetch('/load_data_from_IC')
    .then((response) => {
        return response.json();
      })
    .then((data) => {
        //console.log(data);
        document.querySelector('.status_text').innerHTML = data.comment
        });
}

function load_scu_data(){
    fetch('/load_scu_from_IC')
    .then((response) => {
        return response.json();
      })
    .then((data) => {
        //console.log(data);
        document.querySelector('.status_text_scu').innerHTML = data.comment
        });
}

function load_barcode(){
    fetch('/load_barcode')
    .then((response) => {
        return response.json();
      })
    .then((data) => {
        //console.log(data);
        document.querySelector('.status_text_barcode').innerHTML = data.comment
        });

}

function load_prices(){
    fetch('/load_prices')
    .then((response) => {
        return response.json();
      })
    .then((data) => {
        //console.log(data);
        document.querySelector('.status_text_prices').innerHTML = data.comment
        });

}

function change_div_id(){
    console.log("change id to jsGrid")
    document.querySelector('.jsGrid').innerHTML = 'jsGrid'
}