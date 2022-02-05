﻿var MessageType = {
  Success: 1,
  Failed: 2,
  Error: 3
};

$(document).ready(function () {
    $('.navbar-minimalize').on('click', function () {
        console.log('clicked');

        //$(this).find('svg.svg-inline--fa').toggleClass('fa-arrow-left fa-arrow-right');
        var button = $(this).find('svg.svg-inline--fa');
        //console.log(button);
        button.toggleClass('fa-arrow-left').toggleClass('fa-arrow-right');
    });
    var path = window.location.pathname;
    path = path.split('/')[1].toLowerCase();
    
    $('ul.metismenu > li').each(function(){
      var matchingpath = $(this).text().trim().toLowerCase();      
      if(matchingpath === path){
        $(this).find('a').addClass('active');
      }
    })
    $('.clockpicker').clockpicker();

    
});
const showloading = function(){
  $('.loading').css('display','flex');
}
const stoploading = function(){
  $('.loading').css('display','none');
};
const GetWeekStartDate = function(selecteddate){
    selectedDayStr = getcalenderformat(selecteddate);
    selectedDayArr = selecteddate.toString('en-us').split(' ');
    const daydiff = getWeekDayNo(selectedDayArr[0]) - 1;
    // set week start date as global copy
    weekstartdate = new Date(selectedDayStr);
    weekstartdate.setHours(0, 0, 0, 0);
    weekstartdate.setDate(weekstartdate.getDate() - daydiff);
    return getcalenderformat(weekstartdate);
};
const GetWeekEndDate = function(selecteddate){
    selectedDayStr = getcalenderformat(selecteddate);
    selectedDayArr = selecteddate.toString('en-us').split(' ');
    const daydiff = 7 - getWeekDayNo(selectedDayArr[0]);
    // set week start date as global copy
    weekenddate = new Date(selectedDayStr);
    weekenddate.setHours(0, 0, 0, 0);
    weekenddate.setDate(selecteddate.getDate() + daydiff);
    return getcalenderformat(weekenddate);
};
const GetStubStartDate = function(selecteddate){
    selectedDayStr = getcalenderformat(selecteddate);
    selectedDayArr = selecteddate.toString('en-us').split(' ');
    const daydiff = getReportWeekDayNo(selectedDayArr[0]) - 1;
    // set week start date as global copy
    let weekstartdate = new Date(selectedDayStr);
    weekstartdate.setHours(0, 0, 0, 0);
    weekstartdate.setDate(weekstartdate.getDate() - daydiff);
    return getcalenderformat(weekstartdate);
};
const GetSubEndDate = function(selecteddate){
    selectedDayStr = getcalenderformat(selecteddate);
    selectedDayArr = selecteddate.toString('en-us').split(' ');
    const daydiff = 7 - getReportWeekDayNo(selectedDayArr[0]);
    console.log(daydiff);
    // set week start date as global copy
    let weekenddate = new Date(selectedDayStr);
    weekenddate.setHours(0, 0, 0, 0);
    weekenddate.setDate(weekenddate.getDate() + daydiff);
    console.log(weekenddate);
    return getcalenderformat(weekenddate);
};
const calculatingWorkingHours = function(starttime, endtime) {  
    if(starttime === endtime) return '00:00';
    let starttimeArr = starttime.split(':');
    let endtimeArr = endtime.split(':');
    let carry =0;
    // let minutestr = '';
    let starthour = parseInt(starttimeArr[0]);
    let startminute = parseInt(starttimeArr[1]);
    let endhour = parseInt(endtimeArr[0]);
    let endminute = parseInt(endtimeArr[1]);    
    if((starthour > endhour) || (starthour === endhour && startminute > endminute))
      return '00:00';
    if(startminute > endminute){
        endminute = 60 + endminute;
        carry = 1;
    }
    let minutedeff = endminute - startminute;
    let hourdiff = endhour - (starthour+carry);
    let minutestr = (minutedeff < 10) ? ('0' + minutedeff) : minutedeff;
    let hourdiffstr = (hourdiff < 10) ? ('0' + hourdiff) : hourdiff;
    return hourdiffstr + ':' + minutestr;
}
const calculateTotalHours = function(paymentAmount, hourlyRate){
  if(paymentAmount === NaN || paymentAmount === '' || paymentAmount === 0 || hourlyRate === NaN || hourlyRate === '' ||hourlyRate === 0) return "00:00";
  let total_hours_decimal = paymentAmount/hourlyRate;
  // Separate the int from the decimal part
  var hour = Math.floor(total_hours_decimal);
  var decpart = total_hours_decimal - hour;
  var min = 1 / 60;
  // Round to nearest minute
  decpart = min * Math.round(decpart / min);
  var minute = Math.floor(decpart * 60) + '';
  // Add padding if need
  if (minute.length < 2) {
  minute = '0' + minute; 
  }  
  // Concate hours and minutes
  return ((hour < 10) ? ('0' + hour) : hour) + ':' + minute;
}
const nth = function (d) {
    d = parseInt(d);
    if (d > 3 && d < 21) return d + 'th';
    switch (d % 10) {
        case 1: return d + "st";
        case 2: return d + "nd";
        case 3: return d + "rd";
        default: return d + "th";
    }
}
const getcalenderformat = function (mydate) {    
    var d = mydate.getDate();
    var m = mydate.getMonth() + 1;
    var y = mydate.getFullYear();
    if (d < 10) d = '0' + d;
    if (m < 10) m = '0' + m;
    var fd = y + '-' + m + '-' + d;
    return fd;
}
const getFormattedDate = function (daysplit) {
    var formatteddate = nth(daysplit[2]) + ' ' + daysplit[1];
    return formatteddate;
}
const getFullWeekend = function (dayname) {
    switch (dayname) {
        case 'Mon': return "Monday";
        case 'Tue': return "Tuesday";
        case 'Wed': return "Wednesday";
        case 'Thu': return "Thrusday";
        case 'Fri': return "Friday";
        case 'Sat': return "Saturday";
        case 'Sun': return "Sunday";
        default: return "";
    }
}

