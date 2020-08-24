var api_url = "/inbox/notifications/?max=10";
var live_api_url = "/inbox/notifications/api/unread_count/";

var unread_notification = null;

function getNotifications() {
    $.ajax({
        url: api_url,
        method: 'GET',
        success: function (data) {
            $('#notification_menu1').html('').html(data)
        },
        error: function (e) {
            console.log(e.responseText)
        }
    })
}

function getLiveNotification() {
    $.ajax({
        url: live_api_url,
        method: 'GET',
        success: function (data) {
            if (!unread_notification || data.unread_count != unread_notification) {
                unread_notification = data.unread_count;
                // console.log('here', data.unread_count, unread_notification, data.unread_count != unread_notification)
                $('#notification_count').text('').text(data.unread_count);
                getNotifications();
            }
        },
        error: function (e) {
            console.log(e.responseText)
        }
    })
}

getLiveNotification()
setInterval(getLiveNotification, 10000);