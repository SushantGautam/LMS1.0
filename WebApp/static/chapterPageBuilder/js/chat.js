const chatLog = document.querySelector('#chat-log');
const chatCanvas = document.querySelector('.chat-canvas');
const mainChatBox = document.querySelector('#main-chat-box');
const unreadChat = document.querySelector('.unread-chat-count');
const onlineUserCount = document.querySelector('.online-number');
const onlineUserList = document.querySelector('.user-list');
const screenSync = document.querySelector('#id_screen_sync');
const currentPageNo = document.querySelector('#current-pg-num');

// Info about user and chat room
const roomID = document.querySelector(".chat-info").getAttribute("data-chapterID");
const userID = document.querySelector(".chat-info").getAttribute("data-userID");
const userName = document.querySelector(".chat-info").getAttribute("data-userName");
const userIcon = document.querySelector(".chat-info").getAttribute("data-userIcon");

// Sound object
const soundIn = new Howl({src: [audioURLIn], volume: 0.6,});
const soundOut = new Howl({src: [audioURLOut], volume: 0.6,});

// Chatsocket url
const locationhost = window.location.host;
const webSProtocal = location.protocol === 'https:' ? "wss://" : "ws://";
const chatSocket = new WebSocket(webSProtocal + locationhost + "/ws/" + roomID + '/');

// For Notification detecting inactive tab
var hidden, visibilityChange;
if (typeof document.hidden !== "undefined") { // Opera 12.10 and Firefox 18 and later support 
    hidden = "hidden";
    visibilityChange = "visibilitychange";
} else if (typeof document.msHidden !== "undefined") {
    hidden = "msHidden";
    visibilityChange = "msvisibilitychange";
} else if (typeof document.webkitHidden !== "undefined") {
    hidden = "webkitHidden";
    visibilityChange = "webkitvisibilitychange";
}

// When chatsocket recieve message
chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    const notificationVal = document.querySelector("#id_notification").value;
    const soundVal = document.querySelector("#id_sound").value;
    if (data.message_type === 'chat_users') {
        let users = data.user_list;

        // Clear onlineUserList at first
        onlineUserList.innerHTML = '';

        onlineUserCount.innerHTML = data.user_count;

        users.forEach(user => {
            onlineUserList.innerHTML += `
                    <div class="eachbox">
                        <ul class="leftchat-userbox">
                            <li>
                                <div class="chat-user-image2"><img src="${user.avatar}"></div>
                            </li>
                            <li><span style="font-size:10px ; font-weight:600">${user.username}</span></li>
                        </ul>
                    </div>`;
        });
    } else if (data.message_type === 'screen_sync') {
        if (!screenSync) {
            const event = new Event('change');
            document.querySelector('#pg-change').value = data.message;
            document.querySelector('#pg-change').dispatchEvent(event);
            console.log(data.message);
        }

    } else if (data.message_type === 'chat_message') {
        // converting datetime to local
        let sender_datetime = new Date(data.sender_datetime);
        let localtime = new Date(Date.UTC(sender_datetime.getFullYear(),
            sender_datetime.getMonth(),
            sender_datetime.getDate(),
            sender_datetime.getHours(),
            sender_datetime.getMinutes(),
            sender_datetime.getSeconds())).toLocaleString('en-US', {hour12: true, hour: "numeric", minute: "numeric"});

        // Checking if the message is sent by same user
        let msgClass = userID === data.sender_id ? "right-msg" : "left-msg";
        let msg = '';

        // Play sound if sound option is on
        if (soundVal === '1' && msgClass === "left-msg") soundIn.play();
        if (soundVal === '1' && msgClass === "right-msg") soundOut.play();

        // if message_link_type present, then get link
        if (data.hasOwnProperty('message_link_type')) {
            msg = getTypeLink(data.message_link_type, data.message);
        } else {
            msg = data.message;
        }

        // Check log visible and add unread message counter
        if (mainChatBox.style.display === 'none') {
            unreadChat.style.display = "inline";
        }

        // Appending message to canvas log
        let localdate = new Date(Date.UTC(sender_datetime.getFullYear(),
            sender_datetime.getMonth(),
            sender_datetime.getDate(),
            sender_datetime.getHours(),
            sender_datetime.getMinutes(),
            sender_datetime.getSeconds())).toLocaleString('en-US', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit'
        });

        if (datearr.indexOf(localdate) == -1) {
            let now = new Date();
            datearr.push(localdate)
            date_to_display = null;
            localdate_dateObj = new Date(localdate)
            date_difference = Math.floor((now - localdate_dateObj) / 86400000)

            if (date_difference == 0) {
                date_to_display = 'Today'
            } else if (date_difference == 1) {
                date_to_display = 'Yesterday'
            } else {
                date_to_display = localdate
            }
            chatdatediv = `
            <div class="chat-today" data-localdate="${localdate}">
                        <span class="chat-date">${date_to_display}</span>
                </div>
            `
        } else {
            chatdatediv = ''
        }
        chatLog.innerHTML += `
                ${chatdatediv}
                <div class="msg ${msgClass}">
                    <div class="msg-img" style="background-image: url(${data.sender_icon})"></div>
                    <div class="msg-bubble">
                        <div class="msg-info">
                        <div class="msg-info-name">${data.sender_name}</div>
                        <div class="msg-info-time timecon">${localtime}</div>
                        </div>
                        <div class="msg-text">
                        ${msg}
                        </div>
                    </div>
                    </div>`;

        // Scroll Down on New message
        chatCanvas.scrollTop = chatCanvas.scrollHeight;

        // Adding browser notification if Notification is on and tab not active
        if (document[hidden]) {
            if (notificationVal === '1' && msgClass === "left-msg") {
                if (!window.Notification) {
                    console.log('Browser does not support notifications.');
                } else {
                    // check if permission is already granted
                    if (Notification.permission === 'granted') {
                        // show notification
                        let notify = new Notification(data.sender_name, {
                            body: data.message,
                            icon: data.sender_icon,
                        });
                    } else {
                        // request permission from user
                        Notification.requestPermission().then(function (p) {
                            if (p === 'granted') {
                                // show notification
                                let notify = new Notification(data.sender_name, {
                                    body: data.message,
                                    icon: data.sender_icon,
                                });
                            } else {
                                console.log('User blocked notifications.');
                            }
                        }).catch(function (err) {
                            console.error(err);
                        });
                    }
                }
            }
        }

    }
};

