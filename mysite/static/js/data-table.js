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
    // DataTables initialisation
    let table = $('#income-table').DataTable({
         dom: 'Bfrtip',
         buttons: [
             'excel', 'pdf', 'print'
         ],
         order: [[1, 'asc']],
         rowGroup: {
           dataSrc: 1
         },
         responsive: true
    });

    $('#income-table').wrap("<div class='scrollTable'></div>");

    // Initial column filter
    table.columns().every( function() {
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

    // Refilter the table
    $('#start-date, #end-date').on('change', function () {
        table.columns().every( function() {
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
