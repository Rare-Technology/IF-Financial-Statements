let today = new Date();
monthAgo = new Date(today - 1000*6*60*60*24*30); // subtract 6 month's worth of milliseconds

document.querySelector("#end-date").valueAsDate = today;
document.querySelector("#start-date").valueAsDate = monthAgo;

const options = { month: 'long', year: 'numeric'};
let start_date_text = monthAgo.toLocaleDateString('en-US', options); // will have to change this when localizing
let end_date_text = today.toLocaleDateString('en-US', options);

document.querySelectorAll('.start-date-display').forEach(e => e.innerText = start_date_text);
document.querySelectorAll('.end-date-display').forEach(e => e.innerText = end_date_text);