// Execute on chatsocket close
chatSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};

// Focusing the message input box after sending message
document.querySelector('#chat-message-input').focus();
// When enter is pressed sending message
document.querySelector('#chat-message-input').onkeyup = function (e) {
    if (e.keyCode === 13) {
        document.querySelector('#chat-message-submit').click();
    }
};

// Sending message to websocket
document.querySelector('#chat-message-submit').onclick = function () {
    sendChatMessage()
}

// Sending pagechange to websocket if screenSync is true
currentPageNo.onchange = function () {
    if (screenSync) {
        if (screenSync.checked == true) {
            let currentDateTime = new Date().toLocaleString('en-US', {timeZone: 'UTC'});
            const pageNo = currentPageNo.value;
            const messageData = {
                'message_type': 'screen_sync',
                'sender_id': userID,
                'sender_name': userName,
                'sender_icon': userIcon,
                'sender_datetime': currentDateTime,
                'message': pageNo,
            }
            chatSocket.send(JSON.stringify(messageData));
        }
    }
};

function sendChatMessage(extraParam = null) {
    let currentDateTime = new Date().toLocaleString('en-US', {timeZone: 'UTC'});
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    // Prevent submission of empty message
    if (!message) return;
    let messageData = {
        'message_type': 'chat_message',
        'sender_id': userID,
        'sender_name': userName,
        'sender_icon': userIcon,
        'sender_datetime': currentDateTime,
        'message': message,
    }
    if (extraParam) {
        for (var attrname in extraParam) {
            messageData[attrname] = extraParam[attrname];
        }
    }
    chatSocket.send(JSON.stringify(messageData));
    messageInputDom.value = '';
};


