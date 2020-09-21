var number1Tag = document.getElementById("number-1");
var number2Tag = document.getElementById("number-2");
var resultTag = document.getElementById("result");
var addButton = document.getElementById("add");

addButton.addEventListener("click", (e) => {
    var num1 = parseInt(number1Tag.value, 10);
    var num2 = parseInt(number2Tag.value, 10);
    resultTag.innerText = String(num1 + num2);
    // Uncomment below to fail all test cases
    // resultTag.innerText = String("Failed");
})