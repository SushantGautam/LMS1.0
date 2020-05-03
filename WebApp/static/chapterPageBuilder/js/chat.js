
const chatLog = document.querySelector('#chat-log');
const chatCanvas = document.querySelector('.chat-canvas');

const roomID = document.querySelector(".chat-info").getAttribute("data-chapterID");
const userID = document.querySelector(".chat-info").getAttribute("data-userID");
const userName = document.querySelector(".chat-info").getAttribute("data-userName");
const userIcon = document.querySelector(".chat-info").getAttribute("data-userIcon");

let webSProtocal = '';
let locationhost = window.location.host;

if (location.protocol === 'https:') {
    webSProtocal = "wss://";
} else {
    webSProtocal = "ws://";
}

console.log(locationhost);

const chatSocket = new WebSocket(webSProtocal + locationhost + "/ws/" + roomID + '/');

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);

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
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

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