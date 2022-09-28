var csvExport = csvExport || {};
csvExport.util = csvExport.util || {};

/// <summary>
/// Generates JSON from HTML Table and sets Value of Hidden Input to the Result
/// </summary>
///
/// <param name="selector">jQuery Selector Used to Target HTML Table</param>
/// <param name="excludeHeaders">Array that identifies columns to remove from output</param>
/// <param name="hiddenJsonElementId">Specifies a different targeted hidden input to store json</param>
csvExport.util.convertTableToJson = {
    convert: function (selector, excludeHeaders, hiddenJsonElementId) {
        if (!hiddenJsonElementId) {
            hiddenJsonElement = "#jsonString";
        } else {
            hiddenJsonElement = hiddenJsonElementId;
        }

        var jsonString = '[';
        var outputArray = [];
        $(selector + ' tbody tr').each(function (item) {
            if ($(this)[0].rowIndex !== 0) {
                children = $(this).children();
                var inputArray = [];
                children.each(function () {
                    $th = $(this).closest('table').find('th').eq($(this).index()).text().trim();
                    if ($th !== "" && excludeHeaders.indexOf($th) === -1) {
                        inputArray.push('"' + $th + '":"' + $(this).text().replace(/(\r\n|\n|\r)/gm, "").replace(/ +(?= )/g, '').replace(/"/g, '\'') + '"');
                    } else {
                        return;
                    }
                });
                outputArray.push('{' + inputArray.join(',') + '}');
            }
        });
        jsonString += outputArray.join(",") + ']';

        $(hiddenJsonElement).val(jsonString);
        

        jsonString = [];
    },
    /// <summary>
    /// Creates CSV File from Json String and Initiates Download
    /// </summary>
    ///
    /// <param name="json">Raw Json</param>
    /// <param name="title">File Name and Title that Appears in the CSV</param>
    /// <param name="headers">Optional Headers to Include in the CSV file. i.e. "Date Exported"</param>
    /// <param name="label">Optional Include Column Headers</param>
    exportExcel: function (json, title, headers, showColumnHeaders) {
        var data = typeof json != 'object' ? JSON.parse(json) : json;
        var exportCSV = '';
        // exportCSV += title + '\r\n\n';

        headers.forEach(function (header) {
            exportCSV += header + '\r\n';
        });
        // exportCSV += '\r\n';

        if (showColumnHeaders) {
            var header = "";
            for (var idx in data[0]) {
                header += idx + ',';
            }
            header = header.slice(0, -1);
            exportCSV += header + '\r\n';
        }

        for (var i = 0; i < data.length; i++) {
            var row = "";
            for (var index in data[i]) {
                row += '"' + data[i][index] + '",';
            }
            row.slice(0, row.length - 1);
            exportCSV += row + '\r\n';
        }

        if (exportCSV === '') {
            console.error("Invalid data");
            return;
        }
        var fileName = title.replace(/ /g, "_");
        
        var ua = window.navigator.userAgent;
        
        if(ua.indexOf('MSIE ') > 0 || ua.indexOf('Trident/') > 0 || ua.indexOf('Edge/') > 0){
            var blob = new Blob([exportCSV],{type: "text/csv;charset=utf-8"});
            navigator.msSaveBlob(blob, fileName + ".csv")
        } else {
            var uri = 'data:text/csv;charset=utf-8,' + encodeURI(exportCSV);
            var link = document.createElement("a");
            link.href = uri;
            link.style = "visibility:hidden";
            link.download = fileName + ".csv";

            document.body.appendChild(link);

            link.click();

            document.body.removeChild(link);
        }
    }
}