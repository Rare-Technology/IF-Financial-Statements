

// create event listeners and update #start-date-display / #end-date-display dynamically
$('#start-date').datepicker()
  .on('changeDate', function(e) {
    const start_date = $('#start-date').datepicker('getDate');
    const options = { month: 'long', year: 'numeric'};
    start_date_text = start_date.toLocaleDateString('en-US', options); // will have to change this when localizing
    document.querySelectorAll('.start-date-display').forEach(e => e.innerText = start_date_text);
});

$('#end-date').datepicker()
    .on('changeDate', function (e) {
      const end_date = $('#end-date').datepicker('getDate');
      const options = { month: 'long', year: 'numeric'};
      end_date_text = end_date.toLocaleDateString('en-US', options); // will have to change this when localizing
      document.querySelectorAll('.end-date-display').forEach(e => e.innerText = end_date_text);
});
