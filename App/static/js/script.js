/*----------------------------------------------------
# All the script here it will extends to all the pages
* -----------------------------------------------*/
// 1) Script tp validate all inputs
function validateEmail(email){
    var regex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
    return regex.test(email);
}

function validateFormatPassword(password) {
    let passwordPattern = /^(?=.*[a-zA-Z])(?=.*\d)[A-Za-z\d]{8,}$/;
    return passwordPattern.test(password.val())
}

function validateCI(ci) {
    let ciValue = ci.val();
    let ciPattern = /^\d{11}$/;
    return ciPattern.test(ciValue);
}

function validateAll() {
    let isValid = true;

    function validateField(field, errorMessage) {
        if (field.val() === '') {
            field.addClass('is-invalid');
            field.removeClass('is-valid');
            swal("Opss !", errorMessage, "error").then(() => {
                field[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
                field.focus();
            });
            isValid = false;
        } else {
            field.removeClass('is-invalid');
            field.addClass('is-valid');
        }
    }

    // Usuarios
    let check = $('#flexCheckDefault');
    let check2 = $('#flexCheckDefault2');
    let username = $("#username");
    let password = $("#userPassword");
    let phone = $("#phone");
    let email = $("#email");
    let fundacion_date = $("#fundacion_date");

    // Autor
    let birthday = $("#birthday");
    let first_name = $('#first_name');
    let last_name = $('#last_name');
    let ci = $('#CI');

    // Editorial
    let nombreEditorial = $('#nombreEditorial');
    let editorialActivity = $('#editorialActivity');
    let editorialNaturalezaJud = $('#editorialNaturalezaJud');
    let representante_name = $('#representante_name');
    let representante_apellido = $('#representante_apellido');

    // Ambos
    let provincia = $('#editorProvincia');
    let municipio = $('#editorMunicipio');
    let address = $("#address");
    let idTribute = $("#idTribute");
    let editorPrefijo = $("#editorPrefijo");

    // Publicacion
    let title = $("#title");
    let autor = $("#autor");
    let editor = $("input[name*='editor']");
    let genero = $("#gender");
    let date = $("#date");
    let letra = $("input[name*='publication_letter']");


    // Validar Checks
    if (check2.length && !check2.is(':checked')) {
        check2.addClass('is-invalid');
        swal("Opss!", "Asegúrese de leer y entender los terminos y condiciones.", "error")
            .then(() => {
                check2[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
                check2.focus();
            });
        isValid = false;
        return isValid;
    } else {
        check2.removeClass('is-invalid').addClass('is-valid');
    }

    if (check.length && !check.is(':checked')) {
        check.addClass('is-invalid');
        swal("Opss!", "Asegúrese de leer y entender los terminos y condiciones y marque la opción de 'leido'.", "error")
            .then(() => {
                check[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
                check.focus();
            });
        isValid = false;
        return isValid;
    } else {
        check.removeClass('is-invalid').addClass('is-valid');
    }

    // Validar email
    if (email.val() && !(validateEmail(email.val()))) {
        email.addClass('is-invalid');
        swal("Opsss !", "Inserte un correo válido.", "error").then(() => {
                email[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
                email.focus();
            });
        isValid = false;
        return isValid;
    } else if (email.val()) {
        email.removeClass('is-invalid');
        email.addClass('is-valid');
    }

    // Validación de la contraseña
    if (password.val() && !validateFormatPassword(password)) {
        swal('Opsss !', 'La contraseña debe tener al menos 8 caracteres y ser alfanumérica.', 'error').then(() => {
                password[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
                password.focus();
            });
        password.removeClass('is-valid').addClass('is-invalid');
        isValid = false;
        return isValid;
    } else if (password.val()) {
        password.removeClass('is-invalid').addClass('is-valid');
    }

    if (username.val() && password.val().includes(username.val())) {
        swal('Opsss !', 'La contraseña NO debe contener el nombre de usuario.', 'error').then(() => {
                password[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
                password.focus();
            });
        password.removeClass('is-valid').addClass('is-invalid');
        isValid = false;
        return isValid;
    } else if (password.val()) {
        password.removeClass('is-invalid').addClass('is-valid');
    }

    // Validar el CI
    if (ci.val() && !validateCI(ci)){
        swal('Opsss !', 'La número de carnet de identidad debe tener 11 dígitos.', 'error').then(() => {
                ci[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
                ci.focus();
            });
        ci.removeClass('is-valid').addClass('is-invalid');
        isValid = false;
        return isValid;
    } else if (ci.val()) {
        ci.removeClass('is-invalid').addClass('is-valid');
    }

    validateField(first_name, "Inserte su nombre.");
    validateField(last_name, "Inserte su apellido.");
    validateField(ci, "Inserte su Carnet de Identidad.");
    validateField(birthday, "El campo 'Fecha de nacimiento' está vacío.");
    validateField(idTribute, "Se ha olvidado el número de identificación tributaria.");
    validateField(nombreEditorial, "Inserte el nombre o razón social de la Editorial.");
    validateField(provincia, "Se ha olvidado seleccionar una provincia.");
    validateField(municipio, "Se ha olvidado seleccionar un municipio.");
    validateField(address, "La dirección está vacía.");
    validateField(phone, "Inserte su número de teléfono.");
    validateField(email, "Inserte su dirección de correo electrónico.");
    validateField(fundacion_date, "Inserte la fecha de fundación de la Editorial.");
    validateField(editorialActivity, "Seleccione la Actividad Principal de la Editorial.");
    validateField(editorialNaturalezaJud, "Seleccione la Naturaleza Jurídica de la Editorial.");
    validateField(representante_name, "Inserte el nombre del responsable  de la Editorial.");
    validateField(representante_apellido, "Inserte el apellido del responsable  de la Editorial.");
    validateField(username, "Inserte su nombre de usuario.");
    validateField(password, "Inserte una contraseña.");
    validateField(editorPrefijo, "Seleccione su número estimado de publicaciones por año.");

    if (letra.val() === '' && document.querySelector('div.edicion') == null) {
        swal("Opss!", "Se ha olvidado la letra de la canción. Seleccione un archivo word, " +
            "pdf o txt donde tenga guardada la letra de la obra musical", "error");
        isValid = false;
    } else if (title.val() === '') {
        swal("Opss!", "Se ha olvidado el título de la obra.", "error");
        isValid = false;
    } else if (autor.val() === '') {
        swal("Opss!", "Se ha olvidado el nombre del autor.", "error");
        isValid = false;
    } else if (editor.val() === '') {
        swal("Opss!", "Se ha olvidado de elegir un editor.", "error");
        isValid = false;
    } else if (genero.val() === '') {
        swal("Opss!", "Se ha olvidado de elegir un género musical.", "error");
        isValid = false;
    } else if (date.val() === '') {
        swal("Opss!", "Se ha olvidado de elegir la fecha de creación de la obra musical.", "error");
        isValid = false;
    }
    return isValid;
}

function validateFieldOnInput() {
    let field = $(this);
    if (field.val().trim() === '') {
        field.addClass('is-invalid');
        field.removeClass('is-valid');
    } else {
        field.removeClass('is-invalid');
        field.addClass('is-valid');
    }
}

$(document).ready(function () {
    $("#btn-add, #btn-send").bind("click", function() {
        return validateAll();
    });

    $("input, select").on("input change", validateFieldOnInput);
});


// 2) Script (Name field) only letter is allowed
$(document).ready(function (){

    // Only letter
    $('#first_name, #last_name, #autor, #representante_apellido, #representante_name, #siglasEditorial, #floatingInput').keyup(function () {
        var letter = $(this).val();
        var allow = letter.replace(/[^a-zA-ZáéíóúñÑ]/g, '');
        $(this).val(allow);

        // Validar después del reemplazo
        if ($(this).val().trim() === '') {
            $(this).removeClass('is-valid').addClass('is-invalid');
        } else {
            $(this).removeClass('is-invalid').addClass('is-valid');
        }
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
$("#autor, #first_name, #last_name, #representante_apellido, #representante_name").keyup(function () {
    var txt = $(this).val();
    $(this).val(txt.replace(/^(.)|\s(.)/g, function ($1){return $1.toUpperCase( );}));
});

// 3.1) Script to capitalize siglas
$("#siglasEditorial").keyup(function () {
    var txt = $(this).val();
    $(this).val(txt.toUpperCase());
});


// 4) Script to lowercase input email
$(document).ready(function (){
    $('#email').keyup(function (){
        this.value = this.value.toLowerCase();
    });
});

// 5) Date validation
$(document).ready(function (){
    $('#birthday, #date, #fundacion_date').blur(function () {
        var currentDate = new Date();
        var date_input = new Date($(this).val())
        if (date_input > currentDate || date_input.getFullYear() < 1900){
            swal('Opsss !', 'Fecha incorrecta. Revise por favor', 'error');
            $(this).val('')
            $(this).removeClass('is-valid').addClass('is-invalid');
        } else {
            $(this).removeClass('is-invalid').addClass('is-valid');
        }
    });
});

// 6) Phone mask
$(document).ready(function (){
    $('#phone').inputmask("+535-999-99-99", { "onincomplete": function () {
            swal('Opsss !', 'Número de teléfono incompleto. Revise por favor', 'error');
            $(this).removeClass('is-valid').addClass('is-invalid');
        return false;
        }
    });
});

// 7) Validate Image Extension
$(document).ready(function() {
    $("input[name*='image']").on('change', function() {

        var filePath = $(this).val();
        var allowedExtensions = /(\.jpg|\.jpeg|\.png|\.gif|\.jfif)$/i;
        if (!allowedExtensions.exec(filePath)) {
            swal('Opsss !', 'Por favor, selecciona un archivo de imagen válido.', 'error');
            $(this).removeClass('is-valid').addClass('is-invalid');
            $(this).val('');
            return false;
        }
        else {
            $(this).removeClass('is-invalid').addClass('is-valid');
            previewImage(event);
        }
    });
});

// 8) Validate Letter Extension
$(document).ready(function () {
    $("input[name='publication_letter']").on('change', function () {
        var filePath = $(this).val();
        var allowedExtensions = /(\.pdf|\.docx|\.txt)/i;
        if (!allowedExtensions.exec(filePath)) {
            swal('Opsss !', 'Por favor, selecciona un archivo de documento válido.', 'error');
            $(this).val('');
            return false;
        }
    });
});

// 9) Validate exporting data
$(document).ready(function () {
    $('#floatingTextarea2').blur(function () {
        let currentDate = new Date();
        let date_input = new Date($(this).val())
        let p_error = $('#p_error')
        console.log($(this).val())
        if (date_input > currentDate || date_input.getFullYear() < 1900 || $(this).val().length < 10){
            $(this).addClass('is-invalid');
            $(this).val('')
            p_error.removeAttr('hidden').html('&ast;&nbsp;Fecha incorrecta.');
        }
        else {
            $(this).removeClass('is-invalid');
            p_error.attr('hidden', 'hidden');
            $(this).addClass('is-valid');
        }
    });
})

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
let verify = $("#chk_td").length;
if (verify === 0) {
    $("#no-data").text("No se ha encontrado");
}

// 12) Script to allow only numbers in ID Tribute
$("#idTribute, #CI, #floatingInput2").keyup(function () {
    if(!/^[0-9]*$/.test(this.value)) {
        this.value = this.value.split(/[^0-9]/).join('');
    }

});

// 13) Validate Description of the Reject
$(document).ready(function(){
    $('#rejectButton').click(function(event) {
        // Prevenir el submit del formulario
        event.preventDefault();

        // Obtener el valor del textarea
        let noteValue = $('#floatingTextarea3').val().trim();
        // Verificar si el textarea está vacío
        if(noteValue === "" || noteValue.length < 50) {
            // Añadir la clase 'is-invalid' al textarea
            $('#floatingTextarea3').addClass('is-invalid');
        } else {
            // Si no está vacío, enviar el formulario
            $('#floatingTextarea3').removeClass('is-invalid');
            $('#form-reject').submit();
            $('#rejectButton i').remove();
            $('.invalid-feedback-spinner').removeAttr('hidden');

        }
    });
});

// 14) Validate Description of the Reject
$(document).ready(function() {
    $('#floatingTextarea3').on('input', function() {
        let textareaContent = $(this).val();
        if (textareaContent.length >= 50) {
            $(this).removeClass('is-invalid').addClass('is-valid');
        } else {
            $(this).removeClass('is-valid');
        }
    });
});

// 15 Reload Image Profile
function previewImage(event) {
    let input = event.target;
    let reader = new FileReader();
    reader.onload = function(){
        let img = document.getElementById("profile-image");
        img.src = reader.result;
    };
    reader.readAsDataURL(input.files[0]);
}

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

// 17 Validate Name Editorial
// Only letter
$('#nombreEditorial, #selloEditorial').keyup(function () {
    var letter = $(this).val();
    var allow = letter.replace(/[^a-zA-ZáéíóúñÑ0-9 ]/g, '');
    $(this).val(allow);

    // Validar después del reemplazo
    if ($(this).val().trim() === '') {
        $(this).removeClass('is-valid').addClass('is-invalid');
    } else {
        $(this).removeClass('is-invalid').addClass('is-valid');
    }
});

// 18 Prevent to change the editor's prefijo
$('#editorPrefijo, #userPassword').mousedown((e) => {
    if (e.target.baseURI.includes('/editor/')) {
        e.preventDefault();
        swal('Error', 'No es posible editar o cambiar los prefijos asignados a los editores ni sus contraseñas.', 'error');
    }
})

// 19 Boostrap's Spinner to sending email
$('#btn-accept').click((e) => {
    if (validateAll()) {
        $("#preloader").css('animation', 'preloader_forever 1.2s forwards infinite');
    }
})

// 20 Ajax Calls to Spinner Loading
jQuery(function ($) {
    // Flag para controlar el spinner
    let spinnerTriggered = false;

    // Evento de ajaxSend asociado solo a solicitudes AJAX que provienen del botón con clase 'ajax-submit-btn' para
    // mostrar el spinner y el ´Espere...´
    $(document).ajaxSend(function (event, xhr, settings) {
        if (spinnerTriggered) {
            $(".spinner-border").fadeIn(500);

            let loading = `<span class="spinner-border spinner-border-sm" aria-hidden="true"></span>&nbsp;
                           <span role="status">Espere...</span>`;
            $("#btn-add").html(loading);
        }
    });

    $("#btn-add").click(function (event) {
        let val = validateAll();
        if (val) {
            // Activa el flag
            spinnerTriggered = true;
            $.ajax({
                type: 'GET'
            }).fail(() => {
                // Resetea el flag en caso de error
                spinnerTriggered = false;
            });
        }
    });

    // Código para manejar el cambio de provincias y la actualización de municipios
    $('#editorProvincia').change(function () {
        var provinciaId = $(this).val();
        if (provinciaId) {
            $.ajax({
                url: 'http://127.0.0.1:8000/get-municipios/',
                data: {
                    'provincia_id': provinciaId
                },
                dataType: 'json',
                success: function (data) {
                    var municipioSelect = $('#editorMunicipio');
                    municipioSelect.empty();
                    // Si la provincia es Isla de la Juventud
                    if (provinciaId === '15') {
                        municipioSelect.append('<option value="162" hidden>Municipio Especial</option>');
                    } else {
                        municipioSelect.append('<option value="" hidden>Municipio</option>');
                    }

                    $.each(data, function (index, municipio) {
                        municipioSelect.append('<option value="' + municipio.id + '">' + municipio.nombre + '</option>');
                    });
                }
            });
        } else {
            $('#editorMunicipio').empty();
            $('#editorMunicipio').append('<option value="" hidden>Municipio</option>');
        }
    });
});

// 21 Validate Adress
$('#address').keyup(function () {
        var value = $(this).val();
        var allow = value.replace(/[^a-zA-ZáéíóúñÑ./:,#0-9 ]/g, '');
        $(this).val(allow);

        // Validar después del reemplazo
        if ($(this).val().trim() === '') {
            $(this).removeClass('is-valid').addClass('is-invalid');
        } else {
            $(this).removeClass('is-invalid').addClass('is-valid');
        }
    });




var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
  return new bootstrap.Popover(popoverTriggerEl)
});


