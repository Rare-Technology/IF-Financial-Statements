var inputStatements = document.querySelect(".input-statements");
var inputDates = document.querySelect("#input-dates");

inputDates.addEventListener("click", function() {
  inputDates.toggleAttribute("disabled");
}
