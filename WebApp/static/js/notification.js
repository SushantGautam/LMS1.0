var api_url = "/inbox/notifications/?max=10";
var live_api_url = "/inbox/notifications/api/unread_count/";

var unread_notification = null;

function getNotifications() {
    $.ajax({
        url: api_url,
        method: 'GET',
        success: function (data) {
            $('#notification_menu1').html('').html(data)
        }
    });
}

function getLiveNotification() {
    $.ajax({
        url: live_api_url,
        method: 'GET',
        success: function (data) {
            if (!unread_notification || data.unread_count != unread_notification) {
                unread_notification = data.unread_count;
                // console.log('here', data.unread_count, unread_notification, data.unread_count != unread_notification)
                parseInt(data.unread_count) > 0 ? $('#notification_count').text('').text(data.unread_count) : $('#notification_count').text('');
                getNotifications();
            }
        },
        error: function (e) {
            console.log(e.responseText)
        }
    })
}

getLiveNotification()
setInterval(getLiveNotification, 600000);
