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
        doc.save(config.config.title);
    }
};

const user_name = $('#user-name').text()

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
             title: "Income Statement for " + user_name,
             className: "btn btn-outline-dark"
           },
           {
             extend: 'jspdf',
             config: {
               title: "Income Statement for " + user_name
             },
             className: "btn btn-outline-dark"
           },
           {
             extend: 'print',
             text: $('#print-text').text(),
             title: "Income Statement for " + user_name,
             exportOptions: {
               columns: [1, ':visible']
             },
             className: "btn btn-outline-dark"
           },
         ],
         // order: [[1, 'asc']],
         ordering: false,
         bPaginate: false,
         bInfo: false,
         // rowGroup: {
         //   dataSrc: 1
         // },
         searching: false,
         responsive: true,
         scrollX: true,
         // scrollCollapse: true,
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
             title: "Cash Flow Statement for " + user_name,
             className: "btn btn-outline-dark"
           },
           {
             extend: 'jspdf',
             config: {
               title: "Cash Flow Statement for " + user_name,
             },
             className: "btn btn-outline-dark"
           },
           {
             extend: 'print',
             text: $('#print-text').text(),
             title: "Cash Flow Statement for " + user_name,
             exportOptions: {
               columns: ':visible'
             },
             className: "btn btn-outline-dark"
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
        max.setMonth(max.getMonth() + 1);
        max.setDate(0);
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
      if (!(this.index() in  [0])) {
        let min = $('#start-date').datepicker('getDate');
        let max = $('#end-date').datepicker('getDate');
        max.setMonth(max.getMonth() + 1);
        max.setDate(0);
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
            max.setMonth(max.getMonth() + 1);
            max.setDate(0);
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
          if (!(this.index() in [0])) {
            let min = $('#start-date').datepicker('getDate');
            let max = $('#end-date').datepicker('getDate');
            max.setMonth(max.getMonth() + 1);
            max.setDate(0);
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

    // Remove dt-button class from button elements so bootstrap styling can show
    document.querySelectorAll('.dt-button').forEach(btn => btn.classList.remove("dt-button"));

    // Add an email button that functions as a form POST button, separate from dataTables.js functionalities
    let income_email_button_html = '<input id="income-submit" name="income-submit" class="btn btn-outline-dark" type="submit" form="dates-form" value="Email"></input>';
    let cashflow_email_button_html = '<input id="cashflow-submit" name="cashflow-submit" class="btn btn-outline-dark" type="submit" form="dates-form" value="Email"></input>';
    let income_button_container = document.querySelector('#income-table_wrapper').querySelector('.dt-buttons');
    let cashflow_button_container = document.querySelector('#cashflow-table_wrapper').querySelector('.dt-buttons');
    income_button_container.insertAdjacentHTML('beforeend', income_email_button_html);
    cashflow_button_container.insertAdjacentHTML('beforeend', cashflow_email_button_html);
});

// TODO use this function in template to get the DataTable data and pass it
// to a form. Then have export options use views with POST data.
function getTableData(table) {
  return table.buttons.exportData({
    columns: ':visible'
  });
}
