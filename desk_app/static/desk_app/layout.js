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

    console.log(window.location.href)

    
    //document.querySelector('#price_list_groups').addEventListener('click', () => change_div_id());

    
    //document.querySelector('#load_all_data').addEventListener('click', () => load_all_data());

    
    //document.querySelector('#load_from_xml').addEventListener('click', () => load_from_xml());
    
    

});







function load_from_xml() {
    console.log("load_from_xml")
    fetch('/load_from_xml')
    .then((response) => {
        return response.json();
      })
    .then((data) => {
        console.log(data);
        document.querySelector('.status_text').innerHTML = data.comment
        });
}

function progress() {
    console.log("progress");


    const bar_div = document.getElementById('progress') //show progress bar
    bar_div.hidden = false;

    document.querySelector('.status_text').innerHTML = "Завантаження груп товарів триває..."

    const intervalLength = 3000;
    const bar = document.getElementById('progress-bar')
    const interval = setInterval(() => {
        $.ajax({
            type: 'GET',
            url: '/progress_api',
            headers:{
                "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()
            },
            data: {
                comment : "load_data"
            },
            success:function(response){
                // Do visualization stuff then check if complete
                
                console.log(response)
                bar.setAttribute("style","width:" + response.progress + "%;");
                //bar.style.width = response.progress + '%;';
                bar.setAttribute('aria-valuenow', response.progress);
                bar.innerHTML = response.progress + "%";
                
                
                
                if (response.progress >= 100) {
                    clearInterval(interval);

                    bar_div.hidden = true;

                }
            }
        });
    }, intervalLength);


}


function change_div_id(){
    console.log("change id to jsGrid")
    document.querySelector('.jsGrid').innerHTML = 'jsGrid'
}