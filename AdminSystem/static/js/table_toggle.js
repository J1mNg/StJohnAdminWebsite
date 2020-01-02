var tableA = document.getElementById("tableA");
var tableB = document.getElementById("tableB");

var btnA = document.getElementById("toggleA");
var btnB = document.getElementById("toggleB");

btnA.onclick = function () {
    tableA.style.display = "table";
    tableB.style.display = "none";
}
btnB.onclick = function () {
    tableA.style.display = "none";
    tableB.style.display = "table";
}
