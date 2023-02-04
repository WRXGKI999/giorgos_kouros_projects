
var button = document.getElementById('submit');
button.onclick = function validatePass() {
    var password = document.getElementById('cl_password');
    var confirm_pass = document.getElementById('cl_confirm_password');
    if(password.value != confirm_pass.value) {
        alert("Passwords did not match, Try Again");
        returnToPreviousPage();
    }
}