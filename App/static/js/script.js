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
    return passwordPattern.test(password.val());
}

function validateCI(ci) {
    let ciValue = ci.val();
    let ciPattern = /^\d{11}$/;
    return ciPattern.test(ciValue);
}

function showAlert(field, message) {
    field.addClass('is-invalid').removeClass('is-valid');
    swal("Opss!", message, "error").then(() => {
        field[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
        field.focus();
    });
}

function validateField(field, errorMessage) {
    if (field.val() === '') {
        showAlert(field, errorMessage);
        return false;
    } else {
        field.removeClass('is-invalid').addClass('is-valid');
        return true;
    }
}

function validateAll() {
    let isValid = true;

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
    let editor = $("input[name='editor']");
    let genero = $("#genero");
    let date = $("#date");
    let letra = $("input[name*='publication_letter']");
    let materia = $("#materia");
    let tema_coleccion = $("#tema_coleccion");
    let tema_numero_coleccion = $("#tema_numero_coleccion");
    let tema_tipo_publicacion = $("#tema_tipo_publicacion");
    let tema_idioma = $("#tema_idioma");

    // Validar Checks
    if (check2.length && !check2.is(':checked')) {
        showAlert(check2, "Asegúrese de leer y entender los términos y condiciones.");
        isValid = false;
    } else {
        check2.removeClass('is-invalid').addClass('is-valid');
    }

    if (check.length && !check.is(':checked')) {
        showAlert(check, "Asegúrese de leer y entender los términos y condiciones y marque la opción de 'leído'.");
        isValid = false;
    } else {
        check.removeClass('is-invalid').addClass('is-valid');
    }

    // Validar email
    if (email.val() && !validateEmail(email.val())) {
        showAlert(email, "Inserte un correo válido.");
        isValid = false;
    } else if (email.val()) {
        email.removeClass('is-invalid').addClass('is-valid');
    }

    // Validación de la contraseña
    if (password.val() && !validateFormatPassword(password)) {
        showAlert(password, 'La contraseña debe tener al menos 8 caracteres y ser alfanumérica.');
        isValid = false;
    } else if (password.val()) {
        password.removeClass('is-invalid').addClass('is-valid');
    }

    if (username.val() && password.val().includes(username.val())) {
        showAlert(password, 'La contraseña NO debe contener el nombre de usuario.');
        isValid = false;
    } else if (password.val()) {
        password.removeClass('is-invalid').addClass('is-valid');
    }

    // Validar el CI
    if (ci.val() && !validateCI(ci)){
        showAlert(ci, 'El número de carnet de identidad debe tener 11 dígitos.');
        isValid = false;
    } else if (ci.val()) {
        ci.removeClass('is-invalid').addClass('is-valid');
    }

    // Validar colaborador
    // Verificar si existen elementos con la clase select2-selection__choice
        if ($('#colaborador').length && $(".select2-selection__choice").length === 0) {
            showAlert($('#colaborador'), 'Debe seleccionar al menos un colaborador.')
            isValid=false;
        } else if (ci.val()) {
        ci.removeClass('is-invalid').addClass('is-valid');
        }

    isValid &= validateField(first_name, "Inserte su nombre.");
    isValid &= validateField(last_name, "Inserte su apellido.");
    isValid &= validateField(ci, "Inserte su Carnet de Identidad.");
    isValid &= validateField(birthday, "El campo 'Fecha de nacimiento' está vacío.");
    isValid &= validateField(idTribute, "Se ha olvidado el número de identificación tributaria.");
    isValid &= validateField(nombreEditorial, "Inserte el nombre o razón social de la Editorial.");
    isValid &= validateField(provincia, "Se ha olvidado seleccionar una provincia.");
    isValid &= validateField(municipio, "Se ha olvidado seleccionar un municipio.");
    isValid &= validateField(address, "La dirección está vacía.");
    isValid &= validateField(phone, "Inserte su número de teléfono.");
    isValid &= validateField(email, "Inserte su dirección de correo electrónico.");
    isValid &= validateField(fundacion_date, "Inserte la fecha de fundación de la Editorial.");
    isValid &= validateField(editorialActivity, "Seleccione la Actividad Principal de la Editorial.");
    isValid &= validateField(editorialNaturalezaJud, "Seleccione la Naturaleza Jurídica de la Editorial.");
    isValid &= validateField(representante_name, "Inserte el nombre del responsable de la Editorial.");
    isValid &= validateField(representante_apellido, "Inserte el apellido del responsable de la Editorial.");
    isValid &= validateField(username, "Inserte su nombre de usuario.");
    isValid &= validateField(password, "Inserte una contraseña.");
    isValid &= validateField(editorPrefijo, "Seleccione su número estimado de publicaciones por año.");

    // Validar los campos de la publicación
    isValid &= validateField(title, "Se ha olvidado el título de la publicación.");
    isValid &= validateField(genero, "Se ha olvidado de elegir un género musical para la publicación.");
    isValid &= validateField(materia, "Se ha olvidado de elegir la materia de la publicación musical.");
    isValid &= validateField(tema_coleccion, "Se ha olvidado de elegir el tema de colección de la publicación musical.");
    isValid &= validateField(tema_numero_coleccion, "Se ha olvidado de elegir el número de colección de la publicación musical.");
    isValid &= validateField(tema_tipo_publicacion, "Se ha olvidado de elegir el tipo de publicación musical.");
    isValid &= validateField(tema_idioma, "Se ha olvidado de elegir el idioma de publicación musical.");
    isValid &= validateField(editor, "Seleccione un editor.");
    isValid &= validateField(date, "Se ha olvidado de elegir la fecha de creación de la publicación musical.");

    // Validar la letra de la canción
    if (letra.val() === '' && document.querySelector('#medio_electronico') == null) {
        showAlert(letra, "Se ha olvidado la letra de la canción. Seleccione un archivo word, pdf o txt donde tenga guardada la letra de la obra musical.");
        isValid = false;
    }

    return isValid;
}

function validateFieldOnInput() {
    let field = $(this);
    if (field.val().trim() === '') {
        field.addClass('is-invalid').removeClass('is-valid');
    } else {
        field.removeClass('is-invalid').addClass('is-valid');
    }
}

$(document).ready(function () {
    $("#btn-add").click(function(event) {
        let isValid = validateAll();

        if (!isValid) {
            event.preventDefault();
        } else {
            $("#prefijo-editor, #prefijo-publicacion, #ismn").removeAttr('readonly');
            $("#form_add_publication").submit();
        }
    });

    // Manejar la validación en cambios de input y selección
    $("input, select").on("input change", validateFieldOnInput);
});


// 2) Script (Name field) only letter is allowed
$(document).ready(function (){

    // Only letter
    $('#first_name, #apellidoAutor, #nombreAutor,  #last_name, #autor, #representante_apellido, #representante_name, #siglasEditorial, #floatingInput').keyup(function () {
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
$("#autor, #first_name,#apellidoAutor,  #last_name, #representante_apellido, #representante_name, #title, #subtitle").keyup(function () {
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
            $(this).removeClass('is-valid').addClass('is-invalid');
            $(this).val('');
            return false;
        }
        else {
            $(this).removeClass('is-invalid').addClass('is-valid');
        }
    });
});

// 9) Validate exporting data
$(document).ready(function () {
    $('#floatingTextarea2').blur(function () {
        let currentDate = new Date();
        let date_input = new Date($(this).val())
        let p_error = $('#p_error')
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
$("#idTribute, #CI, #floatingInput2, #tema_numero_coleccion, #num_paginas").keyup(function () {
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
$('#nombreEditorial, #selloEditorial, #title, #tema_coleccion, #subtitle').keyup(function () {
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
$('#editorPrefijo, #userPassword, #editorial_prefijo').mousedown((e) => {
    if (e.target.baseURI.includes('/editor')) {
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

// Solo un Colapse
$(document).ready(function() {
    // Detectar cambios en los inputs de la descripción física
    $('#fisica input, #fisica select, #fisica textarea').on('input change', function() {
        if (!$('#fisica').hasClass('show')) {
            $('#fisica').collapse('show');
        }
        if ($('#electronica').hasClass('show')) {
            $('#electronica').collapse('hide');
            // Limpiar los valores de los inputs dentro del collapse de descripción electrónica
            $('#electronica input, #electronica select, #electronica textarea').val('');
        }
    });

    // Detectar cambios en los inputs de la descripción electrónica
    $('#electronica input, #electronica select').on('input change', function() {
        if (!$('#electronica').hasClass('show')) {
            $('#electronica').collapse('show');
        }
        if ($('#fisica').hasClass('show')) {
            $('#fisica').collapse('hide');
            // Limpiar los valores de los inputs dentro del collapse de descripción física
            $('#fisica input, #fisica select, #fisica textarea').val('');
        }
    });
});

// Crear Autor dinamicamente

$(document).ready(function() {
  $('#agregarAutorBtn').on('click', function() {
    var isValid = true;

    // Obtener valores de los inputs
    var nombre = $('#nombreAutor').val();
    var apellido = $('#apellidoAutor').val();
    var nacionalidad = $('#nacionalidadSelect').val();
    var rol = $('#rolSelect').val();

    // Limpiar mensajes previos y clases de error
    $('.is-invalid').removeClass('is-invalid');
    $('.invalid-feedback').remove();

    // Validar cada campo
    if (!nombre) {
      isValid = false;
      $('#nombreAutor').addClass('is-invalid');
      $('#nombreAutor').after('<div class="invalid-feedback">El nombre es requerido.</div>');
    }
    if (!apellido) {
      isValid = false;
      $('#apellidoAutor').addClass('is-invalid');
      $('#apellidoAutor').after('<div class="invalid-feedback">El apellido es requerido.</div>');
    }
    if (!nacionalidad || nacionalidad === 'Nacionalidad') {
      isValid = false;
      $('#nacionalidadSelect').addClass('is-invalid');
      $('#nacionalidadSelect').after('<div class="invalid-feedback">La nacionalidad es requerida.</div>');
    }
    if (!rol || rol === 'Rol') {
      isValid = false;
      $('#rolSelect').addClass('is-invalid');
      $('#rolSelect').after('<div class="invalid-feedback">El rol es requerido.</div>');
    }

    // Si todos los campos son válidos, enviar la solicitud AJAX
    if (isValid) {
      $.ajax({
        type: 'POST',
        url: $('#autorForm').attr('action'),  // URL from the form's action attribute
        data: {
          'nombre': nombre,
          'apellido': apellido,
          'nacionalidad': nacionalidad,
          'rol': rol,
          'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val()  // CSRF token
        },
        success: function(data) {
          // Lógica de éxito, por ejemplo, cerrar el modal y limpiar el formulario
          $('#autoresModal').modal('hide');
          $('#autorForm')[0].reset();
          var newAuthorHTML = `
                    <li class="select2-selection__choice" title="${data.nombre} ${data.apellido}">
                        <span class="select2-selection__choice__remove" role="presentation">×</span>
                        ${data.nombre} ${data.apellido}
                    </li>
                `;
            $('.select2-selection__rendered .select2-search').before(newAuthorHTML);
        },
        error: function(response) {
          // Lógica de error
          console.log(response);
        }
      });
    }
  });
});

// Validate Editor
$(document).ready(function () {
    // Manejar el evento blur del campo editor
    $("input[name='editor']").change(function() {
        // Obtener el valor del elemento prefijo-publicacion
        let prefijoPublicacion = $("#prefijo-publicacion").val();

        // Si el valor está vacío, lanzar una alerta
        if (!prefijoPublicacion) {
            $("input[name='editor']").val('');
            swal('Error', 'El campo editor no coincide con ningún editor registrado, revise.', 'error');
        }
    });
});


var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
  return new bootstrap.Popover(popoverTriggerEl)
});


