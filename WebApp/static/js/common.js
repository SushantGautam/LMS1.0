function DateConvert(date) {
    if (date == "") {
        return 'None'
    }
    date = new Date(date);
    var options = {year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit'};
    let newdate = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate(), date.getHours(), date.getMinutes())).toLocaleString("en-IN", options)
    return newdate
}

function convertDateToUTC(date) {
    date = new Date(date).toISOString()
    return date
}

function TimeConvert(date) {
    date = new Date(date);
    var options = {
        year: 'numeric',
        month: '2-digit',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    };
    let newdate = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate(), date.getHours(), date.getMinutes(), date.getSeconds())).toLocaleString("en-US", options);
    return newdate.split(' ')[1] + ' ' + newdate.split(' ')[2]
}

function DateConvertFullMonth(date) {
    if (date == "") {
        return 'None'
    }
    date = new Date(date);
    var options = {year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'};
    let newdate = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate(), date.getHours(), date.getMinutes())).toLocaleString("en-IN", options)
    return newdate
}

window.onload = function () {
    $('.datecon').each(function () {
        $(this).text(DateConvert($(this).text()))
    });
    $('.timecon').each(function () {
        $(this).text(TimeConvert($(this).text()))
    });
    $('.dateconFullMonth').each(function () {
        $(this).text(DateConvertFullMonth($(this).text()))
    });
}

// end_date, start_date must be date objects
function dateDifference(end_date, start_date) {
    if (end_date < start_date) {
        return "Expired"
    }
    var msec = end_date - start_date;
    var mins = Math.floor(msec / 60000);
    var hrs = Math.floor(mins / 60);
    var days = Math.floor(hrs / 24);
    var yrs = Math.floor(days / 365);
    mins = mins % 60;
    hrs = hrs % 24;
    return days + " days, " + hrs + " hours, " + mins + " minutes"
}

$(document).on('click', '.dropdown-menu', function (e) {
    e.stopPropagation();
});