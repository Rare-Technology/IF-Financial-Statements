



// $('#start-date').datepicker({
//   format: "mm-yyyy",
//   startView: "months",
//   minViewMode: "months"
// });
//
// $('#end-date').datepicker({
//   format: "mm-yyyy",
//   startView: "months",
//   minViewMode: "months"
// });
//
// function saveMyDate(inst) {
//     inst.selectedDay = 1;
//     inst.input.data('year', inst.selectedYear);
//     inst.input.data('month', inst.selectedMonth);
//     inst.input.data('day', inst.selectedDay );
//
//     var date = new Date(inst.selectedYear, inst.selectedMonth, inst.selectedDay);
//     inst.input.datepicker('setDate', date );
//     formatDate(inst, date);
//     inst.input.data('date-setted', true);
// };
//
// function setMyDate(inst) {
//     var dateSetted = inst.input.data('date-setted');
//
//     if (dateSetted == true) {
//         var year = inst.input.data('year');
//         var month = inst.input.data('month');
//         var day = inst.input.data('day');
//
//         var date = new Date(year, month, day);
//         inst.input.datepicker('setDate', date );
//     };
// };
//
// function formatDate(inst, date) {
//     var formattedDate = $.datepicker.formatDate('MM - yy', date);
//     inst.input.val(formattedDate);
// };
