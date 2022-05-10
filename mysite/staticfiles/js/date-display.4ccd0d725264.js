

// create event listeners and update #start-date-display / #end-date-display dynamically
$('#start-date').datepicker()
  .on('changeDate', function(e) {
    const start_date = $('#start-date').datepicker('getDate');
    const options = { month: 'long', year: 'numeric'};
    start_date_text = start_date.toLocaleDateString('en-US', options); // will have to change this when localizing
    document.querySelectorAll('.start-date-display').forEach(e => e.innerText = start_date_text);

    // update plots
    const end_date = $('#end-date').datepicker('getDate');

    income_x = [];
    income_y = [];
    cashflow_x = [];
    cashflow_y = [];

    for (i = 0; i < income_data.length; i++) {
      obj = income_data[i];
      isodate = bY_to_date_plot(income_data[i]['date']);
      js_date = new Date(isodate);
      if (start_date <= js_date && js_date <= end_date) {
        income_x.push(isodate);
        income_y.push(obj['Net income']);
      };
    };
    income_plot_data = [{
      x: income_x,
      y: income_y,
      type: 'bar'
    }];

    for (i = 0; i < cashflow_data.length; i++) {
      obj = cashflow_data[i];
      isodate = bY_to_date_plot(cashflow_data[i]['date']);
      js_date = new Date(isodate);
      if (start_date <= js_date && js_date <= end_date) {
        cashflow_x.push(isodate);
        cashflow_y.push(obj['Total cash from fisheries operations']);
      };
    };
    cashflow_plot_data = [{
      x: cashflow_x,
      y: cashflow_y,
      type: 'bar'
    }];

    Plotly.newPlot('income-plot', income_plot_data)
    Plotly.newPlot('cashflow-plot', cashflow_plot_data);
});

$('#end-date').datepicker()
    .on('changeDate', function (e) {
      const end_date = $('#end-date').datepicker('getDate');
      const options = { month: 'long', year: 'numeric'};
      end_date_text = end_date.toLocaleDateString('en-US', options); // will have to change this when localizing
      document.querySelectorAll('.end-date-display').forEach(e => e.innerText = end_date_text);

      // update plots
      const start_date = $('#start-date').datepicker('getDate');

      income_x = [];
      income_y = [];
      cashflow_x = [];
      cashflow_y = [];

      for (i = 0; i < income_data.length; i++) {
        obj = income_data[i];
        isodate = bY_to_date_plot(income_data[i]['date']);
        js_date = new Date(isodate);
        if (start_date <= js_date && js_date <= end_date) {
          income_x.push(isodate);
          income_y.push(obj['Net income']);
        };
      };
      income_plot_data = [{
        x: income_x,
        y: income_y,
        type: 'bar'
      }];

      for (i = 0; i < cashflow_data.length; i++) {
        obj = cashflow_data[i];
        isodate = bY_to_date_plot(cashflow_data[i]['date']);
        js_date = new Date(isodate);
        if (start_date <= js_date && js_date <= end_date) {
          cashflow_x.push(isodate);
          cashflow_y.push(obj['Total cash from fisheries operations']);
        };
      };
      cashflow_plot_data = [{
        x: cashflow_x,
        y: cashflow_y,
        type: 'bar'
      }];

      Plotly.newPlot('income-plot', income_plot_data);
      Plotly.newPlot('cashflow-plot', cashflow_plot_data);
});
