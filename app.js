d3.csv("mainFile.csv").then(function (data) {
  // console.log(data);

  var games = data;

  var button = d3.select("#button");

  var form = d3.select("#form");

  button.on("click", runEnter);
  form.on("submit", runEnter);

  function runEnter() {
    d3.select("tbody").html("")
    d3.selectAll("p").classed('noresults', true).html("")
    d3.event.preventDefault();
    
    var inputElement = d3.select("#user-input");
    var inputValue = inputElement.property("value").toLowerCase().trim();

    // console.log(inputValue.length);
    // console.log(games);
    if (inputValue.length < 5){
      d3.select("p").classed('noresults2', true).html("<center><strong>Please try using more than 4 characters to avoid too many results!</strong>")
      inputValue = "Something to give no results"
    }
    var filteredData = games.filter(movies => movies.actors.toLowerCase().trim().includes(inputValue));
    // console.log(filteredData.length)
    if (filteredData.length === 0 && inputValue !== "Something to give no results"){
      d3.select("p").classed('noresults', true).html("<center><strong>No results. Please check your spelling!</strong>")
    }
    output = filteredData

    

});