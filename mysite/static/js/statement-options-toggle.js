const inputStatements = document.querySelectorAll(".input-statements");
const inputStatements1 = inputStatements[0];
const inputStatements2 = inputStatements[1];
const viewStatements = document.querySelector("#view-statements");
const statementOptions = document.querySelectorAll(".statement-option");
const catchesTable = document.querySelector("#catches-div");

inputStatements1.addEventListener("click", function() {
  let num_checked = 0;
  inputStatements.forEach(element => num_checked = num_checked + element.checked);

  if (num_checked == 0) {
    statementOptions.forEach(element => element.disabled = true);
  } else {
    statementOptions.forEach(element => element.disabled = false);
  };

  if (!inputStatements1.checked) {
    catchesTable.hidden = true;
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

viewStatements.addEventListener("click", function() {
  if (inputStatements1.checked) {
    catchesTable.hidden = false;
  };
});
