// using jQuery
function obtenerCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


$(document).ready(function(){

    $("#form-random").submit(function (e) {
        e.preventDefault();
        var csrftoken = obtenerCookie('csrftoken');

        alert( csrftoken );
        $.ajax({
            url: "randomTesting",
            async: false,
            method: "POST",
            data: { numeroEventos: $('#eventos').val() , semilla: $('#semilla').val(), ruta: $('#ruta').val() },
            dataType: "json",
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                //$('#loader').show();
            }
        }).done(function (data) {
            unidades = data;
        }).fail(function (jqXHR, textStatus) {
            alert("Request failed: " + textStatus);
        }).always(function () {
            //$('.loader').hide();
        });

        return false;
    });
});