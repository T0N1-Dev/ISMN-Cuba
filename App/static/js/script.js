/*----------------------------------------------------
# All the script here it will extends to all the pages
* -----------------------------------------------*/
// 1) Script tp validate all inputs
function validateEmail(email){
    var regex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
    return regex.test(email);
}

function validateAll() {

    var username = $("#username").val();
    var password = $("#userPassword").val();
    var phone = $("#phone").val();
    var email = $("#email").val();
    var editor_type = $("#editorType").val();
    var age = $("#age").val();
    var first_name = $('#first_name').val();
    var last_name = $('#last_name').val();
    var address = $("#address").val();
    var file = $("#file").val();
    var idTribute = $("#idTribute").val();
    var title = $("#title").val()


    if (username === '') {
        swal("Opsss !", "Inserte su nombre de usuario.", "error");
        return false;
    } else if (password === '') {
        swal("Opsss !", "Inserte una contraseña.", "error");
        return false;
    } else if (phone === '') {
        swal("Opsss !", "Inserte su número de teléfono.", "error");
        return false;
    } else if (email === '') {
        swal("Opsss !", "Inserte su dirección de correo electrónico.", "error");
        return false;
    } else if (editor_type === '') {
        swal("Opsss !", "Seleccione un tipo de Editor.", "error");
        return false;
    }
    else if (!(validateEmail(email))) {
        swal("Opsss !", "Inserte un correo válido.", "error");
        return false;
    } else if (editor_type === 'Independiente' && age === '') {
        swal("Opsss !", "El campo 'Edad' está vacío.", "error");
        return false;
    } else if (first_name === '') {
        swal("Opss !", "Inserte su nombre.", "error")
        return false;
    } else if (editor_type === 'Independiente' && last_name === '') {
        swal("Opss !", "Inserte su apellido.", "error")
        return false;
    } else if (address === '') {
        swal("Opss !", "La dirección está vacia.", "error")
        return false;
    } else if (file === '') {
        swal("Opss!", "Se ha olvidado la letra de la canción.", "error");
        return false;
    } else if (idTribute === '') {
        swal("Opss!", "Se ha olvidado el número de identificación tributaria.", "error");
        return false;
    } else if (title === '') {
        swal("Opss!", "Se ha olvidado el título de la obra.", "error");
        return false;
    }
    else {
        return true;
    }
}

$("#btn-add, #btn-send").bind("click", validateAll);

// 2) Script (Name field) only letter is allowed
$(document).ready(function (){

    // Only letter
    $('#first_name, #last_name').keyup(function () {
        var letter = $(this).val();
        var allow = letter.replace(/[^a-zA-Z _]/g, '');
        $(this).val(allow);
    });

    //prevent to write space in the input
    $('input').on("keypress", function(e) {

        // Not space at start
        if (e.which === 32 && !$(this).val())
            e.preventDefault();
        // Not two space consecutive
        else if (e.key === ' ' && e.target.value[e.target.value.length - 1] === ' ')
            e.preventDefault();
    });

    $('#userPassword').on("keypress", (e) => {
        if (e.which === 32)
            e.preventDefault();
    });
});

// 3) Script to put First Letter capitalized
$("#autor, #first_name, #last_name, #address").keyup(function () {
    var txt = $(this).val();
    $(this).val(txt.replace(/^(.)|\s(.)/g, function ($1){return $1.toUpperCase( );}));
});

// 4) Script to lowercase input email
$(document).ready(function (){
    $('#email').keyup(function (){
        this.value = this.value.toLowerCase();
    });
});

// 5) Script to allow only numbers in AGE and ID Tribute
$("#age, #idTribute").keyup(function () {
    if(!/^[0-9]*$/.test(this.value)) {
        this.value = this.value.split(/[^0-9]/).join('');
    }
});


// 6) Phone mask
$(document).ready(function (){
    $('#phone').inputmask("+535-999-99-99", { "onincomplete": function () {
        swal('Opsss !', 'Incomplete phone. Review', 'error');
        return false;
        }
    });
});

// 7) If input AGE has number greater than 120, auto clear (alternative oprion)
$(document).ready(function (){
    $("#age").keyup(function (){
        var age = $("#age").val();
        if (age > 120) {
            $("#age").val("");
            return false
        }
    });
});

// 8) Prevent starting by zero in AGE field
$("#age").on("input", function() {
    if(/^0/.test(this.value)) {
        this.value = this.value.replace(/^0/, "");
    }
});

// 10) Time running at real time
setInterval(function (){
    var date = new Date();
    let hour = date.getHours()
    if (hour > 12)
        hour -= 12 // Eliminar horario militar
    let minutes = date.getMinutes()
    let seconds = date.getSeconds()
    $("#clock").html(
        ((hour < 10 ? '0' : hour) + hour + ":" + (minutes < 10 ? '0' : '') + minutes + ":" + (seconds < 10 ? '0' : '') + seconds)
    );
}, 500);

// 11) If not there editors, show a message
var verify = $("#chk_td").length;
if (verify == 0) {
    $("#no-data").text("No se ha encontrado");
}

// 12) ISMN mask
// $(document).ready(function (){
//     let ismn_init = "\\97\\9-0"
//     $('#ismn').inputmask({"mask": ismn_init + "-9999-9999-9"});
// });

// 13) Clear the form if this was closed
$("#sendemailtestModal").on('hidden.bs.modal', function (){
    $("#sendemailtestModal form")[0].reset();
})

// 14)  Ajax Spinner
jQuery(function($) {
    $(document).ajaxSend(function (){
        $("#bg-spinner").fadeIn(500);
    });

    $("#btn-send").click(function (){
        $.ajax({
            type: 'GET',
            success: function (data) {
                var element = document;
                var html = element.outerHTML;
                var data = { html: html };
                var json = JSON.stringify(data)
                var d = $.parseJSON(json);
            }
        }).done(function (){ // Una vez termine ajax correctamente elimina el spinner en 15s.
            setTimeout(function (){
                $("#bg-spinner").fadeOut(500);
            },40000);
        });
    });
});

// 15 Close modal (after 'send button is clicked')
$("#btn-send").click(function (){

    if (validateAll()) {
        document.getElementById("bg-spinner").hidden = false;
        document.getElementById('offcanvasRight').hidden = true;
        $('.close-modal').modal('hide');
    }
    else {
        // Oculta la spinner si hay campos vacios
        document.getElementById("bg-spinner").hidden = true;
    }
})

// 16 Toggle Password Visibility
function toggleFunction(){
    var p = document.getElementById("userPassword");
    var i = document.getElementById("toggleIcon");
    if (p.type === "password"){
        p.type = "text";
        i.classList.remove("fa-eye-slash");
        i.classList.add("fa-eye");
    }
    else {
        p.type = "password"
        i.classList.remove("fa-eye");
        i.classList.add("fa-eye-slash");
    }
}

// Function to activate an age field editor
$("#editorType").change( (e) => {

    const age = $('#age')
    const last_name = $('#last_name')

    if (e.target.value === 'Independiente'){
        age.removeAttr('disabled');
        last_name.removeAttr('disabled')
    }
    else {
        age.val('');
        last_name.val('');
        age.attr('disabled', 'disabled');
        last_name.attr('disabled', 'disabled');
    }
})
