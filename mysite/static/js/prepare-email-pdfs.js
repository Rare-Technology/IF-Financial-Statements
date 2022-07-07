let doc = jspdf.jsPDF('l');
let income_table_id = '#income-table';
doc.text('Income Statement', 120, 20);
doc.autoTable({
  styles: {halign: 'right'},
  columnStyles: {0: {halign: 'left'}},
  html: income_table_id,
  horizontalPageBreak: true,
  horizontalPageBreakRepeat: 0,
  margin: {top: 30}
})

let pdf_base64 = btoa(doc.output());

$('#id_pdf_base64').val(pdf_base64);
