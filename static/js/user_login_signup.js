console.log("loaded");

var showPassword = document.querySelector("#show-password");
var password = document.querySelector("#password");
var para = document.querySelector("#para");
password.addEventListener("keyup", pass);
function pass(e) {
  var passValue = e.target.value;
  if (passValue.length < 6 && passValue.length > 0) {
    para.innerHTML = "password must be 6 characters long";
  } else {
    para.innerHTML = "";
  }
}
function showPass() {
  if (showPassword.checked) {
    password.type = "text";
  } else {
    password.type = "password";
  }
}
