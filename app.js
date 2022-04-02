//bug: takes 2 presses to display results initially

function submitForm() {
    nameValue = document.getElementById("searchTerm").value;

    //capitalize each letter of a new word
    nameValue = nameValue.replace(/(^\w{1})|(\s+\w{1})/g, letter => letter.toUpperCase());

    document.getElementById("display-results").innerHTML = "You wanted games like: " + "<u>" + nameValue + "</u>" + "<br><br>" + "<h4> Check out the following titles: </h4>";

    location.href = "#page-3";

    function arrayToTable(tableData) {
        var table = $('<table></table>');
        $(tableData).each(function (i, rowData) {
            var row = $('<tr></tr>');
            $(rowData).each(function (j, cellData) {
                if (cellData == nameValue) {
                    row.append($('<td>' + rowData[1] + '</td>'));
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
            var table = arrayToTable(Papa.parse(data).data); // convert parse object to table
            table = table.eq(0).text(); // get text value of table 
            table = table.replaceAll(/[\[\]"']+/g, ''); // replace brackets and quotations 
            table = "<ul><li>" + table.replaceAll(",", '<li>')+"</ul>"; // create an unordered list display

            if ($('#game-list').length === 0) // append if you haven't built the table yet
                $('#game-list').append(table);
            else
                $('#game-list').replaceWith("<h4>" + table + "<\h4>");
        }
    });
}