$.fn.dataTable.ext.buttons.jspdf = {
    text: 'PDF',
    action: function ( e, dt, node, config ) {
        // let doc = jspdf.jsPDF('l');
        // doc.autoTable({
        //   html:
        // })
        let id = '#' + dt.context[0].ntable.id;
        console.log(config.id);
    },
};
