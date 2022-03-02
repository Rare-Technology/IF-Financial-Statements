const months = {
  'Jan': '01',
  'Feb': '02',
  'Mar': '03',
  'Apr': '04',
  'May': '05',
  'Jun': '06',
  'Jul': '07',
  'Aug': '08',
  'Sep': '09',
  'Oct': '10',
  'Nov': '11',
  'Dec': '12'
};

function bY_to_iso (date) {
  const date_split = date.split(' '); // ['Jan', 2022]
  const isodate = [date_split[1], months[date_split[0]], '01'].join('-');

  return isodate
}

$(document).ready(function() {
    // DataTables initialisation for income
    let income_table = $('#income-table').DataTable({
         dom: 'Bfrtip',
         buttons: [
             'excel', 'pdf', 'print'
         ],
         order: [[1, 'asc']],
         ordering: false,
         bPaginate: false,
         bInfo: false,
         rowGroup: {
           dataSrc: 1
         },
         searching: false,
         responsive: true
    });

    // add horizontal scrolling
    $('#income-table').wrap("<div class='scrollTable'></div>");

    // and now cashflow
    let cashflow_table = $('#cashflow-table').DataTable({
         dom: 'Bfrtip',
         buttons: [
             'excel', 'pdf', 'print'
         ],
         ordering: false,
         bPaginate: false,
         bInfo: false,
         searching: false,
         responsive: true
    });
    $('#cashflow-table').wrap("<div class='scrollTable'></div>");

    // Initial column filter and removing sorting
    income_table.columns().every( function() {
      if (this.header().textContent != "Date") {
        let min = new Date($('#start-date').val());
        let max = new Date($('#end-date').val());
        let isodate = bY_to_iso(this.header().textContent);
        let date = new Date(isodate);

        if (
            ( min === null && max === null ) ||
            ( min === null && date <= max ) ||
            ( min <= date   && max === null ) ||
            ( min <= date   && date <= max )
        ) {
            this.visible(true);
        } else {
            this.visible(false);
        }
      }
    });

    // and cashflow
    cashflow_table.columns().every( function() {
      if (this.header().textContent != "Date") {
        let min = new Date($('#start-date').val());
        let max = new Date($('#end-date').val());
        let isodate = bY_to_iso(this.header().textContent);
        let date = new Date(isodate);

        if (
            ( min === null && max === null ) ||
            ( min === null && date <= max ) ||
            ( min <= date   && max === null ) ||
            ( min <= date   && date <= max )
        ) {
            this.visible(true);
        } else {
            this.visible(false);
        }
      }
    });

    // Refilter the tables
    $('#start-date, #end-date').on('change', function () {
        income_table.columns().every( function() {
          if (this.header().textContent != "Date") {
            let min = new Date($('#start-date').val());
            let max = new Date($('#end-date').val());
            let isodate = bY_to_iso(this.header().textContent);
            let date = new Date(isodate);

            if (
                ( min === null && max === null ) ||
                ( min === null && date <= max ) ||
                ( min <= date   && max === null ) ||
                ( min <= date   && date <= max )
            ) {
                this.visible(true);
            } else {
                this.visible(false);
            }
          }
        });

        cashflow_table.columns().every( function() {
          if (this.header().textContent != "Date") {
            let min = new Date($('#start-date').val());
            let max = new Date($('#end-date').val());
            let isodate = bY_to_iso(this.header().textContent);
            let date = new Date(isodate);

            if (
                ( min === null && max === null ) ||
                ( min === null && date <= max ) ||
                ( min <= date   && max === null ) ||
                ( min <= date   && date <= max )
            ) {
                this.visible(true);
            } else {
                this.visible(false);
            }
          }
        });
    });
});
