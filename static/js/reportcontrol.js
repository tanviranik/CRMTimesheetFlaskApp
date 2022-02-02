var minFontSize = 12;
var maxFontSize = 26;

function zoomIn() {
    // finding the current computed fontSize of the <body> element, parsing it
    // as a float (though parseInt() would be just as safe, really):
    var titlefontsize = $('.report-title').css("font-size");
    var tablefontsize = $('.table-report').css("font-size");
    var titlefontsizeArr = titlefontsize.match(/[a-zA-Z]+|[0-9]+/g);
    var tablefontsizeArr = tablefontsize.match(/[a-zA-Z]+|[0-9]+/g);
    // if the currentFontSize is less than the specified max:
    if (parseInt(titlefontsizeArr[0]) < maxFontSize) {
        // let newsize = (parseInt(titlefontsizeArr[0]) + 2) + titlefontsizeArr[1];        
        $('.report-title').css("font-size", (parseInt(titlefontsizeArr[0]) + 2) + titlefontsizeArr[1]);
        $('.table-report').css("font-size", (parseInt(tablefontsizeArr[0]) + 2) + tablefontsizeArr[1]);
    }
  }
  
  function zoomOut() {
    var titlefontsize = $('.report-title').css("font-size");
    var tablefontsize = $('.table-report').css("font-size");
    var titlefontsizeArr = titlefontsize.match(/[a-zA-Z]+|[0-9]+/g);
    var tablefontsizeArr = tablefontsize.match(/[a-zA-Z]+|[0-9]+/g);
    if (parseInt(titlefontsizeArr[0]) > minFontSize) {
        // let newsize = (parseInt(valueArr[0]) - 2) + valueArr[1];
        $('.report-title').css("font-size", (parseInt(titlefontsizeArr[0]) - 2) + titlefontsizeArr[1]);
        $('.table-report').css("font-size", (parseInt(tablefontsizeArr[0]) - 2) + tablefontsizeArr[1]);
    }
  }

  const ExporttoExcel = function(reportname) {
    let file = new Blob([$('#print-area').html()], {type:"application/vnd.ms-excel"});
    reportname = reportname + '.xls';
    let url = URL.createObjectURL(file);
    let a = $("<a />", {
        href: url,
        download: reportname
    }).appendTo("body").get(0).click();
  };