const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/currency/'
);

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    document.querySelector('#app').innerHTML = JSON.stringify(data.message, null, 2);
};

chatSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};
