document.addEventListener('DOMContentLoaded', function() {
    
    fetch('/IC_connection/check')
    .then(function(response) {
        if(response.status === 200) {
            document.querySelector('#ICstatus').innerHTML = '1С connected.'
            }
        else {
            const stat = document.querySelector('#ICstatus')
            stat.innerHTML = '1С no connection.'
            stat.setAttribute("class", "alert alert-danger");
        }    
    });
});


function progress() {
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
                
                bar.setAttribute("style","width:" + response.progress + "%;");
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
    document.querySelector('.jsGrid').innerHTML = 'jsGrid'
}