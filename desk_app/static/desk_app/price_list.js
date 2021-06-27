//script to highlight by grey group names on .../price_list_all? url

document.addEventListener('DOMContentLoaded', function() {
    td_array = document.getElementsByTagName("td");
    check_value = 'is_group';

    for (i = 0; i < td_array.length; i++){
        if (td_array[i].classList.contains(check_value)){
            td_array[i].parentNode.style.backgroundColor = "grey";
            };
    };
});