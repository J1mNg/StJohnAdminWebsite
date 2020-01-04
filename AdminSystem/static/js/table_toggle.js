var tableA = document.getElementById("tableA");
var tableB = document.getElementById("tableB");

var btnA = document.getElementById("toggleA");
var btnB = document.getElementById("toggleB");

var headingA = document.getElementById("headingA")

btnA.onclick = function () {
    tableA.style.display = "table";
    tableB.style.display = "none";
    btnA.className='btn btn-primary';
    btnB.className='btn btn-secondary';
    headingA.innerHTML='Cadets who are close to next reward tier'
}
btnB.onclick = function () {
    tableA.style.display = "none";
    tableB.style.display = "table";
    btnB.className='btn btn-primary';
    btnA.className='btn btn-secondary';
    headingA.innerHTML='Cadets who have yet to recieve their rewards'
}
