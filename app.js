function submitForm(){
    var input = document.getElementById("myform");
    var text = "";
    text = input.elements[0].value;
    window.localStorage.setItem(text);
    window.write(window.localStorage.getItem(text));
}