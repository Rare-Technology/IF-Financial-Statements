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

function bY_to_date (date) {
  const date_split = date.split(' '); // ['Jan', 2022]
  const isodate = [date_split[1], months[date_split[0]], '01'].join('-'); // 2022-01-01
  let out = new Date(isodate); // Date Fri Dec 31 2021 19:00:00 GMT-0500 (Eastern Standard Time)
  out.setHours(out.getHours() + 5); // Date Sat Jan 01 2022 00:00:00 GMT-0500 (Eastern Standard Time)

  return out
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
           // {
           //      "text" : 'Email',
           //      action : function(e, dt, node, conf) {
           //          var data = income_table.buttons.exportData({
           //              "stripHtml" : true,
           //              "columns" : ':visible',
           //              // "modifier" : {
           //              //     "selected" : true
           //              // }
           //          });
           //          var headerArray = data.header;
           //          var rowsArray = data.body;
           //          var rowItem = '';
           //          var innerRowItem = '';
           //
           //          for (var h = 0, hen = rowsArray.length; h < hen; h++) {
           //              var innerRowsArray = rowsArray[h];
           //
           //              for (var i = 0, ien = innerRowsArray.length; i < ien; i++) {
           //                  var outerCount = [i];
           //
           //                  var checker = 'false';
           //                  for (var j = 0, jen = headerArray.length; j < ien; j++) {
           //                      if ( outerCount = [j] & checker == 'false') {
           //                          checker = 'true';
           //                          innerRowItem += headerArray[i];
           //                      }
           //                  }
           //
           //                  if (innerRowsArray[i] != '') {
           //                      innerRowItem += ': ';
           //                  }
           //
           //                  innerRowItem += innerRowsArray[i];
           //
           //                  if (innerRowsArray[i] != '') {
           //                      innerRowItem += '<br>';
           //                  }
           //
           //              };
           //
           //              innerRowItem += '<br>';
           //
           //          };
           //          $('#emailForm').modal({
           //              showClose : true,
           //              fadeDuration : 250,
           //              fadeDelay : 1.5
           //          });
           //                              // tinymce.activeEditor.execCommand('mceInsertContent', false, innerRowItem);
           //          //$("textarea#mce-content-body").val(innerRowItem);
           //      }
           //  }
         ],
         order: [[1, 'asc']],
         ordering: false,
         bPaginate: false,
         bInfo: false,
         // rowGroup: {
         //   dataSrc: 1
         // },
         searching: false,
         responsive: true,
         scrollX: true,
         scrollCollapse: true,
         // scroller: {
         //   loadingIndicator: true
         // },
         fixedColumns: {
           left: 2
         }
    });

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
         responsive: true,
         scrollX: true,
         fixedColumns: {
           left: 1
         }
    });

    // Initial column filter and removing sorting
    income_table.columns().every( function() {
      if (!(this.index() in [0,1])) {
        let min = $('#start-date').datepicker('getDate');
        let max = $('#end-date').datepicker('getDate');
        let date = bY_to_date(this.header().textContent);

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
      if (!(this.index() in  [0,1])) {
        let min = $('#start-date').datepicker('getDate');
        let max = $('#end-date').datepicker('getDate');
        let date = bY_to_date(this.header().textContent);

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
          if (!(this.index() in [0,1])) {
            let min = $('#start-date').datepicker('getDate');
            let max = $('#end-date').datepicker('getDate');
            let date = bY_to_date(this.header().textContent);

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
          if (!(this.index() in [0,1])) {
            let min = $('#start-date').datepicker('getDate');
            let max = $('#end-date').datepicker('getDate');
            let date = bY_to_date(this.header().textContent);

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