const getWeekDayNo = function (dayname) {
    switch (dayname) {
        case 'Mon': return 1;
        case 'Tue': return 2;
        case 'Wed': return 3;
        case 'Thu': return 4;
        case 'Fri': return 5;
        case 'Sat': return 6;
        case 'Sun': return 7;
        default: return "";
    }
}

const getReportWeekDayNo = function (dayname) {
    switch (dayname) {
        case 'Mon': return 4;
        case 'Tue': return 5;
        case 'Wed': return 6;
        case 'Thu': return 7;
        case 'Fri': return 1;
        case 'Sat': return 2;
        case 'Sun': return 3;
        default: return "";
    }
}

function printDiv(div) {
  var PW = window.open('', '_blank', 'Print content');
  //IF YOU HAVE DIV STYLE IN CSS, REMOVE BELOW COMMENT AND ADD CSS ADDRESS
  PW.document.write('<link href="../css/print.css" rel="stylesheet" />');
  PW.document.write(document.getElementById(div).innerHTML);
  PW.document.close();
  PW.focus();
  setTimeout(function () {
      PW.print();
      PW.close();
  }, 500);
}
function printDivPortrait(div, csslink) {
    var PW = window.open('', '_blank', 'Print content');
    //IF YOU HAVE DIV STYLE IN CSS, REMOVE BELOW COMMENT AND ADD CSS ADDRESS
    // '<link href="../css/print.css" rel="stylesheet" />'
    PW.document.write('<link href="'+csslink+'" rel="stylesheet" />');
    PW.document.write(document.getElementById(div).innerHTML);
    PW.document.close();
    PW.focus();
    setTimeout(function () {
        PW.print();
        PW.close();
    }, 500);
  }

