const inputStatements = document.querySelectorAll(".input-statements");
const incomeCheck = inputStatements[0];
const cashflowCheck = inputStatements[1];
const viewStatements = document.querySelector("#view-statements");
const statementOptions = document.querySelectorAll(".statement-option"); // may not need this, except for email
const incomeTable = document.querySelector("#income-div");
const cashflowTable = document.querySelector("#cashflow-div");

// Create two event listeners to enable statement-option (email btn) when eiter input is checked.
// Disable if both are not checked
// First event listener
incomeCheck.addEventListener("click", function() {
  let num_checked = 0;
  inputStatements.forEach(element => num_checked = num_checked + element.checked);

  if (num_checked == 0) {
    statementOptions.forEach(element => element.disabled = true);
  } else {
    statementOptions.forEach(element => element.disabled = false);
  };

  // if (!inputStatements1.checked) {
  //   catchesTable.hidden = true;
  // };
});

// Second event listener (uncomment when reimplementing email button)
cashflowCheck.addEventListener("click", function() {
  let num_checked = 0;
  inputStatements.forEach(element => num_checked = num_checked + element.checked);

  if (num_checked == 0) {
    statementOptions.forEach(element => element.disabled = true);
  } else {
    statementOptions.forEach(element => element.disabled = false);
  };
});

viewStatements.addEventListener("click", function() {
  if (incomeCheck.checked) {
    incomeTable.hidden = false;
  } else {
    incomeTable.hidden = true;
  };
  if (cashflowCheck.checked) {
    cashflowTable.hidden = false;
  } else {
    cashflowTable.hidden = true;
  };
});
