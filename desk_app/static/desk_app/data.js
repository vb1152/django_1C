document.addEventListener('DOMContentLoaded', function() {
    
    console.log('data run')
    fetch('/data_api')
        .then((response) => {
            if (response.status === 200) {
                return response.json();
            } 
            else {
                alert('Помилка 404 на сервері.')
            }
        })
        .then((data) => {

            document.querySelector('#folders_quantity').innerHTML = 'В базі ' + data.folders_quantity + ' груп.' 
            document.querySelector('#scu_quantity').innerHTML = 'В базі ' + data.scu_quantity + ' товарів.' 
            document.querySelector('#folders_date_time').innerHTML = data.event_group;
            document.querySelector('#scu_date_time').innerHTML = data.event_scu;
            document.querySelector('#barcode_date_time').innerHTML = data.event_barcode;
            document.querySelector('#barcode_data').innerHTML = 'В базі ' + data.barcode + ' штрихкодів'
            document.querySelector('#event_price').innerHTML = data.event_price;
            document.querySelector('#prices_count').innerHTML = 'В базі ' + data.prices_count + ' цін'

            console.log(data);
        });    
    
    document.querySelector('#load_barcode').addEventListener('click', () => load_barcode());
    document.querySelector('#load_all_data').addEventListener('click', () => load_all_data());
    document.querySelector('#check_new_folders').addEventListener('click', () => check_new_folders());
    document.querySelector('#load_scu').addEventListener('click', () => load_scu());
    document.querySelector('#delete_data').addEventListener('click', () => delete_data());
    document.querySelector('#load_prices').addEventListener('click', () => load_prices());
    document.querySelector('#load_price_from_xml').addEventListener('click', () => load_price_from_xml());
    document.querySelector('#delete_prices_xml').addEventListener('click', () => delete_prices_xml());
    document.querySelector('#delete_barcode').addEventListener('click', () => delete_barcode());
    document.querySelector('#delete_scu').addEventListener('click', () => delete_scu());

    


    
});

function delete_scu() {
    document.querySelector('.status_text').innerHTML = "Видаляю всі SCU з бази..."

    fetch('/delete_scu')
    .then((response) => {
        return response.json();
      })
    .then((data) => {
        console.log(data);
        document.querySelector('.status_text').innerHTML = data.comment
        });
}

function delete_barcode() {
    document.querySelector('.status_text').innerHTML = "Видаляю штрихкоди з бази..."

    fetch('/delete_barcode')
    .then((response) => {
        return response.json();
      })
    .then((data) => {
        console.log(data);
        document.querySelector('.status_text').innerHTML = data.comment
        });
}

function load_barcode() {
    fetch('/load_barcode')
    .then((response) => {
        return response.json();
      })
    .then((data) => {
        console.log(data);
        document.querySelector('.status_text').innerHTML = data.comment
        });
}

function load_all_data() {
    //function to load folders from IC

    document.querySelector('.status_text').innerHTML = "Завантаження папок... очікуйте."

    fetch('/load_all_data', {
        method: 'POST',
        headers:{
            "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()
        }
        
    })
    
    .then((response) => {
        return response.json();
      })
    .then((data) => {
        //console.log(data);
        document.querySelector('.status_text').innerHTML = data.comment
        });
}


function check_new_folders() {
    document.querySelector('.status_text').innerHTML = "Перевірка наявності нових папок в групі Товари..."
    
    fetch('/check_new_folders')
    .then((response) => {
        return response.json();
      })
    .then((data) => {
        console.log(data);
        document.querySelector('.status_text').innerHTML = data.comment
        });
}

function load_scu(){
    fetch('/load_scu')
    .then((response) => {
        return response.json();
      })
    .then((data) => {
        //console.log(data);
        document.querySelector('.status_text_scu').innerHTML = data.comment
        });
}

function delete_data() {
    
    fetch('/delete_data', {
        method: 'POST',
        headers:{
            "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()
        }
    })
    .then((response) => {
        return response.json();
      })
    .then((data) => {
        //console.log(data);
        document.querySelector('.status_text').innerHTML = data.comment
        });
}


function load_prices(){
    document.querySelector('.status_text').innerHTML = "Завантажую актуальні ціни з 1С в базу... "

    fetch('/load_prices')
    .then((response) => {
        return response.json();
      })
    .then((data) => {
        //console.log(data);
        document.querySelector('.status_text' ).innerHTML = data.comment
        });

}


function load_price_from_xml() {
    fetch('/load_price_from_xml')
    .then((response) => {
        return response.json();
      })
    .then((data) => {
        console.log(data);
        document.querySelector('.status_text').innerHTML = data.comment
        });
}


function delete_prices_xml() {
    fetch('/delete_prices_xml')
    .then((response) => {
        return response.json();
      })
    .then((data) => {
        console.log(data);
        document.querySelector('.status_text').innerHTML = data.comment
        });
}
