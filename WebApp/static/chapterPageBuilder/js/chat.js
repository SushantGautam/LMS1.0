const chatLog = document.querySelector('#chat-log');
const chatCanvas = document.querySelector('.chat-canvas');
const mainChatBox = document.querySelector('#main-chat-box');

// Info about user and chat room
const roomID = document.querySelector(".chat-info").getAttribute("data-chapterID");
const userID = document.querySelector(".chat-info").getAttribute("data-userID");
const userName = document.querySelector(".chat-info").getAttribute("data-userName");
const userIcon = document.querySelector(".chat-info").getAttribute("data-userIcon");

// Sound object
const soundIn = new Howl({ src: [audioURLIn], volume: 0.6, });
const soundOut = new Howl({ src: [audioURLOut], volume: 0.6, });

// Chatsocket url
const locationhost = window.location.host;
const webSProtocal = location.protocol === 'https:' ? "wss://" : "ws://";
const chatSocket = new WebSocket(webSProtocal + locationhost + "/ws/" + roomID + '/');

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
chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const notificationVal = document.querySelector("#id_notification").value;
    const soundVal = document.querySelector("#id_sound").value;

    if (data.message_type === 'message'){
        // converting datetime to local
        let sender_datetime = new Date(data.sender_datetime);
        let localtime = new Date(Date.UTC(sender_datetime.getFullYear(),
            sender_datetime.getMonth(),
            sender_datetime.getDate(),
            sender_datetime.getHours(),
            sender_datetime.getMinutes(),
            sender_datetime.getSeconds())).toLocaleString('en-US', { hour12: true, hour: "numeric", minute: "numeric"});

        // Checking if the message is sent by same user
        let msgClass = userID === data.sender_id ? "right-msg" : "left-msg";

        // Play sound if sound option is on
        if(soundVal==='1' && msgClass==="left-msg") soundIn.play();
        if(soundVal==='1' && msgClass==="right-msg") soundOut.play();

        // Appending message to canvas log
        chatLog.innerHTML += `
                <div class="msg ${msgClass}">
                    <div class="msg-img" style="background-image: url(${data.sender_icon})"></div>
                    <div class="msg-bubble">
                        <div class="msg-info">
                        <div class="msg-info-name">${data.sender_name}</div>
                        <div class="msg-info-time timecon">${localtime}</div>
                        </div>
                        <div class="msg-text">
                        ${data.message}
                        </div>
                    </div>
                    </div>`;
        
        // Scroll Down on New message
        chatCanvas.scrollTop = chatCanvas.scrollHeight;

        // Adding browser notification if Notification is on and tab not active
        if (document[hidden]) {
            if (notificationVal === '1' && msgClass==="left-msg"){
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
chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

// Focusing the message input box after sending message
document.querySelector('#chat-message-input').focus();
// When enter is pressed sending message
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {
        document.querySelector('#chat-message-submit').click();
    }
};

// Sending message to websocket
document.querySelector('#chat-message-submit').onclick = function(e) {
    let currentDateTime = new Date().toLocaleString('en-US', { timeZone: 'UTC' });
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;

    // Prevent submission of empty message
    if (!message) return;

    chatSocket.send(JSON.stringify({
        'sender_id': userID,
        'sender_name': userName,
        'sender_icon': userIcon,
        'sender_datetime': currentDateTime,
        'message': message,
    }));
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

}
else {
    $(document).ready(function () {
        
        // Clear chatlog at first
        chatLog.innerHTML = '';
        
        chatHistory.forEach(data => {
            let msgClass = userID === data.sender_id ? "right-msg" : "left-msg";

            // converting datetime to local
            let sender_datetime = new Date(data.sender_datetime);
            let localtime = new Date(Date.UTC(sender_datetime.getFullYear(),
                    sender_datetime.getMonth(),
                    sender_datetime.getDate(),
                    sender_datetime.getHours(),
                    sender_datetime.getMinutes(),
                    sender_datetime.getSeconds())).toLocaleString('en-US', { hour12: true, hour: "numeric", minute: "numeric"});
                        
            // Appending message to canvas log
            chatLog.innerHTML += `
                    <div class="msg ${msgClass}">
                        <div class="msg-img" style="background-image: url(${data.sender_icon})"></div>
                        <div class="msg-bubble">
                            <div class="msg-info">
                            <div class="msg-info-name">${data.sender_name}</div>
                            <div class="msg-info-time timecon">${localtime}</div>
                            </div>
                            <div class="msg-text">
                            ${data.message}
                            </div>
                        </div>
                        </div>`;

        });

        // Scroll Down after message append
        mainChatBox.style.display = "block";
        chatCanvas.scrollTop = chatCanvas.scrollHeight;
        mainChatBox.style.display = "none";

    });
}