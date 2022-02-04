let minDate, maxDate;

// Custom filtering function which will search data in column four between two values
$.fn.dataTable.ext.search.push(
    function( settings, data, dataIndex ) {
        let min = minDate.val();
        let max = maxDate.val();
        let date = new Date( data[0] );
        console.log(min)
        console.log(date)
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
    minDate = new DateTime($('#start-date'), {
        format: 'MMMM Do YYYY'
    });
    maxDate = new DateTime($('#end-date'), {
        format: 'MMMM Do YYYY'
    });

    // DataTables initialisation
    let table = $('#catches').DataTable();

    // Refilter the table
    $('#start-date, #end-date').on('change', function () {
        table.draw();
    });
});
