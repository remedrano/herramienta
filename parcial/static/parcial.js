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
    $('#btn-random-reporte').on('click', function(){
        $('.container').hide();
        $('#random-reporte').show();
    });

    $('#btn-calabash-reporte').on('click', function(){
        $('.container').hide();
        $('#calabash-reporte').show();
    });

    $('#btn-vrt-reporte').on('click', function(){
        $('.container').hide();
        $('#vrt-reporte').show();
    });

    $('#btn-random').on('click', function(){
        $('.container').hide();
        $('#contenido-random').show();
    });

    $('#btn-calabash').on('click', function(){
        $('.container').hide();
        $('#contenido-calabash').show();
    });

    $('#btn-vrt').on('click', function(){
        $('.container').hide();
        $('#contenido-vrt').show();
    });

    $('#reporteRandom').on('click', function(){
        var csrftoken = obtenerCookie('csrftoken');
        $.ajax({
            url: "generarReporteRandom",
            async: false,
            method: "POST",
            data: {  },
            dataType: "json",
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }).done(function (data) {

            $("#tabla-reporte-random tbody").html('');
            var cantidad = 0;
            var html = "";
            for( var indice in data){
                cantidad = ""+(indice + 1);
                html+="<tr>" +
                    "<td>"+cantidad+"</td>" +
                    "<td>"+data[indice].fecha+" "+data[indice].hora+"</td>" +
                    "<td >"+data[indice].mutante+"</td>" +
                    "<td style='color: red'>"+data[indice].des+"</td>" +
                    "<td style='color: red'>"+data[indice].linea+"</td>" +
                    "</tr>"

            }
            $("#tabla-reporte-random tbody").append( html );

            var totalRandom = $("#tabla-reporte-random tbody tr").length;
            $("#totalRandom").val( totalRandom );

        }).fail(function (jqXHR, textStatus) {
            alert("Request failed: " + textStatus);
        }).always(function () {
            //$('.loader').hide();
        });
    });



    $('#ejecutarCalabash').on('click', function(){
        var csrftoken = obtenerCookie('csrftoken');
        $.ajax({
            url: "ejecutarCalabash",
            async: false,
            method: "POST",
            data: {  },
            dataType: "json",
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }).done(function (data) {
            unidades = data;
        }).fail(function (jqXHR, textStatus) {
            alert("Request failed: " + textStatus);
        }).always(function () {
            //$('.loader').hide();
        });
    });

    $('#agregarPermiso').on('click', function(){
        var csrftoken = obtenerCookie('csrftoken');
        $.ajax({
            url: "permisoInternetApks",
            async: false,
            method: "POST",
            data: {  },
            dataType: "json",
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }).done(function (data) {
            unidades = data;
        }).fail(function (jqXHR, textStatus) {
            alert("Request failed: " + textStatus);
        }).always(function () {
            //$('.loader').hide();
        });
    });

    $("#form-random").submit(function (e) {
        e.preventDefault();
        var csrftoken = obtenerCookie('csrftoken');

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