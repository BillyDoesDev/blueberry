const socket = io();
socket.on('connect', function () {
    console.log("connecttion to websocket successful")
    socket.emit('my event', { data: 'I\'m connected!' });
});