/*----------------------------------------------------
# All the script here it will extends to all the pages
* -----------------------------------------------*/

// 1) Script tp validate all inputs
function validateEmail(email){
    var regex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
    return regex.test(email);
}

function validateAll() {

    var name = $("#name").val();
    var phone = $("#phone").val();
    var email = $("#email").val();
    var age = $("#age").val();
    var gender = $("#gender").val();

    if (name == '') {
        swal("Opsss !", "Name field cannot be empty.", "error");
        return false;
    }
    else if (phone == '') {
        swal("Opsss !", "Phone field cannot be empty.", "error");
        return false;
    }
    else if (email == '') {
        swal("Opsss !", "Email field cannot be empty.", "error");
        return false;
    }
    else if (!(validateEmail(email))) {
        swal("Opsss !", "Put a valid email address.", "error");
        return false;
    }
    else if (age == '') {
        swal("Opsss !", "Age field cannot be empty.", "error");
        return false;
    }
    else if (age > 120) {
        swal("Denied !", "The maxinum value is 120 years.", "error");
        $("#age").val("");
        return false;
    }
    else if (gender == '') {
        swal("Opsss !", "Gender field cannot be empty.", "error");
        return false;
    }
    else {
        return true;
    }
}

$("#btn-add").bind("click", validateAll);

// 2) Script (Name field) only letter is allowed
$(document).ready(function (){
    // Only letter
    jQuery('input[name="name').keyup(function () {
        var letter = jQuery(this).val();
        var allow = letter.replace(/[^a-zA-Z]/g, '');
        jQuery(this).val(allow);
    });
    //prevent starting with space
    $('#input').on("keypress", function(e) {
        if (e.which === 32 && ! this.value.length)
            e.preventDefault();
    });
});

// 3) Script to put First Letter capitalized
$("#name").keyup(function () {
    var txt = $(this).val();
    $(this).val(txt.replace(/^(.)|\s(.)/g, function ($1){return $1.toUpperCase( );}));
});

// 4) Script to lowercase input email
$(document).ready(function (){
    $('#email').keyup(function (){
        this.value = this.value.toLowerCase();
    });
});

// 5) Script to allow only numbers in AGE
$("#age").keyup(function () {
    else if(!/^[0-9]*$/.test(this.value)) {
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
    if(/^0/.text(this.value)) {
        this.value = this.value.replace(/^0/, "");
    }
});
