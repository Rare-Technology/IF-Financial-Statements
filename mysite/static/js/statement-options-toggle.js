const inputStatements = document.querySelectorAll(".input-statements");
inputStatements1 = inputStatements[0];
inputStatements2 = inputStatements[1];
const statementOptions = document.querySelectorAll(".statement-option");
const table = document.querySelector(".table");

inputStatements1.addEventListener("click", function() {
  let num_checked = 0;
  inputStatements.forEach(element => num_checked = num_checked + element.checked);

  if (num_checked == 0) {
    statementOptions.forEach(element => element.disabled = true);
    // table.hidden = true;
  } else {
    statementOptions.forEach(element => element.disabled = false);
    // table.hidden = false;
  };
});

inputStatements2.addEventListener("click", function() {
  let num_checked = 0;
  inputStatements.forEach(element => num_checked = num_checked + element.checked);

  if (num_checked == 0) {
    statementOptions.forEach(element => element.disabled = true);
  } else {
    statementOptions.forEach(element => element.disabled = false);
  };
});
