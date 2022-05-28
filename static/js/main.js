$(function() {
	'use strict';
	
  $('.form-control').on('input', function() {
	  var $field = $(this).closest('.form-group');
	  if (this.value) {
	    $field.addClass('field--not-empty');
	  } else {
	    $field.removeClass('field--not-empty');
	  }
	});

});

document.getElementById('btnn').addEventListener('click',function(event){
	event.preventDefault();
	validate();});

function validate(){
var username = document.getElementById("username").value;
var password = document.getElementById("password").value;
if ( username == "admin" && password == "1234"){
window.location.href="/capture"; // Redirecting to other page.
return false;
}
else{
alert("Invalid Username or password");
}
}