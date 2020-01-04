function get_sum_html_column(colNumber) {
  let table, i, row, sum=0;
  table = document.getElementById("finance_summary_table");
  let tableBody = table.getElementsByTagName("tbody").item(0);
  let nRows = tableBody.rows.length;
  row = table.getElementsByTagName("tr");
  for (i=0; i<(nRows-1); i++) {
    let thisTrElem = tableBody.rows[i];
    let thisTdElem = thisTrElem.cells[colNumber];
    let thisTextNode = thisTdElem.childNodes.item(0);

    let thisNumber = parseFloat(thisTextNode.data);
    // if you didn't get back the value NaN (i.e. not a number), add into result
    if (!isNaN(thisNumber))
      sum += thisNumber;
  }
  table.rows[nRows-1].cells[colNumber].innerHTML=sum;
}
