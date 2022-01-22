var inputStatements = document.querySelector(".input-statements");
var inputDates = document.querySelector(".input-dates");

inputStatements.addEventListener("click", function() {
  inputDates.toggleAttribute("disabled");
});
