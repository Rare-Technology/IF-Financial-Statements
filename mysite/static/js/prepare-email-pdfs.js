let income_doc = jspdf.jsPDF('l');
let cashflow_doc = jspdf.jsPDF('l');
const income_table_id = '#income-table';
const cashflow_table_id = '#cashflow-table';

income_doc.text('Income Statement', 120, 20);
income_doc.autoTable({
  styles: {halign: 'right'},
  columnStyles: {0: {halign: 'left'}},
  html: income_table_id,
  horizontalPageBreak: true,
  horizontalPageBreakRepeat: 0,
  margin: {top: 30}
})

cashflow_doc.text('Cashflow Statement', 120, 20);
cashflow_doc.autoTable({
  styles: {halign: 'right'},
  columnStyles: {0: {halign: 'left'}},
  html: cashflow_table_id,
  horizontalPageBreak: true,
  horizontalPageBreakRepeat: 0,
  margin: {top: 30}
})

let income_pdf_base64 = btoa(income_doc.output());
let cashflow_pdf_base64 = btoa(cashflow_doc.output());

$('#income_pdf_raw').val(income_pdf_base64);
$('#cashflow_pdf_raw').val(cashflow_pdf_base64);
