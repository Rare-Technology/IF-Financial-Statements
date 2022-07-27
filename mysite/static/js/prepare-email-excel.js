
const income_data = $('#income-table').DataTable().buttons.exportData()
const cashflow_data = $('#cashflow-table').DataTable().buttons.exportData()

const income_workbook = XLSX.utils.book_new();
const cashflow_workbook = XLSX.utils.book_new();

const income_worksheet = XLSX.utils.json_to_sheet(income_data.body);
const cashflow_worksheet = XLSX.utils.json_to_sheet(cashflow_data.body);

XLSX.utils.book_append_sheet(income_workbook, income_worksheet);
XLSX.utils.book_append_sheet(cashflow_workbook, cashflow_worksheet);

const income_excel_base64 = XLSX.write(income_workbook, {type: "base64", bookType: "xlsx"});
const cashflow_excel_base64 = XLSX.write(cashflow_workbook, {type: "base64", bookType: "xlsx"});

$('#income_excel_raw').val(income_excel_base64);
$('#cashflow_excel_raw').val(cashflow_excel_base64);
