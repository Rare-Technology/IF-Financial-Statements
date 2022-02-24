let minDate, maxDate;

// Custom filtering function which will search data in column four between two values
$.fn.dataTable.ext.search.push(
    function( settings, data, dataIndex ) {
        let min = new Date($('#start-date').val());
        let max = new Date($('#end-date').val());
        let date = new Date(data[0]);

        if (
            ( min === null && max === null ) ||
            ( min === null && date <= max ) ||
            ( min <= date   && max === null ) ||
            ( min <= date   && date <= max )
        ) {
            return true;
        }
        return false;
    }
);

$(document).ready(function() {
    // Create date inputs


    // DataTables initialisation
    let table = $('#income-table').DataTable({
         dom: 'Bfrtip',
         buttons: [
             'excel', 'pdf', 'print'
         ]
    });

    // Refilter the table
    $('#start-date, #end-date').on('change', function () {
        table.draw();
    });
});
