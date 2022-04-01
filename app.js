function submitForm(){
    var nameValue = document.getElementById("searchTerm").value;
    //bug: takes 2 presses to display results initially

    document.getElementById("display-results").innerHTML = nameValue;
    location.href = "#page-3";

    
}