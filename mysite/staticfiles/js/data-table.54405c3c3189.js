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

let income_table, cashflow_table

$.fn.dataTable.ext.buttons.jspdf = {
    text: 'PDF',
    action: function ( e, dt, node, config ) {
        let doc = jspdf.jsPDF('l');
        let dt_id = '#' + dt.context[0].nTable.id;
        doc.text(config.config.title, 120, 20);
        doc.autoTable({
          styles: {halign: 'right'},
          columnStyles: {0: {halign: 'left'}},
          html: dt_id,
          horizontalPageBreak: true,
          horizontalPageBreakRepeat: 0,
          margin: {top: 30}
        })
        doc.save('table.pdf');
    }
};


$(document).ready(function() {
    // DataTables initialisation for income
    income_table = $('#income-table').DataTable({
         dom: 'Bfrtip',
         buttons: [
           {
             extend: 'excel',
             exportOptions: {
               columns: [1, ':visible']
             },
             title: "Income Statement"
           },
           {
             extend: 'jspdf',
             config: {
               title: "Income Statement"
             }
           },
           {
             extend: 'print',
             exportOptions: {
               columns: [1, ':visible']
             }
           },
           {
                "text" : 'Email',
                action : function(e, dt, node, conf) {
                    var data = income_table.buttons.exportData({
                        "stripHtml" : true,
                        "columns" : ':visible',
                        // "modifier" : {
                        //     "selected" : true
                        // }
                    });
                    var headerArray = data.header;
                    var rowsArray = data.body;
                    var rowItem = '';
                    var innerRowItem = '';

                    for (var h = 0, hen = rowsArray.length; h < hen; h++) {
                        var innerRowsArray = rowsArray[h];

                        for (var i = 0, ien = innerRowsArray.length; i < ien; i++) {
                            var outerCount = [i];

                            var checker = 'false';
                            for (var j = 0, jen = headerArray.length; j < ien; j++) {
                                if ( outerCount = [j] & checker == 'false') {
                                    checker = 'true';
                                    innerRowItem += headerArray[i];
                                }
                            }

                            if (innerRowsArray[i] != '') {
                                innerRowItem += ': ';
                            }

                            innerRowItem += innerRowsArray[i];

                            if (innerRowsArray[i] != '') {
                                innerRowItem += '<br>';
                            }

                        };

                        innerRowItem += '<br>';

                    };
                    $('#emailForm').modal({
                        showClose : true,
                        fadeDuration : 250,
                        fadeDelay : 1.5
                    });
                                        // tinymce.activeEditor.execCommand('mceInsertContent', false, innerRowItem);
                    //$("textarea#mce-content-body").val(innerRowItem);
                }
            }
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
    cashflow_table = $('#cashflow-table').DataTable({
         dom: 'Bfrtip',
         buttons: [
           {
             extend: 'excel',
             exportOptions: {
               columns: ':visible'
             },
             title: "Cash Flow Statement"
           },
           {
             extend: 'jspdf',
             config: {
               title: "Cash Flow Statement"
             }
           },
           {
             extend: 'print',
             exportOptions: {
               columns: ':visible'
             }
           }
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
      if (!this.header().textContent.includes('Type')) {
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
      if (!this.header().textContent.includes('Type')) {
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
          if (!this.header().textContent.includes('Type')) {
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
          if (!this.header().textContent.includes('Type')) {
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

// TODO use this function in template to get the DataTable data and pass it
// to a form. Then have export options use views with POST data.
function getTableData(table) {
  return table.buttons.exportData({
    columns: ':visible'
  });
}
