
function submitForm(){
    nameValue = document.getElementById("searchTerm").value;
    //bug: takes 2 presses to display results initially

    document.getElementById("display-results").innerHTML = nameValue;
    location.href = "#page-3";

    function arrayToTable(tableData) {
        var table = $('<table></table>');
        $(tableData).each(function (i, rowData) {
            var row = $('<tr></tr>');
            
            $(rowData).each(function (j, cellData) {
              if (cellData == nameValue) {
                row.append($('<td>'+rowData[1]+'</td>'));
              }
            });
            table.append(row);
        });
        return table;
    }

    $.ajax({
        type: "GET",
        url: "mainFile.csv",
        success: function (data) {
            parsed = Papa.parse(data).data;
            $('#display-results').append(arrayToTable(Papa.parse(data).data));
        }
    });
}
