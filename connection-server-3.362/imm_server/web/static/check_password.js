function check_password() {
	var pin = document.getElementById("passwd");
	var cin = document.getElementById("confirm");

	if (pin.value != cin.value) {
		alert("passwords does not match!");
		pin.focus();
		return false;
	}
	if (pin.value.length == 0) {
		alert('password empty!');
		pin.focus();
		return false;
	}
	return true;
}
