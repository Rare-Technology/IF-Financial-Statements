start_date_input = document.querySelector('#start-date');
end_date_input = document.querySelector('#end-date');

// create event listeners and update #start-date-display / #end-date-display dynamically
start_date_input.addEventListener('change', function() {
  const start_date = new Date(start_date_input.value);
  const options = { month: 'long', year: 'numeric'};
  start_date_text = start_date.toLocaleDateString('en-US', options); // will have to change this when localizing

  document.querySelectorAll('.start-date-display').forEach(e => e.innerText = start_date_text);
});

end_date_input.addEventListener('change', function() {
  const end_date = new Date(end_date_input.value);
  const options = { month: 'long', year: 'numeric'};
  end_date_text = end_date.toLocaleDateString('en-US', options); // will have to change this when localizing

  document.querySelectorAll('.end-date-display').forEach(e => e.innerText = end_date_text);
});
