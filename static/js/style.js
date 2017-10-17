"use strict";

window.onload = function(){
var tbody = document.getElementsByTagName("tbody");

for (var i = 0, row; row = tbody[0].rows[i]; i++) {
   for (var j = 0, col; col = row.cells[j]; j++) {
       var mustbe = parseInt(row.cells[3].innerHTML);
       var total = parseInt(row.cells[1].innerHTML)
                 + parseInt(row.cells[2].innerHTML);
       if (total < mustbe) {
           row.style.color = "#db4747";
       }
   }
}
};