function OnSuccessRequest(result) {
  if (result.MessageType == MessageType.Success) {
      alertify.success(result.Message);
  }
  else if (result.MessageType == MessageType.Failed) {
      alertify.error(result.Message);
      return false;
  }
  else {
      alertify.confirm('Something went wrong.For Detail, Please Check Console');
      return false;
  }
  return true;
}
const getreportdata = function(){
  return [
    {
        "employee_id": 1,
        "task_id": 1,
        "task_name": "WEM Floor 1 West Area Cleaning",
        "project_id": 6,
        "project_name": "Tim Hortons ",
        "category_id": 1,
        "category_name": "Floor Cleaner",
        "notes": "What do you call a local json file? local on the browser or the server? ",
        "insert_date": "2022-01-10",
        "entry_date": "2022-01-21",
        "start_time": "2022-01-21 8:10:10",
        "end_time": "2022-01-21 10:10:30",
        "total_hours": "2:00"
    },
    {
        "employee_id": 1,
        "task_id": 1,
        "task_name": "WEM Floor 1 West Area Cleaning",
        "project_id": 6,
        "project_name": "South Edmonton Common",
        "category_id": 1,
        "category_name": "Floor Cleaner",
        "notes": "What do you call a local json file? local on the browser or the server? ",
        "insert_date": "2022-01-10",
        "entry_date": "2022-01-22",
        "start_time": "2022-01-22 8:10:10",
        "end_time": "2022-01-22 10:10:30",
        "total_hours": "1:00"
    },
    {
        "employee_id": 1,
        "task_id": 1,
        "task_name": "Floor 1 West Area Cleaning",
        "project_id": 6,
        "project_name": "Tim Hortons Common",
        "category_id": 1,
        "category_name": "Floor Cleaner",
        "notes": "What do you call a local json file? local on the browser or the server? ",
        "insert_date": "2022-01-10",
        "entry_date": "2022-01-23",
        "start_time": "2022-01-23 8:10:10",
        "end_time": "2022-01-23 10:10:30",
        "total_hours": "1:00"
    },
    {
        "employee_id": 1,
        "task_id": 1,
        "task_name": "WEM 1 West Area Cleaning",
        "project_id": 6,
        "project_name": "Tim Edmonton Common",
        "category_id": 1,
        "category_name": "Floor Cleaner",
        "notes": "What do you call a local json file? local on the browser or the server? ",
        "insert_date": "2022-01-10",
        "entry_date": "2022-01-24",
        "start_time": "2022-01-24 8:10:10",
        "end_time": "2022-01-24 10:10:30",
        "total_hours": "2:20"
    },
    {
        "employee_id": 1,
        "task_id": 1,
        "task_name": "WEM Floor 1 Area Cleaning",
        "project_id": 6,
        "project_name": "Tim Hortons South",
        "category_id": 1,
        "category_name": "Floor Cleaner",
        "notes": "What do you call a local json file? local on the browser or the server? ",
        "insert_date": "2022-01-10",
        "entry_date": "2022-01-25",
        "start_time": "2022-01-25 8:10:10",
        "end_time": "2022-01-25 10:10:30",
        "total_hours": "3:20"
    },
    {
        "employee_id": 1,
        "task_id": 1,
        "task_name": "WEM Floor 1 West Cleaning",
        "project_id": 6,
        "project_name": "Tim Hortons South Edmonton",
        "category_id": 1,
        "category_name": "Floor Cleaner",
        "notes": "What do you call a local json file? local on the browser or the server? ",
        "insert_date": "2022-01-10",
        "entry_date": "2022-01-26",
        "start_time": "2022-01-26 8:10:10",
        "end_time": "2022-01-26 10:10:30",
        "total_hours": "1:20"
    },
    {
        "employee_id": 1,
        "task_id": 1,
        "task_name": "WEM Floor 1 West Area ",
        "project_id": 6,
        "project_name": "Hortons South Edmonton Common",
        "category_id": 1,
        "category_name": "Floor Cleaner",
        "notes": "What do you call a local json file? local on the browser or the server? ",
        "insert_date": "2022-01-10",
        "entry_date": "2022-01-27",
        "start_time": "2022-01-27 8:10:10",
        "end_time": "2022-01-27 10:10:30",
        "total_hours": "1:50"
    },
    {
        "employee_id": 1,
        "task_id": 1,
        "task_name": "WEM Floor 1  Area Cleaning",
        "project_id": 6,
        "project_name": "Tim Hortons South  Common",
        "category_id": 1,
        "category_name": "Floor Cleaner",
        "notes": "What do you call a local json file? local on the browser or the server? ",
        "insert_date": "2022-01-10",
        "entry_date": "2022-01-28",
        "start_time": "2022-01-28 8:10:10",
        "end_time": "2022-01-28 10:10:30",
        "total_hours": "2:40"
    },
    {
      "employee_id": 1,
      "task_id": 1,
      "task_name": "WEM Floor 1 West Area Cleaning",
      "project_id": 6,
      "project_name": "Tim Hortons ",
      "category_id": 1,
      "category_name": "Floor Cleaner",
      "notes": "What do you call a local json file? local on the browser or the server? ",
      "insert_date": "2022-01-10",
      "entry_date": "2022-01-21",
      "start_time": "2022-01-21 8:10:10",
      "end_time": "2022-01-21 10:10:30",
      "total_hours": "2:00"
  },
  {
      "employee_id": 1,
      "task_id": 1,
      "task_name": "WEM Floor 1 West Area Cleaning",
      "project_id": 6,
      "project_name": "South Edmonton Common",
      "category_id": 1,
      "category_name": "Floor Cleaner",
      "notes": "What do you call a local json file? local on the browser or the server? ",
      "insert_date": "2022-01-10",
      "entry_date": "2022-01-22",
      "start_time": "2022-01-22 8:10:10",
      "end_time": "2022-01-22 10:10:30",
      "total_hours": "1:00"
  },
  {
      "employee_id": 1,
      "task_id": 1,
      "task_name": "Floor 1 West Area Cleaning",
      "project_id": 6,
      "project_name": "Tim Hortons Common",
      "category_id": 1,
      "category_name": "Floor Cleaner",
      "notes": "What do you call a local json file? local on the browser or the server? ",
      "insert_date": "2022-01-10",
      "entry_date": "2022-01-23",
      "start_time": "2022-01-23 8:10:10",
      "end_time": "2022-01-23 10:10:30",
      "total_hours": "1:00"
  },
  {
      "employee_id": 1,
      "task_id": 1,
      "task_name": "WEM 1 West Area Cleaning",
      "project_id": 6,
      "project_name": "Tim Edmonton Common",
      "category_id": 1,
      "category_name": "Floor Cleaner",
      "notes": "What do you call a local json file? local on the browser or the server? ",
      "insert_date": "2022-01-10",
      "entry_date": "2022-01-24",
      "start_time": "2022-01-24 8:10:10",
      "end_time": "2022-01-24 10:10:30",
      "total_hours": "2:20"
  },
  {
      "employee_id": 1,
      "task_id": 1,
      "task_name": "WEM Floor 1 Area Cleaning",
      "project_id": 6,
      "project_name": "Tim Hortons South",
      "category_id": 1,
      "category_name": "Floor Cleaner",
      "notes": "What do you call a local json file? local on the browser or the server? ",
      "insert_date": "2022-01-10",
      "entry_date": "2022-01-25",
      "start_time": "2022-01-25 8:10:10",
      "end_time": "2022-01-25 10:10:30",
      "total_hours": "3:20"
  },
  {
      "employee_id": 1,
      "task_id": 1,
      "task_name": "WEM Floor 1 West Cleaning",
      "project_id": 6,
      "project_name": "Tim Hortons South Edmonton",
      "category_id": 1,
      "category_name": "Floor Cleaner",
      "notes": "What do you call a local json file? local on the browser or the server? ",
      "insert_date": "2022-01-10",
      "entry_date": "2022-01-26",
      "start_time": "2022-01-26 8:10:10",
      "end_time": "2022-01-26 10:10:30",
      "total_hours": "1:20"
  },
  {
      "employee_id": 1,
      "task_id": 1,
      "task_name": "WEM Floor 1 West Area ",
      "project_id": 6,
      "project_name": "Hortons South Edmonton Common",
      "category_id": 1,
      "category_name": "Floor Cleaner",
      "notes": "What do you call a local json file? local on the browser or the server? ",
      "insert_date": "2022-01-10",
      "entry_date": "2022-01-27",
      "start_time": "2022-01-27 8:10:10",
      "end_time": "2022-01-27 10:10:30",
      "total_hours": "1:50"
  },
  {
      "employee_id": 1,
      "task_id": 1,
      "task_name": "WEM Floor 1  Area Cleaning",
      "project_id": 6,
      "project_name": "Tim Hortons South  Common",
      "category_id": 1,
      "category_name": "Floor Cleaner",
      "notes": "What do you call a local json file? local on the browser or the server? ",
      "insert_date": "2022-01-10",
      "entry_date": "2022-01-28",
      "start_time": "2022-01-28 8:10:10",
      "end_time": "2022-01-28 10:10:30",
      "total_hours": "2:40"
  },
  {
    "employee_id": 1,
    "task_id": 1,
    "task_name": "WEM Floor 1 West Area Cleaning",
    "project_id": 6,
    "project_name": "Tim Hortons ",
    "category_id": 1,
    "category_name": "Floor Cleaner",
    "notes": "What do you call a local json file? local on the browser or the server? ",
    "insert_date": "2022-01-10",
    "entry_date": "2022-01-21",
    "start_time": "2022-01-21 8:10:10",
    "end_time": "2022-01-21 10:10:30",
    "total_hours": "2:00"
},
{
    "employee_id": 1,
    "task_id": 1,
    "task_name": "WEM Floor 1 West Area Cleaning",
    "project_id": 6,
    "project_name": "South Edmonton Common",
    "category_id": 1,
    "category_name": "Floor Cleaner",
    "notes": "What do you call a local json file? local on the browser or the server? ",
    "insert_date": "2022-01-10",
    "entry_date": "2022-01-22",
    "start_time": "2022-01-22 8:10:10",
    "end_time": "2022-01-22 10:10:30",
    "total_hours": "1:00"
},
{
    "employee_id": 1,
    "task_id": 1,
    "task_name": "Floor 1 West Area Cleaning",
    "project_id": 6,
    "project_name": "Tim Hortons Common",
    "category_id": 1,
    "category_name": "Floor Cleaner",
    "notes": "What do you call a local json file? local on the browser or the server? ",
    "insert_date": "2022-01-10",
    "entry_date": "2022-01-23",
    "start_time": "2022-01-23 8:10:10",
    "end_time": "2022-01-23 10:10:30",
    "total_hours": "1:00"
},
{
    "employee_id": 1,
    "task_id": 1,
    "task_name": "WEM 1 West Area Cleaning",
    "project_id": 6,
    "project_name": "Tim Edmonton Common",
    "category_id": 1,
    "category_name": "Floor Cleaner",
    "notes": "What do you call a local json file? local on the browser or the server? ",
    "insert_date": "2022-01-10",
    "entry_date": "2022-01-24",
    "start_time": "2022-01-24 8:10:10",
    "end_time": "2022-01-24 10:10:30",
    "total_hours": "2:20"
},
{
    "employee_id": 1,
    "task_id": 1,
    "task_name": "WEM Floor 1 Area Cleaning",
    "project_id": 6,
    "project_name": "Tim Hortons South",
    "category_id": 1,
    "category_name": "Floor Cleaner",
    "notes": "What do you call a local json file? local on the browser or the server? ",
    "insert_date": "2022-01-10",
    "entry_date": "2022-01-25",
    "start_time": "2022-01-25 8:10:10",
    "end_time": "2022-01-25 10:10:30",
    "total_hours": "3:20"
},
{
    "employee_id": 1,
    "task_id": 1,
    "task_name": "WEM Floor 1 West Cleaning",
    "project_id": 6,
    "project_name": "Tim Hortons South Edmonton",
    "category_id": 1,
    "category_name": "Floor Cleaner",
    "notes": "What do you call a local json file? local on the browser or the server? ",
    "insert_date": "2022-01-10",
    "entry_date": "2022-01-26",
    "start_time": "2022-01-26 8:10:10",
    "end_time": "2022-01-26 10:10:30",
    "total_hours": "1:20"
},
{
    "employee_id": 1,
    "task_id": 1,
    "task_name": "WEM Floor 1 West Area ",
    "project_id": 6,
    "project_name": "Hortons South Edmonton Common",
    "category_id": 1,
    "category_name": "Floor Cleaner",
    "notes": "What do you call a local json file? local on the browser or the server? ",
    "insert_date": "2022-01-10",
    "entry_date": "2022-01-27",
    "start_time": "2022-01-27 8:10:10",
    "end_time": "2022-01-27 10:10:30",
    "total_hours": "1:50"
},
{
    "employee_id": 1,
    "task_id": 1,
    "task_name": "WEM Floor 1  Area Cleaning",
    "project_id": 6,
    "project_name": "Tim Hortons South  Common",
    "category_id": 1,
    "category_name": "Floor Cleaner",
    "notes": "What do you call a local json file? local on the browser or the server? ",
    "insert_date": "2022-01-10",
    "entry_date": "2022-01-28",
    "start_time": "2022-01-28 8:10:10",
    "end_time": "2022-01-28 10:10:30",
    "total_hours": "2:40"
}
]
}
