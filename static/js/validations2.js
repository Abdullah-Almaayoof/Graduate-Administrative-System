function validateForm() {
    var x = document.forms["validation"]["lname"].value;
    if (x == "" || x == null) {
      alert("Last name must be filled out");
      return false;
    }
    var y = document.forms["validation"]["fname"].value;
    if (y == "" || y == null) {
      alert("First name must be filled out");
      return false;
    }
    var z = document.forms["validation"]["address"].value;
    if (z == "" || z == null) {
      alert("Address must be filled out");
      return false;
    }
    var a = document.forms["validation"]["email"].value;
    if (a == "" || a == null) {
      alert("Email must be filled out");
      return false;
    }
    var b = document.forms["validation"]["phonenmbr"].value;
    if (b == "" || b == null) {
      alert("Phone number must be filled out");
      return false;
    }
}