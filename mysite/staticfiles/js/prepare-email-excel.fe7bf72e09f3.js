$('#income-table').DataTable().button(0).action(function ( e, dt, button, config ) {
		this.processing( true );

		var that = this;
		var rowPos = 0;
		var dataStartRow, dataEndRow;
		var getXml = function ( type ) {
			var str = excelStrings[ type ];

			//str = str.replace( /xmlns:/g, 'xmlns_' ).replace( /mc:/g, 'mc_' );

			return $.parseXML( str );
		};
		var rels = getXml('xl/worksheets/sheet1.xml');
		var relsGet = rels.getElementsByTagName( "sheetData" )[0];

		var xlsx = {
			_rels: {
				".rels": getXml('_rels/.rels')
			},
			xl: {
				_rels: {
					"workbook.xml.rels": getXml('xl/_rels/workbook.xml.rels')
				},
				"workbook.xml": getXml('xl/workbook.xml'),
				"styles.xml": getXml('xl/styles.xml'),
				"worksheets": {
					"sheet1.xml": rels
				}

			},
			"[Content_Types].xml": getXml('[Content_Types].xml')
		};

		var data = dt.buttons.exportData( config.exportOptions );
		var currentRow, rowNode;
		var addRow = function ( row ) {
			currentRow = rowPos+1;
			rowNode = _createNode( rels, "row", { attr: {r:currentRow} } );

			for ( var i=0, ien=row.length ; i<ien ; i++ ) {
				// Concat both the Cell Columns as a letter and the Row of the cell.
				var cellId = createCellPos(i) + '' + currentRow;
				var cell = null;

				// For null, undefined of blank cell, continue so it doesn't create the _createNode
				if ( row[i] === null || row[i] === undefined || row[i] === '' ) {
					if ( config.createEmptyCells === true ) {
						row[i] = '';
					}
					else {
						continue;
					}
				}

				var originalContent = row[i];
				row[i] = typeof row[i].trim === 'function'
					? row[i].trim()
					: row[i];

				// Special number formatting options
				for ( var j=0, jen=_excelSpecials.length ; j<jen ; j++ ) {
					var special = _excelSpecials[j];

					// TODO Need to provide the ability for the specials to say
					// if they are returning a string, since at the moment it is
					// assumed to be a number
					if ( row[i].match && ! row[i].match(/^0\d+/) && row[i].match( special.match ) ) {
						var val = row[i].replace(/[^\d\.\-]/g, '');

						if ( special.fmt ) {
							val = special.fmt( val );
						}

						cell = _createNode( rels, 'c', {
							attr: {
								r: cellId,
								s: special.style
							},
							children: [
								_createNode( rels, 'v', { text: val } )
							]
						} );

						break;
					}
				}

				if ( ! cell ) {
					if ( typeof row[i] === 'number' || (
						row[i].match &&
						row[i].match(/^-?\d+(\.\d+)?([eE]\-?\d+)?$/) && // Includes exponential format
						! row[i].match(/^0\d+/) )
					) {
						// Detect numbers - don't match numbers with leading zeros
						// or a negative anywhere but the start
						cell = _createNode( rels, 'c', {
							attr: {
								t: 'n',
								r: cellId
							},
							children: [
								_createNode( rels, 'v', { text: row[i] } )
							]
						} );
					}
					else {
						// String output - replace non standard characters for text output
						var text = ! originalContent.replace ?
							originalContent :
							originalContent.replace(/[\x00-\x09\x0B\x0C\x0E-\x1F\x7F-\x9F]/g, '');

						cell = _createNode( rels, 'c', {
							attr: {
								t: 'inlineStr',
								r: cellId
							},
							children:{
								row: _createNode( rels, 'is', {
									children: {
										row: _createNode( rels, 't', {
											text: text,
											attr: {
												'xml:space': 'preserve'
											}
										} )
									}
								} )
							}
						} );
					}
				}

				rowNode.appendChild( cell );
			}

			relsGet.appendChild(rowNode);
			rowPos++;
		};

		if ( config.customizeData ) {
			config.customizeData( data );
		}

		var mergeCells = function ( row, colspan ) {
			var mergeCells = $('mergeCells', rels);

			mergeCells[0].appendChild( _createNode( rels, 'mergeCell', {
				attr: {
					ref: 'A'+row+':'+createCellPos(colspan)+row
				}
			} ) );
			mergeCells.attr( 'count', parseFloat(mergeCells.attr( 'count' ))+1 );
			$('row:eq('+(row-1)+') c', rels).attr( 's', '51' ); // centre
		};

		// Title and top messages
		var exportInfo = dt.buttons.exportInfo( config );
		if ( exportInfo.title ) {
			addRow( [exportInfo.title], rowPos );
			mergeCells( rowPos, data.header.length-1 );
		}

		if ( exportInfo.messageTop ) {
			addRow( [exportInfo.messageTop], rowPos );
			mergeCells( rowPos, data.header.length-1 );
		}


		// Table itself
		if ( config.header ) {
			addRow( data.header, rowPos );
			$('row:last c', rels).attr( 's', '2' ); // bold
		}

		dataStartRow = rowPos;

		for ( var n=0, ie=data.body.length ; n<ie ; n++ ) {
			addRow( data.body[n], rowPos );
		}

		dataEndRow = rowPos;

		if ( config.footer && data.footer ) {
			addRow( data.footer, rowPos);
			$('row:last c', rels).attr( 's', '2' ); // bold
		}

		// Below the table
		if ( exportInfo.messageBottom ) {
			addRow( [exportInfo.messageBottom], rowPos );
			mergeCells( rowPos, data.header.length-1 );
		}

		// Set column widths
		var cols = _createNode( rels, 'cols' );
		$('worksheet', rels).prepend( cols );

		for ( var i=0, ien=data.header.length ; i<ien ; i++ ) {
			cols.appendChild( _createNode( rels, 'col', {
				attr: {
					min: i+1,
					max: i+1,
					width: _excelColWidth( data, i ),
					customWidth: 1
				}
			} ) );
		}

		// Workbook modifications
		var workbook = xlsx.xl['workbook.xml'];

		$( 'sheets sheet', workbook ).attr( 'name', _sheetname( config ) );

		// Auto filter for columns
		if ( config.autoFilter ) {
			$('mergeCells', rels).before( _createNode( rels, 'autoFilter', {
				attr: {
					ref: 'A'+dataStartRow+':'+createCellPos(data.header.length-1)+dataEndRow
				}
			} ) );

			$('definedNames', workbook).append( _createNode( workbook, 'definedName', {
				attr: {
					name: '_xlnm._FilterDatabase',
					localSheetId: '0',
					hidden: 1
				},
				text: _sheetname(config)+'!$A$'+dataStartRow+':'+createCellPos(data.header.length-1)+dataEndRow
			} ) );
		}

		// Let the developer customise the document if they want to
		if ( config.customize ) {
			config.customize( xlsx, config, dt );
		}

		// Excel doesn't like an empty mergeCells tag
		if ( $('mergeCells', rels).children().length === 0 ) {
			$('mergeCells', rels).remove();
		}

		var jszip = _jsZip();
		var zip = new jszip();
		var zipConfig = {
			type: 'blob',
			mimeType: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
		};

		_addToZip( zip, xlsx );

		return zip
});