// Retrieve Chat history
if (chatHistory.length === 0) {
    $(document).ready(function () {
        chatLog.innerHTML = `<div class="msg left-msg">
                <div class="msg-img"
                        style="background-image: url(${botImage})"></div>
                <div class="msg-bubble">
                    <div class="msg-info">
                        <div class="msg-info-name">LMS BOT</div>
                        <div class="default-time msg-info-time"></div>
                    </div>
                    <div class="msg-text">
                        Hello! You can now send message to everyone here.
                    </div>
                </div>
            </div>`;
    });

} else {
    $(document).ready(function () {

        // Clear chatlog at first
        chatLog.innerHTML = '';
        chatdatediv = '';
        // let datearr = [];
        let now = new Date();
        addMessageToChat(chatHistory)
        if (chatDetails.next_page != '') {
            var conn = document.createElement('div');
            conn.innerHTML = `<div id="see_more_messages"> See More </div>`
            chatLog.parentElement.insertBefore(conn, chatLog)
        }
        // Scroll Down after message append
        mainChatBox.style.display = "block";
        chatCanvas.scrollTop = chatCanvas.scrollHeight;
        mainChatBox.style.display = "none";

    });

    function getTypeLink(linktype, linkmsg) {
        if (linktype == 'quiz') {
            if (window.location.href.indexOf("/teachers") > -1) {
                msg = `<a onclick="loadexam('/quiz/markingfilter/${linkmsg}/?iframe=1', 1)">View Quick Quiz Submissions</a>`
            } else if (window.location.href.indexOf("/students") > -1) {
                msg = `<a onclick="loadexam('/quiz/quiz${linkmsg}/take/?iframe=1')">Take Quick Quiz</a>`
            } else {
                msg = `<a onclick="loadexam('/quiz/detail/${linkmsg}/?iframe=1', 1)">View Quick Quiz Details</a>`
            }
        } else if (linktype == 'survey') {
            if (window.location.href.indexOf("/teachers") > -1) {
                msg = `<a onclick="loadexam('/teachers/surveyinfodetail/detail/${linkmsg}/?iframe=1', 1)">View Quick Survey Submissions</a>`
            } else if (window.location.href.indexOf("/students") > -1) {
                msg = `<a onclick="loadexam('/students/questions_student_detail/detail/${linkmsg}/?iframe=1')">Take Quick Survey</a>`
            } else {
                msg = `<a onclick="loadexam('/survey/surveyinfo/detail/${linkmsg}/?iframe=1', 1)">View Quick Survey Submissions</a>`
            }
        }
        return msg
    }
}
$(document).ready(function () {
    $('#see_more_messages').on('click', function () {
        $.get(chatDetails.next_page, function (chat_data) {
            chatDetails = chat_data;
            if (chatDetails.next_page == '') {
                $('#see_more_messages').remove()
            }
            addMessageToChat(chat_data.chat_history)
        })
    })
})

function addMessageToChat(chat_history) {
    // let datearr = [];
    let now = new Date();
    chat_history.forEach(data => {
        let msgClass = userID === data.sender_id ? "right-msg" : "left-msg";

        // converting datetime to local
        let sender_datetime = new Date(data.sender_datetime);
        let localtime = new Date(Date.UTC(sender_datetime.getFullYear(),
            sender_datetime.getMonth(),
            sender_datetime.getDate(),
            sender_datetime.getHours(),
            sender_datetime.getMinutes(),
            sender_datetime.getSeconds())).toLocaleString('en-US', {
            hour12: true,
            hour: "numeric",
            minute: "numeric"
        });
        let localdate = new Date(Date.UTC(sender_datetime.getFullYear(),
            sender_datetime.getMonth(),
            sender_datetime.getDate(),
            sender_datetime.getHours(),
            sender_datetime.getMinutes(),
            sender_datetime.getSeconds())).toLocaleString('en-US', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit'
        });
        if (datearr.indexOf(localdate) == -1) {
            datearr.push(localdate)
            date_to_display = null;
            localdate_dateObj = new Date(localdate)
            date_difference = Math.floor((now - localdate_dateObj) / 86400000)

            if (date_difference == 0) {
                date_to_display = 'Today'
            } else if (date_difference == 1) {
                date_to_display = 'Yesterday'
            } else {
                date_to_display = localdate
            }
            chatdatediv = `
            <div class="chat-today" data-localdate="${localdate}">
                        <span class="chat-date">${date_to_display}</span>
                </div>
            `
        } else {
            // chatdatediv = ''
            $(`.chat-today[data-localdate="${localdate}"]`).remove()
            chatdatediv = `
            <div class="chat-today" data-localdate="${localdate}">
                        <span class="chat-date">${date_to_display}</span>
                </div>
            `
        }

        // Appending message to canvas log

        if (data.hasOwnProperty('message_link_type')) {
            var msg = getTypeLink(data.message_link_type, data.message)
            if (data.hasOwnProperty('isComplete') && window.location.href.indexOf("/students") > -1) {
                var completeStatus = data.isComplete == 1 ? '<i style="color: green" class="fa fa-check" aria-hidden="true"></i>' : ''
            } else {
                var completeStatus = ''
            }

        } else {
            var msg = data.message
            var completeStatus = ''
        }
        $(chatLog).prepend(`
            ${chatdatediv}
            <div class="msg ${msgClass}">
                <div class="msg-img" style="background-image: url(${data.sender_icon})"></div>
                <div class="msg-bubble">
                    <div class="msg-info">
                    <div class="msg-info-name">${data.sender_name}</div>
                    <div class="msg-info-time timecon">${localtime}</div>
                    </div>
                    <div class="msg-text">
                    ${completeStatus}${msg}
                    </div>
                </div>
            </div>
        `);
    });
}