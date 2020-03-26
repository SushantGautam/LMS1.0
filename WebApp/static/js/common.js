function DateConvert(date) {
    date = new Date(date);
    var options = {year: 'numeric', month: '2-digit', day: 'numeric', hour: '2-digit', minute: '2-digit'};
    let newdate = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate(), date.getHours(), date.getMinutes())).toLocaleString("en-US", options)
    return newdate
}

function convertDateToUTC(date) {
    date = new Date(date).toISOString()
    return date
}

window.onload = function () {
    $('.datecon').each(function () {
        $(this).text(DateConvert($(this).text()))
    })
}