let today = new Date();
monthAgo = new Date(today - 1000*60*60*24*30); // subtract a month's worth of milliseconds

document.querySelector("#end-date").valueAsDate = today;
document.querySelector("#start-date").valueAsDate = monthAgo;
