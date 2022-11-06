function validateForm() {
    var x = document.forms["validation"]["address"].value;
    if (x == "" || x == null) {
      alert("Address must be filled out");
      return false;
    }
    var y = document.forms["validation"]["phonenmbr"].value;
    if (y == "" || y == null) {
      alert("Phone Number must be filled out");
      return false;
    }
    var z = document.forms["validation"]["email"].value;
    if (z == "" || z == null) {
      alert("Email must be filled out");
      return false;
    }
}
