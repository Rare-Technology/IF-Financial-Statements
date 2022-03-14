let this_month = new Date();
this_month.setDate(1);
this_month.setHours(0, 0, 0, 0); // HH:mm:ss:ms = 00:00:00:00
let six_months_ago = new Date(this_month);
six_months_ago.setMonth(this_month.getMonth() - 6);

$('.input-daterange').datepicker({
  format: "M yyyy",
  startView: 1,
  minViewMode: 1,
  maxViewMode: 2,
  autoclose: true
});

$('#start-date').datepicker('setDate', six_months_ago);
$('#end-date').datepicker('setDate', this_month);

const options = { month: 'long', year: 'numeric'};
let start_date_text = six_months_ago.toLocaleDateString('en-US', options); // will have to change this when localizing
let end_date_text = this_month.toLocaleDateString('en-US', options);



document.querySelectorAll('.start-date-display').forEach(e => e.innerText = start_date_text);
document.querySelectorAll('.end-date-display').forEach(e => e.innerText = end_date_text);
