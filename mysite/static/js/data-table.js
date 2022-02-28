// Custom filtering function which will search data in column four between two values
// $.fn.dataTable.ext.search.push(
//     function( settings, data, dataIndex ) {
//         let min = new Date($('#start-date').val());
//         let max = new Date($('#end-date').val());
//         let date = new Date(data[0]);
//
//         if (
//             ( min === null && max === null ) ||
//             ( min === null && date <= max ) ||
//             ( min <= date   && max === null ) ||
//             ( min <= date   && date <= max )
//         ) {
//             return true;
//         }
//         return false;
//     }
// );

$(document).ready(function() {
    // Create date inputs


    // DataTables initialisation
    let table = $('#income-table').DataTable({
         dom: 'Bfrtip',
         buttons: [
             'excel', 'pdf', 'print'
         ],
         responsive: true
    });

    $('#income-table').wrap("<div class='scrollTable'></div>");

    table.columns().every( function() {
      if (this.header().textContent != "Date") {
        let min = new Date($('#start-date').val());
        let max = new Date($('#end-date').val());
        let date = new Date(this.header().textContent);

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
            let date = new Date(this.header().textContent);

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
