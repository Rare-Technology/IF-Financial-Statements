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

let pdf_blob = new Blob([doc.output()], {type: 'application/pdf'});

if (textFileUrl !== null) {
  window.URL.revokeObjectURL(pdf_blob);
}

let pdf_url = window.URL.createObjectURL(pdf_blob);
